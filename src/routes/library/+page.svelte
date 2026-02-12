<script lang="ts">
  const segments = [
    { label: 'Albums', value: 42, color: '#1db954' },
    { label: 'Artists', value: 28, color: '#1f77b4' },
    { label: 'Playlists', value: 30, color: '#f4b400' }
  ];

  const miniCharts = [
    {
      label: 'Albums',
      value: 42,
      note: 'Saved in your library',
      breakdown: [
        { label: 'Studio', value: 18, color: '#1db954' },
        { label: 'Live', value: 14, color: '#1f77b4' },
        { label: 'Compilations', value: 10, color: '#f4b400' }
      ]
    },
    {
      label: 'Artists',
      value: 28,
      note: 'Saved in your library',
      breakdown: [
        { label: 'Solo', value: 12, color: '#1db954' },
        { label: 'Bands', value: 9, color: '#1f77b4' },
        { label: 'Features', value: 7, color: '#f4b400' }
      ]
    },
    {
      label: 'Playlists',
      value: 30,
      note: 'Saved in your library',
      breakdown: [
        { label: 'Curated', value: 13, color: '#1db954' },
        { label: 'Personal', value: 10, color: '#1f77b4' },
        { label: 'Shared', value: 7, color: '#f4b400' }
      ]
    }
  ];

  const buildGradient = (items: { value: number; color: string }[]) => {
    const sum = items.reduce((acc, item) => acc + item.value, 0) || 1;
    let offset = 0;
    return items
      .map((item) => {
        const start = offset;
        const end = offset + (item.value / sum) * 100;
        offset = end;
        return `${item.color} ${start.toFixed(2)}% ${end.toFixed(2)}%`;
      })
      .join(', ');
  };

  const total = segments.reduce((sum, item) => sum + item.value, 0);
  const chartGradient = buildGradient(segments);
</script>

<section class="library-page">
  <header class="page-head">
    <h1>Your Library</h1>
    <p>Your saved albums, artists, and playlists in one snapshot.</p>
  </header>

  <section class="library-summary">
    <div class="chart-card">
      <div class="card-header">
        <h2>Library breakdown</h2>
        <p>Albums, artists, and playlists mix</p>
      </div>
      <div class="chart-ring" style={`--ring: conic-gradient(${chartGradient})`}>
        <div class="ring-center">
          <span>{total}</span>
          <small>Items</small>
        </div>
      </div>
      <div class="chart-legend">
        {#each segments as item}
          <div class="legend-row">
            <span class="legend-swatch" style={`background:${item.color}`}></span>
            <div>
              <strong>{item.label}</strong>
              <div class="legend-meta">{item.value} items</div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <div class="summary-cards">
      {#each miniCharts as item}
        <div class="summary-card">
          <div class="summary-header">
            <div class="summary-title">{item.label}</div>
            <div class="summary-subtitle">{item.note}</div>
          </div>
          <div
            class="mini-ring"
            style={`--ring: conic-gradient(${buildGradient(item.breakdown)})`}
          >
            <div class="mini-center">
              <span>{item.value}</span>
              <small>Items</small>
            </div>
          </div>
          <div class="mini-legend">
            {#each item.breakdown as detail}
              <div class="legend-row">
                <span class="legend-swatch" style={`background:${detail.color}`}></span>
                <div>
                  <strong>{detail.label}</strong>
                  <div class="legend-meta">{detail.value} items</div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  </section>
</section>

<style>
  .library-page {
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

  .library-summary {
    display: grid;
    grid-template-columns: minmax(240px, 320px) 1fr;
    gap: 20px;
    align-items: stretch;
  }

  .chart-card {
    background: #ffffff;
    border-radius: 18px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    align-items: center;
  }

  .card-header {
    text-align: center;
  }

  .card-header h2 {
    margin: 0;
    font-size: 1.1rem;
  }

  .card-header p {
    margin: 4px 0 0;
    color: #6f6f6f;
    font-size: 0.85rem;
  }

  .chart-ring {
    --ring: conic-gradient(#1db954 0% 33%, #1f77b4 33% 66%, #f4b400 66% 100%);
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: var(--ring);
    display: grid;
    place-items: center;
    position: relative;
  }

  .chart-ring::after {
    content: '';
    position: absolute;
    inset: 16px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: inset 0 0 0 1px #f0f0f0;
  }

  .ring-center {
    position: relative;
    z-index: 1;
    display: grid;
    place-items: center;
    gap: 2px;
    color: #212121;
  }

  .ring-center span {
    font-size: 1.6rem;
    font-weight: 700;
  }

  .ring-center small {
    color: #6f6f6f;
    font-size: 0.85rem;
  }

  .chart-legend {
    display: flex;
    justify-content: center;
    gap: 18px;
    width: 100%;
    flex-wrap: wrap;
  }

  .legend-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.95rem;
  }

  .legend-swatch {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }

  .legend-meta {
    color: #7a7a7a;
    font-size: 0.82rem;
  }

  .summary-cards {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
  }

  .summary-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 10px 18px rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
    gap: 14px;
    align-items: center;
    text-align: center;
  }

  .summary-header {
    display: grid;
    gap: 4px;
  }

  .summary-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #212121;
  }

  .summary-subtitle {
    color: #6f6f6f;
    font-size: 0.85rem;
  }

  .mini-ring {
    --ring: conic-gradient(#1db954 0% 33%, #1f77b4 33% 66%, #f4b400 66% 100%);
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: var(--ring);
    display: grid;
    place-items: center;
    position: relative;
    flex-shrink: 0;
  }

  .mini-ring::after {
    content: '';
    position: absolute;
    inset: 16px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: inset 0 0 0 1px #f0f0f0;
  }

  .mini-center {
    position: relative;
    z-index: 1;
    display: grid;
    place-items: center;
    gap: 2px;
    color: #212121;
  }

  .mini-center span {
    font-size: 1.6rem;
    font-weight: 700;
  }

  .mini-center small {
    color: #6f6f6f;
    font-size: 0.85rem;
  }

  .mini-legend {
    display: flex;
    justify-content: center;
    gap: 18px;
    width: 100%;
    flex-wrap: wrap;
  }

  .mini-legend .legend-row {
    font-size: 0.95rem;
  }

  @media (max-width: 1100px) {
    .library-summary {
      grid-template-columns: 1fr;
    }

    .summary-cards {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 700px) {
    .summary-cards {
      grid-template-columns: 1fr;
    }
  }
</style>
