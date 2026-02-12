<script lang="ts">
  import Card, { Content } from '@smui/card';
  import IconButton from '@smui/icon-button';
  import CardMediaImage from '$lib/components/CardMediaImage.svelte';

  export let title = 'Live at Wembley';
  export let thumbnailUrl: string | null = null;
</script>

<Card class="video-card">
  <div class="media-wrap">
    <CardMediaImage
      src={thumbnailUrl}
      alt={`${title} thumbnail`}
      aspectRatio="16x9"
      icon="smart_display"
    />
    <div class="overlay">
      <IconButton class="material-icons" aria-label="Play">play_circle_outline</IconButton>
    </div>
  </div>

  <Content class="video-content">{title}</Content>
</Card>

<style>
  .video-card {
    width: 300px;
    background: #181818;
    color: white;
  }

  .media-wrap {
    position: relative;
  }

  .overlay {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    pointer-events: none;
  }

  .overlay :global(.material-icons) {
    color: white;
    font-size: 48px;
    opacity: 0.9;
  }

  .video-content {
    padding-top: 10px;
  }
</style>

