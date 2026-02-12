<script lang="ts">
  import Textfield from '@smui/textfield';
  import Select, { Option } from '@smui/select';
  import Switch from '@smui/switch';
  import Button, { Label } from '@smui/button';

  let playlistName = '';
  let playlistType = 'mix';
  let playlistVisibility = 'private';
  let dedicatedTo = 'chill';
  let genreFrom = 'Alternative';
  let genreTo = 'World';
  let allowedGenres = '';
  let includeExplicit = true;

  let ruleReleaseEnabled = true;
  let ruleReleaseAfter = '';
  let ruleReleaseBefore = '';

  let ruleBpmEnabled = true;
  let bpmMin = '90';
  let bpmMax = '140';

  let ruleDurationEnabled = false;
  let durationMin = '2';
  let durationMax = '6';
</script>

<section class="page create-playlist settings-textfields">
  <header class="page-head">
    <h1>Create Playlist</h1>
    <p>Build a playlist with tailored filters and automation rules.</p>
  </header>

  <section class="section-card">
    <div class="section-head">
      <h2>Playlist Basics</h2>
      <p>Define the identity and purpose of your new playlist.</p>
    </div>

    <div class="form-grid two-col">
      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Playlist name"
        variant="outlined"
        dense
        bind:value={playlistName}
        label$floatAbove
      />

      <Select class="settings-field" label="Playlist type" variant="outlined" bind:value={playlistType}>
        <Option value="mix">Smart mix</Option>
        <Option value="focus">Focus</Option>
        <Option value="workout">Workout</Option>
        <Option value="party">Party</Option>
        <Option value="sleep">Sleep</Option>
      </Select>

      <Select
        class="settings-field"
        label="Visibility"
        variant="outlined"
        bind:value={playlistVisibility}
      >
        <Option value="private">Private</Option>
        <Option value="friends">Friends only</Option>
        <Option value="public">Public</Option>
      </Select>

      <Select class="settings-field" label="Dedicated to" variant="outlined" bind:value={dedicatedTo}>
        <Option value="chill">Chill</Option>
        <Option value="focus">Focus</Option>
        <Option value="energy">High energy</Option>
        <Option value="romance">Romance</Option>
        <Option value="mood">Moody</Option>
      </Select>
    </div>
  </section>

  <section class="section-card">
    <div class="section-head">
      <h2>Music Filters</h2>
      <p>Choose genres and constraints for the playlist to focus on.</p>
    </div>

    <div class="form-grid three-col">
      <Select class="settings-field" label="Genre range from" variant="outlined" bind:value={genreFrom}>
        <Option value="Alternative">Alternative</Option>
        <Option value="Dance">Dance</Option>
        <Option value="Hip Hop">Hip Hop</Option>
        <Option value="Indie">Indie</Option>
        <Option value="Pop">Pop</Option>
        <Option value="Rock">Rock</Option>
      </Select>

      <Select class="settings-field" label="Genre range to" variant="outlined" bind:value={genreTo}>
        <Option value="World">World</Option>
        <Option value="Soul">Soul</Option>
        <Option value="Synthwave">Synthwave</Option>
        <Option value="R&B">R&B</Option>
        <Option value="Jazz">Jazz</Option>
        <Option value="Classical">Classical</Option>
      </Select>

      <Textfield
        class="settings-field mdc-text-field--label-floating"
        label="Allowed genres only (comma-separated)"
        variant="outlined"
        dense
        bind:value={allowedGenres}
        label$floatAbove
      />
    </div>

    <div class="form-grid two-col">
      <div class="toggle-row">
        <Switch bind:checked={includeExplicit} />
        <div>
          <div class="toggle-title">Allow explicit</div>
          <div class="toggle-sub">Include songs with explicit lyrics.</div>
        </div>
      </div>

      <div class="helper-card">
        <h3>Distinct genres only</h3>
        <p>
          Add a list of specific genres to keep in the playlist. Leave this empty if you want
          genre range only.
        </p>
      </div>
    </div>
  </section>

  <section class="section-card rules-card">
    <div class="section-head">
      <h2>Automation Rules</h2>
      <p>Automate the playlist like email rules to keep it fresh.</p>
    </div>

    <div class="rules-list">
      <div class="rule-row">
        <div class="rule-info">
          <Switch bind:checked={ruleReleaseEnabled} />
          <div>
            <h3>Release date window</h3>
            <p>Only include songs released before/after a specific date.</p>
          </div>
        </div>
        <div class="rule-fields">
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="Released after"
            variant="outlined"
            dense
            bind:value={ruleReleaseAfter}
            label$floatAbove
            type="date"
          />
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="Released before"
            variant="outlined"
            dense
            bind:value={ruleReleaseBefore}
            label$floatAbove
            type="date"
          />
        </div>
      </div>

      <div class="rule-row">
        <div class="rule-info">
          <Switch bind:checked={ruleBpmEnabled} />
          <div>
            <h3>BPM range</h3>
            <p>Define the tempo window for the playlist.</p>
          </div>
        </div>
        <div class="rule-fields">
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="Min BPM"
            variant="outlined"
            dense
            bind:value={bpmMin}
            label$floatAbove
            type="number"
          />
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="Max BPM"
            variant="outlined"
            dense
            bind:value={bpmMax}
            label$floatAbove
            type="number"
          />
        </div>
      </div>

      <div class="rule-row">
        <div class="rule-info">
          <Switch bind:checked={ruleDurationEnabled} />
          <div>
            <h3>Track length range</h3>
            <p>Keep tracks between a minimum and maximum length.</p>
          </div>
        </div>
        <div class="rule-fields">
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="Min minutes"
            variant="outlined"
            dense
            bind:value={durationMin}
            label$floatAbove
            type="number"
          />
          <Textfield
            class="settings-field mdc-text-field--label-floating"
            label="Max minutes"
            variant="outlined"
            dense
            bind:value={durationMax}
            label$floatAbove
            type="number"
          />
        </div>
      </div>
    </div>
  </section>

  <div class="page-actions">
    <Button variant="raised"><Label>Create Playlist</Label></Button>
    <Button variant="outlined"><Label>Cancel</Label></Button>
  </div>
