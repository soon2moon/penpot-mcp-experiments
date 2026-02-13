"""
title: Memory Enhancement Tool for LLM Reasoning
author: Victor Vibe
author_url: https://github.com/soon2moon/penpot-mcp-experiments
description: Enhances memory capabilities with structured variable declaration to help smaller models (32B) achieve reasoning quality comparable to larger models (70B+). Forces explicit state management and prevents undefined variable errors.
required_open_webui_version: 0.4.0
version: 0.1.0
license: MIT

This tool enhances Open WebUI's native memory capabilities by:
1. Enforcing structured variable/entity declaration at reasoning start
2. Providing semantic memory search with context awareness
3. Managing memory lifecycle (add, update, delete) with validation
4. Tracking declared state to prevent undefined reference errors

Usage in system prompts:
<structuredReasoning>
BEFORE starting any complex task, you MUST use the declare_reasoning_context tool to:
1. Declare all entities/variables you will reference
2. Define their types and initial values
3. Establish relationships between entities

This declaration phase prevents undefined variable errors and ensures consistent
state management throughout your reasoning process.

MANDATORY WORKFLOW:
1. DECLARE: Call declare_reasoning_context with all planned entities
2. VALIDATE: Use validate_context to check declarations before proceeding
3. EXECUTE: Perform reasoning steps, updating context as needed
4. COMMIT: Save important facts to persistent memory using add_memory_enhanced
</structuredReasoning>

Thanks to https://github.com/soymh and https://github.com/CookSleep for the
foundational memory tool implementation patterns.
"""

import json
from datetime import datetime
from typing import Callable, Any, List, Optional, Dict
from pydantic import BaseModel, Field

# Open WebUI internal imports for memory access
try:
    from open_webui.models.memories import Memories
    MEMORIES_AVAILABLE = True
except ImportError:
    MEMORIES_AVAILABLE = False


