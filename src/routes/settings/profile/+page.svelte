<script lang="ts">
  import Textfield from '@smui/textfield';
  import Button, { Label } from '@smui/button';

  let firstName = '';
  let lastName = '';
  let userName = '';
  let email = '';
  let organization = '';
  let role = '';
  let currentPassword = '';
  let newPassword = '';
  let confirmPassword = '';
</script>

<div class="settings-grid">
  <section class="form-card">
    <div class="form-head">
      <h2>Private information</h2>
      <p>Set up your user profile</p>
    </div>

    <form class="form-body settings-textfields" autocomplete="off">
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="First name"
        variant="outlined"
        dense
        bind:value={firstName}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Last name"
        variant="outlined"
        dense
        bind:value={lastName}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="User name"
        variant="outlined"
        dense
        bind:value={userName}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Email"
        type="email"
        variant="outlined"
        dense
        bind:value={email}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Organization"
        variant="outlined"
        dense
        bind:value={organization}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Role"
        variant="outlined"
        dense
        bind:value={role}
        label$floatAbove
      />
    </form>

    <div class="form-actions">
      <Button variant="raised"><Label>Save</Label></Button>
      <Button variant="outlined"><Label>Cancel</Label></Button>
    </div>
  </section>

  <section class="form-card">
    <div class="form-head">
      <h2>Log in information</h2>
      <p>Change your password</p>
    </div>

    <form class="form-body settings-textfields" autocomplete="off">
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Current password"
        type="password"
        variant="outlined"
        dense
        bind:value={currentPassword}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="New password"
        type="password"
        variant="outlined"
        dense
        bind:value={newPassword}
        label$floatAbove
      />
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="New password"
        type="password"
        variant="outlined"
        dense
        bind:value={confirmPassword}
        label$floatAbove
      />
    </form>

    <div class="form-actions">
      <Button variant="raised"><Label>Save</Label></Button>
      <Button variant="outlined"><Label>Cancel</Label></Button>
    </div>
  </section>
</div>

<style>
  .settings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
  }

  .form-card {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 12px 22px rgba(0, 0, 0, 0.08);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
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

  .form-body {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 24px 16px;
    padding-top: 16px;
  }


  .form-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-start;
  }

  :global(.form-actions .mdc-button) {
    border-radius: 10px;
  }

  :global(.form-actions .mdc-button--raised) {
    background-color: #1db954;
  }
</style>
