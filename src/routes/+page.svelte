<script lang="ts">
  const chips = ['All', 'Music', 'Podcasts', 'Audiobooks'];

  const quickPicks = [
    {
      id: 'jt',
      title: 'Playlist 01',
      subtitle: 'New playlist',
      image: 'https://placehold.co/72x72/111/fff?text=P1'
    },
    {
      id: 'delulu',
      title: 'Playlist 02',
      subtitle: 'Collection',
      image: 'https://placehold.co/72x72/2b2b2b/fff?text=P2'
    },
    {
      id: 'celos',
      title: 'Playlist 03',
      subtitle: 'Fresh picks',
      image: 'https://placehold.co/72x72/3b3b3b/fff?text=P3'
    },
    {
      id: 'release-radar',
      title: 'Playlist 04',
      subtitle: 'Weekly updates',
      image: 'https://placehold.co/72x72/222/fff?text=P4'
    },
    {
      id: 'daily-mix',
      title: 'Playlist 05',
      subtitle: 'Personalized',
      image: 'https://placehold.co/72x72/1a1a1a/fff?text=P5'
    },
    {
      id: 'vibes',
      title: 'Playlist 06',
      subtitle: 'Mood',
      image: 'https://placehold.co/72x72/2d2d2d/fff?text=P6'
    }
  ];

  const madeForYou = [
    {
      id: 'discover',
      title: 'Mix 01',
      subtitle: 'Curated picks for you.',
      image: 'https://placehold.co/320x320/1f2937/fff?text=Mix+01'
    },
    {
      id: 'mix-01',
      title: 'Mix 02',
      subtitle: 'Artist A, Artist B, Artist C',
      image: 'https://placehold.co/320x320/111827/fff?text=Mix+02'
    },
    {
      id: 'mix-02',
      title: 'Mix 03',
      subtitle: 'Artist D, Artist E, Artist F',
      image: 'https://placehold.co/320x320/0f172a/fff?text=Mix+03'
    },
    {
      id: 'mix-03',
      title: 'Mix 04',
      subtitle: 'Artist G, Artist H, Artist I',
      image: 'https://placehold.co/320x320/111/fff?text=Mix+04'
    },
    {
      id: 'mix-04',
      title: 'Mix 05',
      subtitle: 'Artist J, Artist K, Artist L',
      image: 'https://placehold.co/320x320/1a1a1a/fff?text=Mix+05'
    },
    {
      id: 'mix-05',
      title: 'Mix 06',
      subtitle: 'Artist M, Artist N, Artist O',
      image: 'https://placehold.co/320x320/202020/fff?text=Mix+06'
    }
  ];

  const newReleases = [
    {
      id: 'release-01',
      title: 'Release 01',
      subtitle: 'Artist 01',
      image: 'https://placehold.co/320x320/272727/fff?text=Release+01'
    },
    {
      id: 'release-02',
      title: 'Release 02',
      subtitle: 'Artist 02',
      image: 'https://placehold.co/320x320/1a1a1a/fff?text=Release+02'
    },
    {
      id: 'release-03',
      title: 'Release 03',
      subtitle: 'Artist 03',
      image: 'https://placehold.co/320x320/121212/fff?text=Release+03'
    },
    {
      id: 'release-04',
      title: 'Release 04',
      subtitle: 'Artist 04',
      image: 'https://placehold.co/320x320/1f1f1f/fff?text=Release+04'
    },
    {
      id: 'release-05',
      title: 'Release 05',
      subtitle: 'Artist 05',
      image: 'https://placehold.co/320x320/2b2b2b/fff?text=Release+05'
    }
  ];
</script>

<div class="home">
  <header class="hero">
    <div class="hero-title">
      <h1>Welcome Back</h1>
      <p>Jump into your favorites, curated daily.</p>
    </div>

    <div class="chip-row">
      {#each chips as chip}
        <button class={`chip ${chip === 'All' ? 'active' : ''}`}>{chip}</button>
      {/each}
    </div>

    <div class="quick-grid">
      {#each quickPicks as pick (pick.id)}
        <button class="quick-card">
          <img class="quick-image" src={pick.image} alt={pick.title} />
          <div class="quick-text">
            <div class="quick-title">{pick.title}</div>
            <div class="quick-sub">{pick.subtitle}</div>
          </div>
          <span class="material-icons quick-play" aria-hidden="true">play_arrow</span>
        </button>
      {/each}
    </div>
  </header>

  <section class="row">
    <div class="row-head">
      <h2>Made for you</h2>
      <button class="see-all">Show all</button>
    </div>
    <div class="card-row">
      {#each madeForYou as item (item.id)}
        <article class="media-card">
          <div class="card-cover">
            <img src={item.image} alt={item.title} />
          </div>
          <div class="card-title">{item.title}</div>
          <div class="card-sub">{item.subtitle}</div>
        </article>
      {/each}
    </div>
  </section>

  <section class="row">
    <div class="row-head">
      <h2>New releases for you</h2>
      <button class="see-all">Show all</button>
    </div>
    <div class="card-row">
      {#each newReleases as item (item.id)}
        <article class="media-card">
          <div class="card-cover">
            <img src={item.image} alt={item.title} />
          </div>
          <div class="card-title">{item.title}</div>
          <div class="card-sub">{item.subtitle}</div>
        </article>
      {/each}
    </div>
  </section>
</div>

<style>
  .home {
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .hero {
    padding: 8px 0 12px;
  }

  .hero-title h1 {
    margin: 0 0 4px;
    font-size: 2rem;
  }

  .hero-title p {
    margin: 0 0 18px;
    color: #666;
    font-size: 0.95rem;
  }

  .chip-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 24px;
    overflow: visible;
  }

  .chip {
    border: 1px solid #e0e0e0;
    background: #ffffff;
    color: #212121;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    cursor: pointer;
  }

  .chip.active {
    background: #1db954;
    border-color: #1db954;
    color: #ffffff;
  }

  .quick-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
  }

  .quick-card {
    display: flex;
    align-items: center;
    gap: 12px;
    border: none;
    background: #ffffff;
    padding: 10px 14px;
    border-radius: 14px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    cursor: pointer;
    position: relative;
  }

  .quick-image {
    width: 56px;
    height: 56px;
    border-radius: 10px;
    object-fit: cover;
  }

  .quick-text {
    flex: 1;
    min-width: 0;
  }

  .quick-title {
    font-weight: 600;
    color: #212121;
    font-size: 0.95rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .quick-sub {
    color: #757575;
    font-size: 0.8rem;
  }

  .quick-play {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #1db954;
    color: #ffffff;
    display: grid;
    place-items: center;
    font-size: 20px;
  }

  .row {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .row-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .row-head h2 {
    margin: 0;
  }

  .see-all {
    border: none;
    background: transparent;
    color: #666;
    cursor: pointer;
  }

  .card-row {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: minmax(160px, 1fr);
    gap: 16px;
    padding-bottom: 6px;
  }

  .media-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 14px;
    box-shadow: 0 10px 18px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .card-cover {
    border-radius: 12px;
    overflow: hidden;
    background: #1a1a1a;
    aspect-ratio: 1 / 1;
  }

  .card-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .card-title {
    font-weight: 600;
    color: #212121;
    font-size: 0.95rem;
  }

  .card-sub {
    color: #757575;
    font-size: 0.8rem;
  }

  @media (max-width: 900px) {
    .quick-grid {
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    .card-row {
      grid-auto-columns: minmax(150px, 1fr);
    }
  }
</style>
