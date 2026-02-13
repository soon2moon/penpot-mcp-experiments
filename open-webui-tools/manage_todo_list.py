"""
title: Task Tracking Tool for Design Workflows
author: Victor Vibe
author_url: https://github.com/soon2moon/penpot-mcp-experiments
description: A todo list management tool that enables LLMs to break down complex design tasks into trackable steps, monitor progress, and ensure systematic completion of multi-step operations.
required_open_webui_version: 0.4.0
version: 0.2.0
license: MIT

Usage in prompts:
<taskTracking>
Utilize the manage_todo_list tool extensively to organize work and provide visibility 
into your progress. This is essential for planning and ensures important steps aren't forgotten.

Break complex work into logical, actionable steps that can be tracked and verified. 
Update task status consistently throughout execution:
- Mark tasks as in-progress when you begin working on them
- Mark tasks as completed immediately after finishing each one

Task tracking is valuable for:
- Multi-step work requiring careful sequencing
- Breaking down ambiguous or complex requests
- Maintaining checkpoints for feedback and validation
- When users provide multiple requests or numbered tasks
</taskTracking>
"""

import json
from datetime import datetime
from typing import Callable, Any, List, Optional
from pydantic import BaseModel, Field


class Tools:
    """
    Task Tracking Tool for managing todo lists during complex design workflows.
    
    Enables LLMs to:
    - Break down complex tasks into trackable steps
    - Monitor progress through multi-step operations
    - Maintain visibility into planned vs completed work
    - Ensure systematic completion without missed steps
    """
    
    class Valves(BaseModel):
        MAX_TODOS: int = Field(
            default=50, 
            description="Maximum number of todo items allowed per session."
        )
        AUTO_CLEANUP_COMPLETED: bool = Field(
            default=False,
            description="Automatically remove completed todos when list is full."
        )
        DEBUG: bool = Field(
            default=False, 
            description="Enable debug logging."
        )

    class UserValves(BaseModel):
        SHOW_TIMESTAMPS: bool = Field(
            default=True,
            description="Show creation/update timestamps in todo list."
        )

    def __init__(self):
        self.valves = self.Valves()
        # In-memory storage for todos (per-session)
        # In production, consider using Open WebUI's Memories API for persistence
        self._todo_storage: dict[str, List[dict]] = {}

    def _get_user_todos(self, user_id: str) -> List[dict]:
        """Get todos for a specific user."""
        if user_id not in self._todo_storage:
            self._todo_storage[user_id] = []
        return self._todo_storage[user_id]

    def _set_user_todos(self, user_id: str, todos: List[dict]):
        """Set todos for a specific user."""
        self._todo_storage[user_id] = todos

    def _format_status_icon(self, status: str) -> str:
        """Return an icon for the status."""
        icons = {
            "not-started": "○",
            "in-progress": "◐",
            "completed": "●"
        }
        return icons.get(status, "○")

    def _format_todo_list(self, todos: List[dict], show_timestamps: bool = True) -> str:
        """Format the todo list for display."""
        if not todos:
            return "No tasks in the todo list."
        
        lines = ["## Task Progress\n"]
        
        # Group by status
        in_progress = [t for t in todos if t["status"] == "in-progress"]
        not_started = [t for t in todos if t["status"] == "not-started"]
        completed = [t for t in todos if t["status"] == "completed"]
        
        # Summary
        total = len(todos)
        completed_count = len(completed)
        lines.append(f"**Progress: {completed_count}/{total} tasks completed**\n")
        
        # In Progress section
        if in_progress:
            lines.append("\n### 🔄 In Progress")
            for todo in in_progress:
                icon = self._format_status_icon(todo["status"])
                line = f"  {icon} [{todo['id']}] {todo['title']}"
                if show_timestamps:
                    line += f" _(started: {todo.get('updated_at', 'N/A')[:16]})_"
                lines.append(line)
        
        # Not Started section
        if not_started:
            lines.append("\n### ⏳ Pending")
            for todo in not_started:
                icon = self._format_status_icon(todo["status"])
                lines.append(f"  {icon} [{todo['id']}] {todo['title']}")
        
        # Completed section
        if completed:
            lines.append("\n### ✅ Completed")
            for todo in completed:
                icon = self._format_status_icon(todo["status"])
                line = f"  {icon} [{todo['id']}] ~~{todo['title']}~~"
                if show_timestamps:
                    line += f" _(completed: {todo.get('updated_at', 'N/A')[:16]})_"
                lines.append(line)
        
        return "\n".join(lines)

    async def manage_todo_list(
        self,
        todo_list: List[dict],
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Manage a structured todo list to track progress and plan tasks throughout your design session.
        Use this tool FREQUENTLY to ensure task visibility and proper planning.

        When to use this tool:
        - Complex multi-step work requiring planning and tracking
        - When user provides multiple tasks or requests (numbered/comma-separated)
        - After receiving new instructions that require multiple steps
        - BEFORE starting work on any todo (mark as in-progress)
        - IMMEDIATELY after completing each todo (mark completed individually)
        - When breaking down larger tasks into smaller actionable steps
        - To give users visibility into your progress and planning

        When NOT to use:
        - Single, trivial tasks that can be completed in one step
        - Purely conversational/informational requests
        - When just reading files or performing simple searches

        CRITICAL workflow:
        1. Plan tasks by writing todo list with specific, actionable items
        2. Mark ONE todo as in-progress before starting work
        3. Complete the work for that specific todo
        4. Mark that todo as completed IMMEDIATELY
        5. Move to next todo and repeat

        Todo states:
        - not-started: Todo not yet begun
        - in-progress: Currently working (limit ONE at a time)
        - completed: Finished successfully

        IMPORTANT: Mark todos completed as soon as they are done. Do not batch completions.

        :param todo_list: Complete array of all todo items. Each item must have: id (number), title (string, 3-7 words), status (not-started|in-progress|completed). Example: [{"id": 1, "title": "Query API docs", "status": "completed"}, {"id": 2, "title": "Create board", "status": "in-progress"}]
        :return: Formatted todo list showing current progress
        """
        # Validate user
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        # Emit status update
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "updating",
                    "description": "Updating task list...",
                    "done": False
                }
            })

        # Validate and normalize todo items
        normalized_todos = []
        now = datetime.now().isoformat()
        existing_todos = {t["id"]: t for t in self._get_user_todos(user_id)}
        
        # Check for multiple in-progress items
        in_progress_count = sum(1 for t in todo_list if t.get("status") == "in-progress")
        if in_progress_count > 1 and __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "warning",
                    "description": f"Warning: {in_progress_count} tasks marked as in-progress. Recommend only 1 at a time.",
                    "done": False
                }
            })

        for item in todo_list:
            todo_id = item.get("id")
            title = item.get("title", "Untitled task")
            status = item.get("status", "not-started")
            
            # Validate status
            if status not in ["not-started", "in-progress", "completed"]:
                status = "not-started"
            
            # Preserve timestamps or create new ones
            existing = existing_todos.get(todo_id, {})
            created_at = existing.get("created_at", now)
            
            # Update timestamp if status changed
            if existing.get("status") != status:
                updated_at = now
            else:
                updated_at = existing.get("updated_at", now)
            
            normalized_todos.append({
                "id": todo_id,
                "title": title[:100],  # Limit title length
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            })

        # Check max todos limit
        if len(normalized_todos) > self.valves.MAX_TODOS:
            if self.valves.AUTO_CLEANUP_COMPLETED:
                # Remove oldest completed todos
                completed = [t for t in normalized_todos if t["status"] == "completed"]
                active = [t for t in normalized_todos if t["status"] != "completed"]
                
                # Keep most recent completed up to limit
                remaining_slots = self.valves.MAX_TODOS - len(active)
                if remaining_slots > 0:
                    completed = sorted(completed, key=lambda x: x["updated_at"], reverse=True)[:remaining_slots]
                else:
                    completed = []
                
                normalized_todos = active + completed
            else:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "error",
                            "description": f"Todo list exceeds maximum of {self.valves.MAX_TODOS} items.",
                            "done": True
                        }
                    })
                return json.dumps({"error": f"Todo list exceeds maximum of {self.valves.MAX_TODOS} items."}, ensure_ascii=False)

        # Store updated todos
        self._set_user_todos(user_id, normalized_todos)

        # Calculate stats
        total = len(normalized_todos)
        completed_count = sum(1 for t in normalized_todos if t["status"] == "completed")
        in_progress = sum(1 for t in normalized_todos if t["status"] == "in-progress")
        pending = sum(1 for t in normalized_todos if t["status"] == "not-started")

        # Emit completion status
        status_msg = f"Tasks: {completed_count}/{total} completed"
        if in_progress > 0:
            status_msg += f", {in_progress} in progress"
        if pending > 0:
            status_msg += f", {pending} pending"
            
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "updated",
                    "description": status_msg,
                    "done": True
                }
            })

        # Format and return the todo list
        show_timestamps = True
        if __user__:
            user_valves = __user__.get("valves")
            if user_valves:
                show_timestamps = getattr(user_valves, "SHOW_TIMESTAMPS", True)
            
        formatted_list = self._format_todo_list(normalized_todos, show_timestamps)
        
        return formatted_list

    async def get_todo_list(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Retrieve the current todo list to check progress and plan next steps.
        Use this to review what tasks are pending, in progress, or completed.

        :return: Formatted todo list showing all tasks and their status
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "fetching",
                    "description": "Retrieving task list...",
                    "done": False
                }
            })

        todos = self._get_user_todos(user_id)
        
        if not todos:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "empty",
                        "description": "No tasks in the todo list.",
                        "done": True
                    }
                })
            return "No tasks in the todo list. Use manage_todo_list to create tasks."

        # Calculate stats
        total = len(todos)
        completed_count = sum(1 for t in todos if t["status"] == "completed")
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "retrieved",
                    "description": f"Retrieved {total} tasks ({completed_count} completed)",
                    "done": True
                }
            })

        show_timestamps = True
        if __user__:
            user_valves = __user__.get("valves")
            if user_valves:
                show_timestamps = getattr(user_valves, "SHOW_TIMESTAMPS", True)

        return self._format_todo_list(todos, show_timestamps)

    async def clear_completed_todos(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Remove all completed tasks from the todo list.
        Use this to clean up after finishing a major milestone or starting fresh.

        :return: Confirmation message with count of removed tasks
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "clearing",
                    "description": "Clearing completed tasks...",
                    "done": False
                }
            })

        todos = self._get_user_todos(user_id)
        completed_count = sum(1 for t in todos if t["status"] == "completed")
        
        # Filter out completed todos
        active_todos = [t for t in todos if t["status"] != "completed"]
        self._set_user_todos(user_id, active_todos)

        message = f"Cleared {completed_count} completed tasks. {len(active_todos)} tasks remaining."
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "cleared",
                    "description": message,
                    "done": True
                }
            })

        return message

    async def reset_todo_list(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Clear all tasks and start with an empty todo list.
        Use this when starting a completely new workflow or project.

        :return: Confirmation that the todo list has been reset
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "resetting",
                    "description": "Resetting todo list...",
                    "done": False
                }
            })

        previous_count = len(self._get_user_todos(user_id))
        self._set_user_todos(user_id, [])

        message = f"Todo list reset. Removed {previous_count} tasks. Ready for new workflow."
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "reset",
                    "description": message,
                    "done": True
                }
            })

        return message

    async def update_single_todo(
        self,
        todo_id: int,
        status: str,
        title: Optional[str] = None,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Update a single todo item's status or title.
        Use this for quick status updates without resending the entire list.

        Common usage:
        - Mark a task as in-progress before starting work
        - Mark a task as completed after finishing
        - Update a task's title to be more specific

        :param todo_id: The ID of the todo item to update
        :param status: New status: 'not-started', 'in-progress', or 'completed'
        :param title: Optional new title for the todo
        :return: Confirmation and updated todo list
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        # Validate status
        if status not in ["not-started", "in-progress", "completed"]:
            return json.dumps({"error": f"Invalid status '{status}'. Use: not-started, in-progress, or completed"}, ensure_ascii=False)

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "updating",
                    "description": f"Updating task {todo_id}...",
                    "done": False
                }
            })

        todos = self._get_user_todos(user_id)
        
        # Find and update the todo
        todo_found = False
        now = datetime.now().isoformat()
        status_change = ""
        
        for todo in todos:
            if todo["id"] == todo_id:
                todo_found = True
                old_status = todo["status"]
                todo["status"] = status
                todo["updated_at"] = now
                if title:
                    todo["title"] = title[:100]
                
                status_change = f"{old_status} → {status}" if old_status != status else "unchanged"
                break

        if not todo_found:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "not_found",
                        "description": f"Todo with ID {todo_id} not found.",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Todo with ID {todo_id} not found."}, ensure_ascii=False)

        self._set_user_todos(user_id, todos)

        # Check for multiple in-progress
        in_progress_count = sum(1 for t in todos if t["status"] == "in-progress")
        warning = ""
        if in_progress_count > 1:
            warning = f" ⚠️ Warning: {in_progress_count} tasks now in-progress."

        message = f"Task {todo_id} updated ({status_change}).{warning}"
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "updated",
                    "description": message,
                    "done": True
                }
            })

        show_timestamps = True
        if __user__:
            user_valves = __user__.get("valves")
            if user_valves:
                show_timestamps = getattr(user_valves, "SHOW_TIMESTAMPS", True)

        formatted_list = self._format_todo_list(todos, show_timestamps)
        return f"{message}\n\n{formatted_list}"

    async def add_todo(
        self,
        title: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Add a new todo item to the list.
        The new todo will be assigned the next available ID and start with 'not-started' status.

        :param title: Concise action-oriented task description (3-7 words recommended)
        :return: Confirmation and updated todo list
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "adding",
                    "description": "Adding new task...",
                    "done": False
                }
            })

        todos = self._get_user_todos(user_id)
        
        # Check max limit
        if len(todos) >= self.valves.MAX_TODOS:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "limit_reached",
                        "description": f"Cannot add more tasks. Maximum of {self.valves.MAX_TODOS} reached.",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Cannot add more tasks. Maximum of {self.valves.MAX_TODOS} reached."}, ensure_ascii=False)

        # Generate next ID
        next_id = max([t["id"] for t in todos], default=0) + 1
        now = datetime.now().isoformat()
        
        new_todo = {
            "id": next_id,
            "title": title[:100],
            "status": "not-started",
            "created_at": now,
            "updated_at": now,
        }
        
        todos.append(new_todo)
        self._set_user_todos(user_id, todos)

        display_title = f"'{title[:50]}...'" if len(title) > 50 else f"'{title}'"
        message = f"Added task {next_id}: {display_title}"
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "added",
                    "description": message,
                    "done": True
                }
            })

        show_timestamps = True
        if __user__:
            user_valves = __user__.get("valves")
            if user_valves:
                show_timestamps = getattr(user_valves, "SHOW_TIMESTAMPS", True)

        formatted_list = self._format_todo_list(todos, show_timestamps)
        return f"{message}\n\n{formatted_list}"
