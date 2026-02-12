<script lang="ts">
  import Textfield from '@smui/textfield';
  import Select, { Option } from '@smui/select';
  import Switch from '@smui/switch';
  import IconButton from '@smui/icon-button';
  import Button, { Label } from '@smui/button';

  let nextId = 4;
  let newUserEmail = '';
  let newUserRole = 'member';

  let users = [
    {
      id: 'U-001',
      name: 'User One',
      email: 'user.one@example.com',
      role: 'admin',
      active: true,
      memberSince: '12, 01, 2026, 09:15:22'
    },
    {
      id: 'U-002',
      name: 'User Two',
      email: 'user.two@example.com',
      role: 'member',
      active: true,
      memberSince: '25, 01, 2026, 14:05:03'
    },
    {
      id: 'U-003',
      name: 'User Three',
      email: 'user.three@example.com',
      role: 'mod',
      active: false,
      memberSince: '02, 02, 2026, 18:45:50'
    }
  ];

  const formatDate = (date: Date) => {
    const pad = (value: number) => String(value).padStart(2, '0');
    return `${pad(date.getDate())}, ${pad(date.getMonth() + 1)}, ${date.getFullYear()}, ${pad(
      date.getHours()
    )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  };

  const addUser = () => {
    if (!newUserEmail.trim()) return;
    const id = `U-${String(nextId).padStart(3, '0')}`;
    nextId += 1;
    users = [
      ...users,
      {
        id,
        name: '',
        email: newUserEmail.trim(),
        role: newUserRole,
        active: true,
        memberSince: formatDate(new Date())
      }
    ];
    newUserEmail = '';
    newUserRole = 'member';
  };

  const removeUser = (id: string) => {
    users = users.filter((user) => user.id !== id);
  };
</script>

<section class="form-card">
  <div class="form-head">
    <h2>Add Account</h2>
    <p>Click to invite a new user from your party</p>
  </div>

  <div class="add-user-grid settings-textfields">
    <Textfield
      class="settings-field mdc-text-field--label-floating"
      label="New user email"
      variant="outlined"
      dense
      bind:value={newUserEmail}
      label$floatAbove
    />

    <Select
      class="settings-field"
      label="Role"
      variant="outlined"
      bind:value={newUserRole}
    >
      <Option value="admin">Admin</Option>
      <Option value="member">Member</Option>
      <Option value="mod">Mod</Option>
    </Select>
  </div>

  <div class="add-user-actions">
    <Button variant="raised" on:click={addUser}><Label>Add User</Label></Button>
  </div>
</section>

<section class="form-card">
  <div class="form-head">
    <h2>Manage Accounts</h2>
    <p>Update User Accounts</p>
  </div>

  <div class="accounts-table">
    <div class="accounts-grid settings-textfields">
      <div class="grid-head">User ID</div>
      <div class="grid-head">User Name</div>
      <div class="grid-head">User Email</div>
      <div class="grid-head">Role</div>
      <div class="grid-head">Status</div>
      <div class="grid-head">Member Since</div>
      <div class="grid-head"></div>

      {#each users as user (user.id)}
        <div class="cell id-cell">{user.id}</div>
        <div class="cell">
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="User name"
            variant="outlined"
            dense
            bind:value={user.name}
            label$floatAbove
            aria-label={`User name for ${user.id}`}
          />
        </div>
        <div class="cell">
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="User email"
            variant="outlined"
            dense
            bind:value={user.email}
            label$floatAbove
            aria-label={`User email for ${user.id}`}
          />
        </div>
        <div class="cell">
          <Select
            class="settings-field"
            label="Role"
            variant="outlined"
            bind:value={user.role}
          >
            <Option value="admin">Admin</Option>
            <Option value="member">Member</Option>
            <Option value="mod">Mod</Option>
          </Select>
        </div>
        <div class="cell status-cell">
          <Switch bind:checked={user.active} />
          <span class="status-label">{user.active ? 'Active' : 'Inactive'}</span>
        </div>
        <div class="cell since-cell">{user.memberSince}</div>
        <div class="cell delete-cell">
          <IconButton class="material-icons delete-btn" on:click={() => removeUser(user.id)}>
            delete
          </IconButton>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .form-card {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 12px 22px rgba(0, 0, 0, 0.08);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-width: 100%;
    overflow: visible;
  }

  .form-head h2 {
    margin: 0;
    font-size: 1.1rem;
  }

  .form-head p {
    margin: 4px 0 0;
    color: #6b6b6b;
    font-size: 0.9rem;
  }

  .add-user-grid {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 16px;
    margin-top: 6px;
  }

  .add-user-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 12px;
  }

  .accounts-table {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 6px;
  }

  .accounts-grid {
    display: grid;
    grid-template-columns: 90px minmax(150px, 1fr) minmax(170px, 1.2fr) 130px 130px 170px 36px;
    gap: 14px 12px;
    align-items: center;
    margin-top: 12px;
    min-width: 760px;
    overflow: hidden;
  }

  .grid-head {
    font-size: 0.85rem;
    color: #666;
    font-weight: 600;
    padding-bottom: 8px;
    border-bottom: 1px solid #e6e6e6;
  }

  .cell {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .id-cell {
    font-weight: 600;
    color: #212121;
  }

  .status-cell {
    gap: 8px;
  }

  .status-label {
    font-size: 0.85rem;
    color: #6b6b6b;
  }

  .since-cell {
    font-size: 0.85rem;
    color: #555;
    white-space: nowrap;
    padding-left: 6px;
  }

  .delete-cell {
    justify-content: center;
  }

  .delete-btn {
    color: #d32f2f;
  }

  :global(.add-user-actions .mdc-button) {
    border-radius: 10px;
  }

  :global(.add-user-actions .mdc-button--raised) {
    background-color: #1db954;
  }

  @media (max-width: 900px) {
    .add-user-grid {
      grid-template-columns: 1fr;
    }

    .accounts-grid {
      grid-template-columns: 1fr;
      min-width: 0;
    }
  }
</style>
