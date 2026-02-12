<script>
  import Slider from '@smui/slider';
  import IconButton from '@smui/icon-button';
  
  let volume = 50;
  let progress = 30;
  const albumArtUrl = 'https://placehold.co/72x72/f5f5f5/707070?text=Album+Art';
</script>

<div class="player-card">
  <div class="song-info">
    <div class="album-art">
      <img src={albumArtUrl} alt="Album Art" />
    </div>
    <div class="song-text">
      <div class="title">Sample Track</div>
      <div class="artist">Artist Name</div>
    </div>
    <IconButton class="material-icons like-btn" aria-label="Like">favorite</IconButton>
  </div>

  <div class="controls">
    <div class="buttons">
      <IconButton class="material-icons">shuffle</IconButton>
      <IconButton class="material-icons">skip_previous</IconButton>
      <IconButton class="material-icons play-btn">play_circle_filled</IconButton>
      <IconButton class="material-icons">skip_next</IconButton>
      <IconButton class="material-icons">repeat</IconButton>
    </div>
    <div class="progress-bar">
      <span class="time">1:24</span>
      <Slider bind:value={progress} min={0} max={100} style="flex: 1;" />
      <span class="time">3:45</span>
    </div>
  </div>

  <div class="volume-controls">
    <IconButton class="material-icons">playlist_play</IconButton>
    <IconButton class="material-icons">volume_up</IconButton>
    <div class="vol-slider">
      <Slider bind:value={volume} min={0} max={100} />
    </div>
  </div>
</div>

<style>
  .player-card {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) minmax(320px, 2fr) minmax(200px, 1fr);
    align-items: center;
    /*height: 100%;*/
    padding: 8px 16px;
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    box-sizing: border-box;
    width: 100%;
  }
  .song-info { display: flex; align-items: center; gap: 12px; }
  .album-art {
    width: 68px;
    height: 68px;
    border-radius: 12px;
    overflow: hidden;
    background: #f5f5f5;
    border: 1px solid #e6e6e6;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
    box-sizing: border-box;
  }
  .album-art img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    border-radius: 8px;
  }
  .song-text { display: flex; flex-direction: column; }
  .title { color: #212121; font-size: 0.9rem; font-weight: 600; }
  .artist { color: #757575; font-size: 0.75rem; }
  
  .controls { display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .controls { gap: 4px; }
  .buttons { display: flex; align-items: center; gap: 14px; }
  :global(.play-btn) {
    color: #1db954 !important;
    background-color: rgba(29, 185, 84, 0.12);
    border-radius: 999px;
    width: 46px;
    height: 46px;
  }
  :global(.play-btn .mdc-icon-button__icon) {
    font-size: 46px;
  }
  
  .progress-bar {
    display: flex;
    align-items: center;
    width: min(560px, 100%);
    gap: 10px;
  }
  .time { font-size: 0.7rem; color: #9e9e9e; }
  
  .volume-controls { display: flex; align-items: center; justify-content: flex-end; gap: 6px; }
  .vol-slider { width: 100px; }
  
  :global(.player-card .mdc-icon-button) {
    color: #757575;
    width: 38px;
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  :global(.player-card .mdc-icon-button__icon) {
    line-height: 1;
  }
  :global(.player-card .mdc-icon-button:hover) { color: #212121; }
  :global(.like-btn) { color: #1db954 !important; }
</style>
