<script lang="ts">
  import { page } from '$app/stores';

  let { children } = $props();

  const activeTab = $derived.by(() => {
    const pathname = $page.url.pathname;
    if (pathname.startsWith('/settings/all')) return 'all';
    if (pathname.startsWith('/settings/user')) return 'user';
    if (pathname.startsWith('/settings/accounts')) return 'accounts';
    return 'profile';
  });
</script>

<div class="settings-shell">
  <header class="settings-header">
    <h1>Settings</h1>
    <p>Manage your profile and preferences.</p>
  </header>

  <nav class="settings-tabs" aria-label="Settings sections">
    <a href="/settings/all" class:active={activeTab === 'all'}>All settings</a>
    <a href="/settings/profile" class:active={activeTab === 'profile'}>User profile</a>
    <a href="/settings/user" class:active={activeTab === 'user'}>User settings</a>
    <a href="/settings/accounts" class:active={activeTab === 'accounts'}>Manage accounts</a>
  </nav>

  <section class="settings-content">
    {@render children()}
  </section>
</div>

<style>
  .settings-shell {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .settings-header h1 {
    margin: 0;
    font-size: 1.8rem;
  }

  .settings-header p {
    margin: 4px 0 0;
    color: #6b6b6b;
  }

  .settings-tabs {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .settings-tabs a {
    text-decoration: none;
    color: #212121;
    border: 1px solid #e0e0e0;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
  }

  .settings-tabs a.active {
    background: #1db954;
    border-color: #1db954;
    color: #ffffff;
  }

  .settings-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
</style>
