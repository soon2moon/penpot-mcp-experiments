<script lang="ts">
  import Select, { Option } from '@smui/select';

  export let value: string = '';
  export let genres: string[] = ['Rock', 'Pop', 'Jazz', 'Classical'];
</script>

<Select bind:value label="Filter Genre">
  <Option value="">All genres</Option>
  {#each genres as genre (genre)}
    <Option value={genre}>{genre}</Option>
  {/each}
</Select>

