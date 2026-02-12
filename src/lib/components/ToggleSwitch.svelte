<!-- ToggleSwitch.svelte -->
<script lang="ts">
  import Switch from '@smui/switch';
  import FormField from '@smui/form-field';

  export let label = 'Option';
  export let checked = false;
</script>

<FormField>
  <Switch bind:checked />
  <span slot="label">{label}</span>
</FormField>

<style>
  span { color: white; }
</style>

