<script>
  import List, { Item, Graphic, Text, Meta } from '@smui/list';
  import IconButton from '@smui/icon-button';
  
  let songs = [
    { id: 1, title: "Track 01", artist: "Artist 01", duration: "3:45", liked: false, image: "https://placehold.co/40x40/333/fff?text=01" },
    { id: 2, title: "Track 02", artist: "Artist 02", duration: "4:12", liked: true, image: "https://placehold.co/40x40/444/fff?text=02" },
  ];
  
  function toggleLike(id) {
    songs = songs.map(song => 
      song.id === id ? { ...song, liked: !song.liked } : song
    );
  }
</script>

<div class="playlist-container">
  <List twoLine avatarList class="song-list">
    {#each songs as song (song.id)}
      <Item class="song-item">
        <Graphic style="background-image: url({song.image}); background-size: cover; border-radius: 4px;" />
        <Text>
          <span class="song-title">{song.title}</span>
          <span slot="secondary" class="song-artist">{song.artist}</span>
        </Text>
        <Meta>
          <IconButton
            class={`material-icons like-btn ${song.liked ? 'is-liked' : ''}`}
            on:click={() => toggleLike(song.id)}
            aria-label={song.liked ? 'Unlike' : 'Like'}
          >
            {song.liked ? 'favorite' : 'favorite_border'}
          </IconButton>
          <span class="duration">{song.duration}</span>
        </Meta>
      </Item>
    {/each}
  </List>
</div>

<style>
  .playlist-container {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    overflow: hidden;
  }
  
  :global(.song-list) {
    background-color: #ffffff !important;
  }
  
  :global(.song-item) {
    height: 64px !important;
    padding: 0.5rem 1rem !important;
    border-bottom: 1px solid #f5f5f5;
  }
  
  :global(.song-item:last-child) {
    border-bottom: none;
  }
  
  :global(.song-item:hover) {
    background-color: #f9f9f9 !important;
  }
  
  .song-title {
    color: #212121;
    font-weight: 500;
  }
  
  .song-artist {
    color: #757575;
  }
  
  .duration {
    margin-left: 1rem;
    color: #757575;
    font-size: 0.85rem;
  }
  
  :global(.like-btn) {
    color: #757575 !important;
  }
  
  :global(.like-btn.is-liked) {
    color: #1db954 !important;
  }
</style>
