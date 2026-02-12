<!-- RadioGroup.svelte -->
<script lang="ts">
  import FormField from '@smui/form-field';
  import Radio from '@smui/radio';

  export let station: 'FM' | 'AM' = 'FM';
</script>

<FormField>
  <Radio bind:group={station} value="FM" />
  <span slot="label">FM Radio</span>
</FormField>

<FormField>
  <Radio bind:group={station} value="AM" />
  <span slot="label">AM Radio</span>
</FormField>

<style>
  span { color: white; }
</style>
