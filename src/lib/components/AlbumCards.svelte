<script>
  import Card, { Content, Media, PrimaryAction } from '@smui/card';
  
  export let albums = [
    { id: 1, title: "Album One", artist: "Artist One", image: "https://placehold.co/200x200/444/fff?text=Album+1" },
    { id: 2, title: "Album Two", artist: "Artist Two", image: "https://placehold.co/200x200/555/fff?text=Album+2" },
    { id: 3, title: "Album Three", artist: "Artist Three", image: "https://placehold.co/200x200/666/fff?text=Album+3" },
    { id: 4, title: "Album Four", artist: "Artist Four", image: "https://placehold.co/200x200/777/fff?text=Album+4" },
  ];
</script>

<div class="grid">
  {#each albums as album (album.id)}
    <div class="card-wrapper">
      <Card class="album-card">
        <PrimaryAction>
          <Media aspectRatio="square" class="album-media">
            <img src={album.image} alt={album.title} />
          </Media>
          <Content class="card-content">
            <h3 class="album-title">{album.title}</h3>
            <p class="album-artist">{album.artist}</p>
          </Content>
        </PrimaryAction>
      </Card>
    </div>
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
  }
  
  .card-wrapper :global(.album-card) {
    background-color: #ffffff !important;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
  }
  
  .card-wrapper :global(.album-card:hover) {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateY(-4px);
  }
  
  :global(.album-media) {
    overflow: hidden;
  }
  
  :global(.album-media img) {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  :global(.card-content) {
    padding: 1rem !important;
  }
  
  .album-title {
    margin: 0 0 0.25rem;
    color: #212121;
    font-size: 0.95rem;
    font-weight: 600;
  }
  
  .album-artist {
    margin: 0;
    color: #757575;
    font-size: 0.85rem;
  }
</style>
