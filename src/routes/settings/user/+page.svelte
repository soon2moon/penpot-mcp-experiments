<script lang="ts">
  import Button, { Label } from '@smui/button';
</script>

<section class="form-card">
  <div class="form-head">
    <h2>User settings</h2>
    <p>Update your language and time zone</p>
  </div>

  <form class="form-body" autocomplete="off">
    <label>
      Language
      <select name="language">
        <option value="en">English</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        <option value="de">German</option>
      </select>
    </label>

    <label>
      Time zone
      <select name="timezone">
        <option value="utc-8">Pacific Time (UTC-8)</option>
        <option value="utc-6">Central Time (UTC-6)</option>
        <option value="utc-5">Eastern Time (UTC-5)</option>
        <option value="utc+1">Central Europe (UTC+1)</option>
      </select>
    </label>
  </form>

  <div class="form-actions">
    <Button variant="raised"><Label>Save</Label></Button>
    <Button variant="outlined"><Label>Cancel</Label></Button>
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
    max-width: 520px;
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
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px 16px;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 0.85rem;
    color: #555;
  }

  select {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.9rem;
    background: #ffffff;
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
