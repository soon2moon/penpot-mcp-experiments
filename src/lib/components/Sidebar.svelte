<script>
import Drawer, { Content } from '@smui/drawer';
  import List, { Item, Text, Graphic, Separator } from '@smui/list';
  
  export let active = 'Home';
  
  const menuItems = [
    { id: 'Home', icon: 'home', label: 'Home', href: '/' },
    { id: 'Search', icon: 'search', label: 'Search', href: '/search' },
    { id: 'Library', icon: 'library_music', label: 'Your Library', href: '/library' },
    { id: 'Settings', icon: 'settings', label: 'Settings', href: '/settings/all' }
  ];
  
  const actionItems = [
    { id: 'create', icon: 'add_box', label: 'Create Playlist', href: '/playlist/new' },
    { id: 'liked', icon: 'query_stats', label: 'Listening stats', href: '/liked' }
  ];
  
</script>

<div class="sidebar-wrapper">
  <Drawer variant="permanent" class="light-drawer">
    <Content>
      <List>
        {#each menuItems as item (item.id)}
          <Item href={item.href} activated={active === item.id}>
            <Graphic class="material-icons" aria-hidden="true">{item.icon}</Graphic>
            <Text>{item.label}</Text>
          </Item>
        {/each}

        <Separator />
        
        {#each actionItems as item (item.id)}
          <Item href={item.href} activated={active === item.id}>
            <Graphic class="material-icons" aria-hidden="true">{item.icon}</Graphic>
            <Text>{item.label}</Text>
          </Item>
        {/each}
      </List>
    </Content>
  </Drawer>
</div>

<style>
  .sidebar-wrapper {
    height: 100%;
    background-color: #ffffff;
  }
  
  /* Force light theme for drawer */
  :global(.light-drawer.mdc-drawer) {
    background-color: #ffffff !important;
    color: #212121 !important;
    border: none !important;
    position: static;
    width: 100%;
    height: 100%;
    box-shadow: none !important;
  }

  :global(.light-drawer .mdc-drawer__content) {
    height: 100%;
  }
  
  :global(.light-drawer .mdc-drawer__header) {
    display: none;
  }
  
  :global(.light-drawer .mdc-drawer__content) {
    background-color: #ffffff;
  }
  
  :global(.light-drawer .mdc-deprecated-list) {
    padding: 0.5rem 0.5rem;
  }
  
  :global(.light-drawer .mdc-deprecated-list-item) {
    color: #212121 !important;
    border-radius: 8px;
    margin: 2px 0;
    height: 48px;
    padding: 0 1rem;
  }
  
  :global(.light-drawer .mdc-deprecated-list-item:hover) {
    background-color: #f5f5f5 !important;
  }
  
  :global(.light-drawer .mdc-deprecated-list-item--activated) {
    background-color: #e8f5e9 !important;
    color: #1db954 !important;
  }
  
  :global(.light-drawer .mdc-deprecated-list-item--activated .material-icons) {
    color: #1db954 !important;
  }
  
  :global(.light-drawer .material-icons) {
    color: #757575 !important;
  }
  
  :global(.light-drawer .mdc-deprecated-list-item__text) {
    color: inherit !important;
  }
  
  :global(.light-drawer .mdc-deprecated-list-divider) {
    background-color: #e0e0e0;
    margin: 0.5rem 0;
  }
</style>
