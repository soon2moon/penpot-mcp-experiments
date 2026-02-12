<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import Player from '$lib/components/Player.svelte';
	import { page } from '$app/stores';

	let { children } = $props();
	const activeSection = $derived.by(() => {
		const pathname = $page.url.pathname;
		if (pathname === '/' || pathname === '') return 'Home';
		if (pathname.startsWith('/search')) return 'Search';
		if (pathname.startsWith('/library')) return 'Library';
		if (pathname.startsWith('/settings')) return 'Settings';
		if (pathname.startsWith('/playlist')) return 'create';
		if (pathname.startsWith('/liked')) return 'liked';
		return 'Home';
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link
		href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
		rel="stylesheet"
	/>
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
	<link rel="stylesheet" href="/smui.css" />
</svelte:head>

<div class="app-container light-theme">
  <header class="top-bar">
    <Navbar />
  </header>

  <aside class="sidebar-area">
    <Sidebar active={activeSection} />
  </aside>
  
  <main class="main-area">
    <div class="content-scroll">
      {@render children()}
    </div>
  </main>
  
  <footer class="player-area">
    <Player />
  </footer>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Roboto', sans-serif;
    background-color: #eef1f4;
    color: #212121;
  }
  
  .app-container {
    display: grid;
    grid-template-columns: 240px 1fr;
    grid-template-rows: 90px 1fr 90px;
    gap: 20px;
    padding: 20px 20px 20px 28px;
    height: 100vh;
    box-sizing: border-box;
    overflow: hidden;
    background-color: #eef1f4;
  }
  
  /* Force light theme */
  .light-theme {
    --mdc-theme-primary: #1db954;
    --mdc-theme-secondary: #1976d2;
    --mdc-theme-background: #fafafa;
    --mdc-theme-surface: #ffffff;
    --mdc-theme-on-primary: #ffffff;
    --mdc-theme-on-secondary: #ffffff;
    --mdc-theme-on-surface: #212121;
    --mdc-theme-on-background: #212121;
    --mdc-theme-text-primary-on-background: #212121;
    --mdc-theme-text-secondary-on-background: #757575;
  }
  
  .top-bar {
    grid-column: 1 / -1;
    grid-row: 1;
  }

  .sidebar-area {
    grid-column: 1;
    grid-row: 2;
    background-color: #ffffff;
    border-radius: 16px;
    z-index: 2;
    overflow-y: auto;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    min-height: 0;
  }
  
  .main-area {
    grid-column: 2;
    grid-row: 2;
    display: flex;
    flex-direction: column;
    overflow: visible;
    background-color: #f7f8fa;
    border-radius: 16px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    min-height: 0;
  }
  
  .content-scroll {
    flex: 1;
    overflow-y: auto;
    overflow-x: visible;
    min-height: 0;
    padding: 1.5rem;
    padding-bottom: 2.5rem;
    background-color: transparent;
  }
  
  .player-area {
    grid-column: 1 / -1;
    grid-row: 3;
    background-color: transparent;
    z-index: 10;
    box-shadow: none;
    display: flex;
    align-items: center;
  }
  
  :global(h1) {
    font-weight: 300;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
    color: #212121;
  }
  
  :global(h2) {
    margin-top: 1.875rem;
    margin-bottom: 0.938rem;
    font-weight: 500;
    font-size: 1.25rem;
    color: #212121;
  }
</style>