class Tools:
    """
    Memory Enhancement Tool that combines Open WebUI's native memory capabilities
    with structured variable declaration to improve reasoning quality for smaller models.
    
    Key Features:
    - Structured reasoning context with explicit variable declarations
    - Semantic memory search across user's personalization bank
    - Memory lifecycle management (CRUD operations)
    - Validation to prevent undefined variable errors
    - State tracking for complex multi-step reasoning
    """
    
    class Valves(BaseModel):
        ENABLE_MEMORY_OPS: bool = Field(
            default=True, 
            description="Enable memory read/write operations."
        )
        MAX_MEMORIES_PER_SEARCH: int = Field(
            default=10,
            description="Maximum number of memories to return per search."
        )
        REQUIRE_DECLARATION: bool = Field(
            default=True,
            description="Require variable declaration before use in reasoning."
        )
        AUTO_SAVE_CONTEXT: bool = Field(
            default=False,
            description="Automatically save reasoning context to memory after completion."
        )
        DEBUG: bool = Field(
            default=False, 
            description="Enable debug logging."
        )

    class UserValves(BaseModel):
        SHOW_MEMORY_IDS: bool = Field(
            default=False,
            description="Show memory IDs in search results (useful for updates)."
        )
        AUTO_RECALL_ON_START: bool = Field(
            default=True,
            description="Automatically recall related memories when starting a task."
        )

    def __init__(self):
        """Initialize the Tool."""
        self.valves = self.Valves()
        # In-memory storage for reasoning context (per-session, per-user)
        self._reasoning_contexts: Dict[str, Dict] = {}

    def _get_user_context(self, user_id: str) -> Dict:
        """Get or create reasoning context for a user."""
        if user_id not in self._reasoning_contexts:
            self._reasoning_contexts[user_id] = {
                "declared_entities": {},
                "entity_types": {},
                "relationships": [],
                "state_history": [],
                "created_at": datetime.now().isoformat(),
                "last_validated": None,
            }
        return self._reasoning_contexts[user_id]

    def _validate_entity_exists(self, user_id: str, entity_name: str) -> bool:
        """Check if an entity has been declared in the current context."""
        context = self._get_user_context(user_id)
        return entity_name in context["declared_entities"]

    # =========================================================================
    # STRUCTURED REASONING CONTEXT MANAGEMENT
    # =========================================================================

    async def declare_reasoning_context(
        self,
        entities: List[Dict],
        task_description: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        MANDATORY: Declare all entities/variables before starting any complex reasoning task.
        This prevents undefined variable errors and ensures consistent state management.

        Call this FIRST before any other reasoning operations. Declare every entity,
        variable, or concept you plan to reference during your reasoning process.

        Entity structure:
        {
            "name": "unique_identifier",
            "type": "string|number|boolean|object|array|reference",
            "value": <initial_value>,
            "description": "What this entity represents"
        }

        Example entities for a Penpot design task:
        [
            {"name": "board", "type": "reference", "value": null, "description": "The main board container"},
            {"name": "header_text", "type": "object", "value": {"content": "Title", "fontSize": 24}, "description": "Header text element"},
            {"name": "primary_color", "type": "string", "value": "#1976D2", "description": "Primary brand color"}
        ]

        :param entities: List of entity declarations with name, type, value, and description
        :param task_description: Brief description of the reasoning task being performed
        :return: Confirmation of declared entities and validation status
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "declaring",
                    "description": f"Declaring {len(entities)} entities for reasoning context...",
                    "done": False
                }
            })

        context = self._get_user_context(user_id)
        now = datetime.now().isoformat()
        
        # Record the task
        context["task_description"] = task_description
        context["declaration_time"] = now
        
        # Process entity declarations
        declared = []
        errors = []
        
        for entity in entities:
            name = entity.get("name")
            if not name:
                errors.append("Entity missing 'name' field")
                continue
            
            # Validate name format (alphanumeric + underscore)
            if not name.replace("_", "").isalnum():
                errors.append(f"Invalid entity name '{name}': use alphanumeric and underscores only")
                continue
            
            entity_type = entity.get("type", "object")
            value = entity.get("value")
            description = entity.get("description", "")
            
            # Store the declaration
            context["declared_entities"][name] = {
                "type": entity_type,
                "value": value,
                "description": description,
                "declared_at": now,
                "last_modified": now,
                "modification_count": 0,
            }
            context["entity_types"][name] = entity_type
            
            declared.append(f"  • {name}: {entity_type}" + (f" = {json.dumps(value)}" if value is not None else ""))

        # Record state history
        context["state_history"].append({
            "action": "declare",
            "timestamp": now,
            "entities_declared": len(declared),
            "errors": len(errors),
        })

        if __event_emitter__:
            status_msg = f"Declared {len(declared)} entities"
            if errors:
                status_msg += f" ({len(errors)} errors)"
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "declared",
                    "description": status_msg,
                    "done": True
                }
            })

        # Format response
        result_lines = [
            f"## Reasoning Context Declared",
            f"**Task:** {task_description}",
            f"**Declared Entities ({len(declared)}):**",
        ]
        result_lines.extend(declared)
        
        if errors:
            result_lines.append(f"\n**⚠️ Declaration Errors ({len(errors)}):**")
            for err in errors:
                result_lines.append(f"  • {err}")
        
        result_lines.append(f"\n✅ Context ready. You may now proceed with reasoning.")
        result_lines.append(f"💡 Use `update_entity` to modify values, `validate_context` to check state.")
        
        return "\n".join(result_lines)

    async def validate_context(
        self,
        entity_names: Optional[List[str]] = None,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Validate that all required entities are declared before proceeding.
        Call this before using entities in your reasoning to catch undefined references early.

        If entity_names is provided, validates only those specific entities.
        If entity_names is None, returns the full context state.

        :param entity_names: Optional list of entity names to validate (None = show all)
        :return: Validation result with current state of entities
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        context = self._get_user_context(user_id)
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "validating",
                    "description": "Validating reasoning context...",
                    "done": False
                }
            })

        declared = context.get("declared_entities", {})
        now = datetime.now().isoformat()
        context["last_validated"] = now
        
        if not declared:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "empty",
                        "description": "No entities declared yet.",
                        "done": True
                    }
                })
            return (
                "⚠️ **No reasoning context declared.**\n\n"
                "You must call `declare_reasoning_context` before proceeding.\n"
                "Declare all entities, variables, and references you will use."
            )

        # Validate specific entities or show all
        if entity_names:
            valid = []
            undefined = []
            for name in entity_names:
                if name in declared:
                    entity = declared[name]
                    valid.append(f"  ✅ {name}: {entity['type']} = {json.dumps(entity['value'])}")
                else:
                    undefined.append(f"  ❌ {name}: UNDEFINED")
            
            if undefined:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "invalid",
                            "description": f"{len(undefined)} undefined entities found!",
                            "done": True
                        }
                    })
                return (
                    f"## ❌ Validation FAILED\n\n"
                    f"**Undefined Entities ({len(undefined)}):**\n"
                    + "\n".join(undefined) +
                    f"\n\n**Valid Entities ({len(valid)}):**\n"
                    + "\n".join(valid) +
                    "\n\n⚠️ Declare missing entities before using them!"
                )
            else:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "valid",
                            "description": f"All {len(valid)} entities validated.",
                            "done": True
                        }
                    })
                return (
                    f"## ✅ Validation PASSED\n\n"
                    f"**All Requested Entities Valid ({len(valid)}):**\n"
                    + "\n".join(valid)
                )
        else:
            # Show full context
            lines = [
                f"## Current Reasoning Context",
                f"**Task:** {context.get('task_description', 'Not specified')}",
                f"**Declared at:** {context.get('declaration_time', 'N/A')}",
                f"**Last validated:** {now}",
                f"\n**Declared Entities ({len(declared)}):**"
            ]
            
            for name, entity in declared.items():
                value_str = json.dumps(entity['value']) if entity['value'] is not None else "null"
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
                lines.append(f"  • {name} ({entity['type']}): {value_str}")
                if entity.get('description'):
                    lines.append(f"    _{entity['description']}_")
            
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "validated",
                        "description": f"Context has {len(declared)} entities.",
                        "done": True
                    }
                })
            
            return "\n".join(lines)

    async def update_entity(
        self,
        entity_name: str,
        new_value: Any,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Update the value of a previously declared entity.
        Use this to track state changes during your reasoning process.

        The entity must have been declared first using declare_reasoning_context.

        :param entity_name: Name of the entity to update
        :param new_value: New value for the entity
        :return: Confirmation of update with old and new values
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        context = self._get_user_context(user_id)
        declared = context.get("declared_entities", {})
        
        if entity_name not in declared:
            available = list(declared.keys())[:10]
            return (
                f"❌ **Entity '{entity_name}' is not declared.**\n\n"
                f"You must declare entities before using them.\n"
                f"Available entities: {', '.join(available) if available else 'None'}\n\n"
                f"Call `declare_reasoning_context` to declare new entities."
            )

        entity = declared[entity_name]
        old_value = entity["value"]
        now = datetime.now().isoformat()
        
        # Update the entity
        entity["value"] = new_value
        entity["last_modified"] = now
        entity["modification_count"] = entity.get("modification_count", 0) + 1
        
        # Record in state history
        context["state_history"].append({
            "action": "update",
            "entity": entity_name,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": now,
        })

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "updated",
                    "description": f"Entity '{entity_name}' updated.",
                    "done": True
                }
            })

        old_str = json.dumps(old_value) if old_value is not None else "null"
        new_str = json.dumps(new_value) if new_value is not None else "null"
        
        # Truncate long values for display
        if len(old_str) > 50:
            old_str = old_str[:47] + "..."
        if len(new_str) > 50:
            new_str = new_str[:47] + "..."
        
        return (
            f"✅ **Entity Updated**\n"
            f"**{entity_name}** ({entity['type']})\n"
            f"  Old: {old_str}\n"
            f"  New: {new_str}\n"
            f"  Modifications: {entity['modification_count']}"
        )

    async def clear_context(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Clear the current reasoning context and start fresh.
        Use this when switching to a completely different task.

        :return: Confirmation that context was cleared
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        user_id = __user__.get("id", "anonymous")
        
        if user_id in self._reasoning_contexts:
            previous_entities = len(self._reasoning_contexts[user_id].get("declared_entities", {}))
            del self._reasoning_contexts[user_id]
        else:
            previous_entities = 0

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "cleared",
                    "description": f"Context cleared ({previous_entities} entities removed).",
                    "done": True
                }
            })

        return f"✅ Reasoning context cleared. {previous_entities} entities removed.\n\nUse `declare_reasoning_context` to start a new task."

    # =========================================================================
    # MEMORY OPERATIONS (using Open WebUI's native Memories API)
    # =========================================================================

    async def search_memories(
        self,
        query: str,
        count: int = 5,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Search the user's personal memory bank for relevant information.
        Use this to recall previously stored facts, preferences, or context.

        This wraps Open WebUI's native memory search with enhanced formatting.

        :param query: Search query to find related memories
        :param count: Maximum number of memories to return (default: 5, max: 20)
        :return: List of matching memories with their content
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        if not MEMORIES_AVAILABLE:
            return json.dumps({"error": "Memory system not available. Ensure Open WebUI's Memories module is accessible."}, ensure_ascii=False)

        if not self.valves.ENABLE_MEMORY_OPS:
            return json.dumps({"error": "Memory operations are disabled in tool configuration."}, ensure_ascii=False)

        user_id = __user__.get("id")
        if not user_id:
            return json.dumps({"error": "User ID not found."}, ensure_ascii=False)

        # Clamp count to reasonable limits
        count = min(max(1, count), min(20, self.valves.MAX_MEMORIES_PER_SEARCH))

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "searching",
                    "description": f"Searching memories for: '{query[:30]}...'",
                    "done": False
                }
            })

        try:
            # Get all user memories and filter by query
            # Note: Open WebUI's native search_memories uses vector similarity
            # Here we're doing a simpler text-based search as fallback
            user_memories = Memories.get_memories_by_user_id(user_id)
            
            if not user_memories:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "empty",
                            "description": "No memories stored yet.",
                            "done": True
                        }
                    })
                return "No memories found. Use `add_memory_enhanced` to store new facts."

            # Simple relevance scoring based on query term matching
            query_terms = query.lower().split()
            scored_memories = []
            
            for memory in user_memories:
                content_lower = memory.content.lower()
                score = sum(1 for term in query_terms if term in content_lower)
                if score > 0:
                    scored_memories.append((score, memory))

            # Sort by score (descending) and take top results
            scored_memories.sort(key=lambda x: x[0], reverse=True)
            results = scored_memories[:count]

            if not results:
                # Fallback: return most recent memories if no matches
                sorted_memories = sorted(user_memories, key=lambda m: m.created_at, reverse=True)
                results = [(0, m) for m in sorted_memories[:count]]
                fallback_msg = "(No exact matches, showing recent memories)"
            else:
                fallback_msg = ""

            # Check user preference for showing IDs
            show_ids = False
            if __user__:
                user_valves = __user__.get("valves")
                if user_valves:
                    show_ids = getattr(user_valves, "SHOW_MEMORY_IDS", False)

            # Format results
            lines = [f"## Memory Search Results{' ' + fallback_msg if fallback_msg else ''}"]
            lines.append(f"**Query:** {query}")
            lines.append(f"**Found:** {len(results)} memories\n")

            for idx, (score, memory) in enumerate(results, 1):
                content = memory.content
                if len(content) > 200:
                    content = content[:197] + "..."
                
                if show_ids:
                    lines.append(f"{idx}. [{memory.id}] {content}")
                else:
                    lines.append(f"{idx}. {content}")

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "found",
                        "description": f"Found {len(results)} relevant memories.",
                        "done": True
                    }
                })

            return "\n".join(lines)

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Memory search failed: {str(e)}",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Memory search failed: {str(e)}"}, ensure_ascii=False)

    async def add_memory_enhanced(
        self,
        content: str,
        category: Optional[str] = None,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Store a new fact in the user's personal memory bank.
        Use this to save important information that should persist across conversations.

        Best practices for memory content:
        - Be specific and concise
        - Include context (e.g., "User prefers Python for backend development")
        - Use consistent formatting for related facts
        - Avoid storing temporary or session-specific information

        :param content: The fact or information to remember (be specific and concise)
        :param category: Optional category prefix (e.g., "preference", "project", "skill")
        :return: Confirmation that the memory was stored
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        if not MEMORIES_AVAILABLE:
            return json.dumps({"error": "Memory system not available."}, ensure_ascii=False)

        if not self.valves.ENABLE_MEMORY_OPS:
            return json.dumps({"error": "Memory operations are disabled."}, ensure_ascii=False)

        user_id = __user__.get("id")
        if not user_id:
            return json.dumps({"error": "User ID not found."}, ensure_ascii=False)

        # Validate content
        if not content or len(content.strip()) < 3:
            return json.dumps({"error": "Memory content too short. Provide meaningful information."}, ensure_ascii=False)

        if len(content) > 1000:
            content = content[:1000]  # Truncate to reasonable length

        # Add category prefix if provided
        if category:
            formatted_content = f"[{category.upper()}] {content}"
        else:
            formatted_content = content

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "storing",
                    "description": "Storing new memory...",
                    "done": False
                }
            })

        try:
            new_memory = Memories.insert_new_memory(user_id, formatted_content)
            
            if new_memory:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "stored",
                            "description": "Memory stored successfully.",
                            "done": True
                        }
                    })
                
                preview = formatted_content[:80] + "..." if len(formatted_content) > 80 else formatted_content
                return (
                    f"✅ **Memory Stored**\n"
                    f"**Content:** {preview}\n"
                    f"**Memory ID:** {new_memory.id}\n\n"
                    f"Use `search_memories` to retrieve this later."
                )
            else:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "failed",
                            "description": "Failed to store memory.",
                            "done": True
                        }
                    })
                return json.dumps({"error": "Failed to store memory."}, ensure_ascii=False)

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Memory storage failed: {str(e)}",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Memory storage failed: {str(e)}"}, ensure_ascii=False)

    async def update_memory(
        self,
        memory_id: str,
        new_content: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Update an existing memory record with new content.
        Use this to correct or update previously stored information.

        You need the memory_id which can be obtained from search results
        (enable SHOW_MEMORY_IDS in user preferences) or from the recall_all_memories output.

        :param memory_id: The unique ID of the memory to update
        :param new_content: The updated content for the memory
        :return: Confirmation of the update
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        if not MEMORIES_AVAILABLE:
            return json.dumps({"error": "Memory system not available."}, ensure_ascii=False)

        if not self.valves.ENABLE_MEMORY_OPS:
            return json.dumps({"error": "Memory operations are disabled."}, ensure_ascii=False)

        user_id = __user__.get("id")
        if not user_id:
            return json.dumps({"error": "User ID not found."}, ensure_ascii=False)

        if not new_content or len(new_content.strip()) < 3:
            return json.dumps({"error": "Memory content too short."}, ensure_ascii=False)

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "updating",
                    "description": f"Updating memory {memory_id[:8]}...",
                    "done": False
                }
            })

        try:
            updated_memory = Memories.update_memory_by_id(memory_id, new_content)
            
            if updated_memory:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "updated",
                            "description": "Memory updated successfully.",
                            "done": True
                        }
                    })
                
                preview = new_content[:80] + "..." if len(new_content) > 80 else new_content
                return f"✅ **Memory Updated**\n**ID:** {memory_id}\n**New Content:** {preview}"
            else:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "not_found",
                            "description": f"Memory {memory_id} not found.",
                            "done": True
                        }
                    })
                return json.dumps({"error": f"Memory with ID '{memory_id}' not found."}, ensure_ascii=False)

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Update failed: {str(e)}",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Memory update failed: {str(e)}"}, ensure_ascii=False)

    async def delete_memory(
        self,
        memory_id: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Delete a memory record from the user's memory bank.
        Use this to remove outdated, incorrect, or unwanted memories.

        :param memory_id: The unique ID of the memory to delete
        :return: Confirmation of the deletion
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        if not MEMORIES_AVAILABLE:
            return json.dumps({"error": "Memory system not available."}, ensure_ascii=False)

        if not self.valves.ENABLE_MEMORY_OPS:
            return json.dumps({"error": "Memory operations are disabled."}, ensure_ascii=False)

        user_id = __user__.get("id")
        if not user_id:
            return json.dumps({"error": "User ID not found."}, ensure_ascii=False)

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "deleting",
                    "description": f"Deleting memory {memory_id[:8]}...",
                    "done": False
                }
            })

        try:
            result = Memories.delete_memory_by_id(memory_id)
            
            if result:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "deleted",
                            "description": "Memory deleted successfully.",
                            "done": True
                        }
                    })
                return f"✅ **Memory Deleted**\n**ID:** {memory_id}"
            else:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "not_found",
                            "description": f"Memory {memory_id} not found.",
                            "done": True
                        }
                    })
                return json.dumps({"error": f"Memory with ID '{memory_id}' not found or already deleted."}, ensure_ascii=False)

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Deletion failed: {str(e)}",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Memory deletion failed: {str(e)}"}, ensure_ascii=False)

    async def recall_all_memories(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Retrieve ALL stored memories from the user's memory bank.
        Use this to get a complete picture of what has been stored about the user.

        Returns a numbered list of all memories with their IDs for easy reference.

        :return: Complete list of all stored memories
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        if not MEMORIES_AVAILABLE:
            return json.dumps({"error": "Memory system not available."}, ensure_ascii=False)

        user_id = __user__.get("id")
        if not user_id:
            return json.dumps({"error": "User ID not found."}, ensure_ascii=False)

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "recalling",
                    "description": "Retrieving all memories...",
                    "done": False
                }
            })

        try:
            user_memories = Memories.get_memories_by_user_id(user_id)
            
            if not user_memories:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "empty",
                            "description": "No memories stored.",
                            "done": True
                        }
                    })
                return "No memories stored yet. Use `add_memory_enhanced` to store new facts."

            # Sort by creation date
            sorted_memories = sorted(user_memories, key=lambda m: m.created_at)
            
            lines = [
                "## All Stored Memories",
                f"**Total:** {len(sorted_memories)} memories\n"
            ]
            
            for idx, memory in enumerate(sorted_memories, 1):
                # Include ID for update/delete operations
                lines.append(f"{idx}. **[{memory.id}]** {memory.content}")

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "recalled",
                        "description": f"Retrieved {len(sorted_memories)} memories.",
                        "done": True
                    }
                })

            lines.append("\n_Use memory IDs with `update_memory` or `delete_memory` to manage entries._")
            
            return "\n".join(lines)

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Recall failed: {str(e)}",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Memory recall failed: {str(e)}"}, ensure_ascii=False)

    # =========================================================================
    # COMMIT REASONING CONTEXT TO MEMORY
    # =========================================================================

    async def commit_context_to_memory(
        self,
        summary: str,
        entities_to_save: Optional[List[str]] = None,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Save the current reasoning context (or selected entities) to persistent memory.
        Use this at the end of a reasoning task to preserve important conclusions.

        :param summary: A brief summary of what was accomplished
        :param entities_to_save: Optional list of entity names to save (None = save all with non-null values)
        :return: Confirmation of what was saved to memory
        """
        if not __user__:
            return json.dumps({"error": "User context not provided."}, ensure_ascii=False)

        if not MEMORIES_AVAILABLE:
            return json.dumps({"error": "Memory system not available."}, ensure_ascii=False)

        user_id = __user__.get("id")
        if not user_id:
            return json.dumps({"error": "User ID not found."}, ensure_ascii=False)

        context = self._get_user_context(user_id)
        declared = context.get("declared_entities", {})
        
        if not declared:
            return json.dumps({"error": "No reasoning context to save. Declare entities first."}, ensure_ascii=False)

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "status": "committing",
                    "description": "Saving context to memory...",
                    "done": False
                }
            })

        # Determine which entities to save
        if entities_to_save:
            to_save = {name: declared[name] for name in entities_to_save if name in declared}
        else:
            to_save = {name: entity for name, entity in declared.items() if entity["value"] is not None}

        if not to_save:
            return "No entities with values to save."

        # Create memory content
        task_desc = context.get("task_description", "Reasoning task")
        now = datetime.now().isoformat()[:16]
        
        memory_content = f"[CONTEXT:{now}] {summary}\n"
        memory_content += f"Task: {task_desc}\n"
        memory_content += "Entities:\n"
        
        for name, entity in to_save.items():
            value_str = json.dumps(entity["value"])
            if len(value_str) > 100:
                value_str = value_str[:97] + "..."
            memory_content += f"  - {name} ({entity['type']}): {value_str}\n"

        try:
            new_memory = Memories.insert_new_memory(user_id, memory_content)
            
            if new_memory:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "committed",
                            "description": f"Saved {len(to_save)} entities to memory.",
                            "done": True
                        }
                    })
                return (
                    f"✅ **Context Committed to Memory**\n"
                    f"**Summary:** {summary}\n"
                    f"**Entities Saved:** {len(to_save)}\n"
                    f"**Memory ID:** {new_memory.id}\n\n"
                    f"Saved: {', '.join(to_save.keys())}"
                )
            else:
                return json.dumps({"error": "Failed to save context to memory."}, ensure_ascii=False)

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Commit failed: {str(e)}",
                        "done": True
                    }
                })
            return json.dumps({"error": f"Failed to commit context: {str(e)}"}, ensure_ascii=False)
