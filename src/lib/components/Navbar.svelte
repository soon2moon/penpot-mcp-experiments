<script>
  import IconButton from '@smui/icon-button';
  import Select, { Option } from '@smui/select';

  let accountOption = 'account';
</script>

<nav class="navbar">
  <div class="nav-left">
    <div class="brand">
      <span class="material-icons brand-icon">graphic_eq</span>
      <span class="brand-text">Spoti-Svelte</span>
    </div>
  </div>
  
  <div class="nav-center">
    <button class="home-pill" aria-label="Home">
      <span class="material-icons">home</span>
    </button>
    <div class="search-pill">
      <span class="material-icons">search</span>
      <input type="text" placeholder="What do you want to play?" />
      <span class="divider"></span>
      <span class="material-icons">inventory_2</span>
    </div>
  </div>

  <div class="nav-right">
    <div class="account-select">
      <span class="material-icons account-icon">account_circle</span>
      <Select
        class="account-field"
        variant="outlined"
        bind:value={accountOption}
        aria-label="Account"
      >
        <Option value="account">Account</Option>
        <Option value="profile">Profile</Option>
        <Option value="settings">Settings</Option>
        <Option value="signout">Sign out</Option>
      </Select>
    </div>
    <IconButton class="material-icons nav-btn" aria-label="Notifications">notifications</IconButton>
  </div>
</nav>

<style>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background-color: #ffffff;
    border-radius: 18px;
    height: 100%;
    color: #212121;
    border: 1px solid #e6e6e6;
    box-sizing: border-box;
  }
  
  .nav-left,
  .nav-right {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    font-size: 1.1rem;
    color: #212121;
    padding-left: 24px;
  }

  .brand-icon {
    font-size: 22px;
    color: #1db954;
  }

  .brand-text {
    letter-spacing: -0.3px;
  }

  .nav-center {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 0 12px;
  }

  .home-pill {
    width: 36px;
    height: 36px;
    border-radius: 999px;
    border: none;
    background: #f0f0f0;
    color: #212121;
    display: grid;
    place-items: center;
    cursor: pointer;
  }

  .search-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 999px;
    background: #f0f0f0;
    width: min(540px, 100%);
  }

  .search-pill input {
    flex: 1;
    border: none;
    background: transparent;
    color: #212121;
    font-size: 0.9rem;
    outline: none;
  }

  .search-pill input::placeholder {
    color: #8b8b8b;
  }

  .search-pill .divider {
    width: 1px;
    height: 20px;
    background: #d0d0d0;
  }

  .account-select {
    position: relative;
    display: flex;
    align-items: center;
  }

  .account-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    color: #5b5b5b;
    pointer-events: none;
    z-index: 2;
  }

  :global(.account-select .mdc-select) {
    width: 190px;
  }

  :global(.account-select .mdc-select__anchor) {
    height: 44px;
    padding-left: 40px;
  }

  :global(.account-select .mdc-floating-label) {
    padding-left: 4px;
  }

  .premium-btn {
    border: none;
    background: #111111;
    color: #ffffff;
    border-radius: 999px;
    padding: 6px 14px;
    font-weight: 600;
    cursor: pointer;
  }

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #e0e0e0;
    display: grid;
    place-items: center;
    color: #1f1f1f;
    font-weight: 700;
  }
  
  :global(.nav-btn) {
    color: #212121 !important;
  }
  
  :global(.nav-btn:hover) {
    background-color: #f1f1f1 !important;
  }

  @media (max-width: 900px) {
    .nav-center {
      justify-content: flex-start;
    }

    .search-pill {
      width: 100%;
    }
  }
</style>
