<section class="hub">
  <h2>Choose a settings section</h2>
  <div class="hub-grid">
    <a class="hub-card" href="/settings/profile">
      <span class="material-icons">person</span>
      <div>
        <div class="hub-title">User profile</div>
        <div class="hub-sub">Private and login information</div>
      </div>
    </a>

    <a class="hub-card" href="/settings/user">
      <span class="material-icons">tune</span>
      <div>
        <div class="hub-title">User settings</div>
        <div class="hub-sub">Language and time zone</div>
      </div>
    </a>

    <a class="hub-card" href="/settings/accounts">
      <span class="material-icons">manage_accounts</span>
      <div>
        <div class="hub-title">Manage accounts</div>
        <div class="hub-sub">Update user accounts</div>
      </div>
    </a>
  </div>
</section>

<style>
  .hub {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .hub h2 {
    margin: 0;
    font-size: 1.2rem;
  }

  .hub-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
  }

  .hub-card {
    display: flex;
    gap: 12px;
    align-items: center;
    background: #ffffff;
    border-radius: 14px;
    padding: 14px;
    text-decoration: none;
    color: #212121;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  }

  .hub-card .material-icons {
    color: #1db954;
  }

  .hub-title {
    font-weight: 600;
  }

  .hub-sub {
    font-size: 0.85rem;
    color: #6b6b6b;
  }
</style>