</section>

<style>
  .page {
    display: flex;
    flex-direction: column;
    gap: 22px;
  }

  .page-head h1 {
    margin: 0;
  }

  .page-head p {
    margin: 6px 0 0;
    color: #6f6f6f;
  }

  .section-card {
    background: #ffffff;
    border-radius: 18px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    padding: 22px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .section-head h2 {
    margin: 0;
    font-size: 1.1rem;
  }

  .section-head p {
    margin: 6px 0 0;
    color: #6f6f6f;
  }

  .form-grid {
    display: grid;
    gap: 16px;
  }

  .two-col {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .three-col {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .toggle-row {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #f6f8f9;
    border-radius: 12px;
    padding: 12px;
  }

  .toggle-title {
    font-weight: 600;
  }

  .toggle-sub {
    font-size: 0.85rem;
    color: #6f6f6f;
  }

  .helper-card {
    background: #f6f8f9;
    border-radius: 12px;
    padding: 14px;
    color: #5c5c5c;
  }

  .helper-card h3 {
    margin: 0 0 6px;
    font-size: 0.95rem;
  }

  .helper-card p {
    margin: 0;
    font-size: 0.85rem;
  }

  .rules-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .rule-row {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) minmax(280px, 1.3fr);
    gap: 16px;
    background: #f9fbfb;
    border-radius: 14px;
    padding: 16px;
  }

  .rule-info {
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }

  .rule-info h3 {
    margin: 0;
    font-size: 0.95rem;
  }

  .rule-info p {
    margin: 4px 0 0;
    color: #6f6f6f;
    font-size: 0.85rem;
  }

  .rule-fields {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
  }

  .page-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }

  :global(.page-actions .mdc-button--raised) {
    background-color: #1db954;
  }

  :global(.page-actions .mdc-button) {
    border-radius: 12px;
  }

  @media (max-width: 1100px) {
    .three-col {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 900px) {
    .two-col,
    .three-col,
    .rule-row {
      grid-template-columns: 1fr;
    }
  }
</style>
