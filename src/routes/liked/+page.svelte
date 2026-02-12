<script lang="ts">
  import { onMount } from 'svelte';
  import Select, { Option } from '@smui/select';
  import Button, { Label } from '@smui/button';

  const metrics = [
    { value: 'songs', label: 'Songs played', unit: 'Songs' },
    { value: 'minutes', label: 'Minutes listened', unit: 'Minutes' },
    { value: 'genres', label: 'Genres', unit: 'Genres' },
    { value: 'artists', label: 'Artists', unit: 'Artists' },
    { value: 'albums', label: 'Albums', unit: 'Albums' }
  ];

  const ranges = [
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'Week' },
    { value: 'month', label: 'Month' },
    { value: '3months', label: '3 Months' },
    { value: '6months', label: '6 Months' },
    { value: 'year', label: 'Year' }
  ];

  let metric = metrics[0].value;
  let range = ranges[1].value;

  const labels = ['01 Mon', '02 Tue', '03 Wed', '04 Thu', '05 Fri', '06 Sat', '07 Sun'];

  const dataByMetric: Record<string, number[]> = {
    songs: [18, 26, 14, 32, 28, 20, 36],
    minutes: [210, 320, 160, 380, 330, 240, 410],
    genres: [4, 7, 3, 8, 6, 5, 9],
    artists: [12, 18, 10, 21, 17, 13, 24],
    albums: [6, 9, 5, 11, 10, 7, 13]
  };

  const summaryCards = [
    { label: 'Total number of songs', value: '4,820' },
    { label: 'Total minutes', value: '18,540' },
    { label: 'Total genres', value: '54' },
    { label: 'Total artists', value: '392' },
    { label: 'Total albums', value: '186' }
  ];

  let country = 'Global';
  let region = 'North America';
  let city = 'All cities';

  const chartHeight = 240;
  const chartTop = 30;
  const chartBottom = 210;
  const chartLeft = 24;
  const chartRight = 24;
  const tickCount = 5;
  let chartWidth = 700;
  let chartContainer: HTMLDivElement | null = null;

  onMount(() => {
    if (!chartContainer) return;
    const updateWidth = () => {
      chartWidth = chartContainer?.clientWidth || 700;
    };
    updateWidth();
    const observer = new ResizeObserver(updateWidth);
    observer.observe(chartContainer);
    return () => observer.disconnect();
  });

  $: series = dataByMetric[metric] ?? dataByMetric.songs;
  $: maxValue = Math.max(...series, 1);
  $: tickLabels = Array.from({ length: tickCount }, (_, index) =>
    Math.round(maxValue - (index * maxValue) / (tickCount - 1))
  );
  $: tickYs = Array.from({ length: tickCount }, (_, index) =>
    chartTop + (index * (chartBottom - chartTop)) / (tickCount - 1)
  );
  $: points = series
    .map((value, index) => {
      const width = Math.max(chartWidth - chartLeft - chartRight, 1);
      const x = chartLeft + (index * width) / (series.length - 1);
      const y = chartBottom - (value / maxValue) * (chartBottom - chartTop);
      return `${x},${y}`;
    })
    .join(' ');
</script>

<section class="listening-stats settings-textfields">
  <header class="page-head">
    <h1>Listening stats</h1>
    <p>Track playback trends, totals, and region-based insights.</p>
  </header>

  <section class="chart-card">
    <div class="chart-head">
      <div>
        <h2>Listening activity</h2>
        <p>Review trends across your selected time range.</p>
      </div>
      <div class="chart-controls">
        <Select class="settings-field" label="Metric" variant="outlined" bind:value={metric}>
          {#each metrics as option}
            <Option value={option.value}>{option.label}</Option>
          {/each}
        </Select>
        <Select class="settings-field" label="Range" variant="outlined" bind:value={range}>
          {#each ranges as option}
            <Option value={option.value}>{option.label}</Option>
          {/each}
        </Select>
      </div>
    </div>

    <div class="chart-body">
      <div class="y-axis">
        {#each tickLabels as label}
          <span>{label}</span>
        {/each}
      </div>
      <div class="chart-area" bind:this={chartContainer}>
        <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} aria-label="Listening stats chart">
          {#each tickYs as y}
            <line x1={chartLeft} y1={y} x2={chartWidth - chartRight} y2={y} />
          {/each}
          <polyline points={points} />
          {#each series as value, index}
            <circle
              cx={chartLeft + (index * Math.max(chartWidth - chartLeft - chartRight, 1)) / (series.length - 1)}
              cy={chartBottom - (value / maxValue) * (chartBottom - chartTop)}
              r="4"
            />
          {/each}
        </svg>
        <div class="x-axis">
          {#each labels as label}
            <span>{label}</span>
          {/each}
        </div>
      </div>
    </div>
  </section>

  <section class="summary-grid">
    {#each summaryCards as card}
      <div class="summary-card">
        <div class="summary-label">{card.label}</div>
        <div class="summary-value">{card.value}</div>
      </div>
    {/each}
  </section>

  <section class="region-card">
    <div class="section-head">
      <h2>Artist and label insights</h2>
      <p>Filter performance by country, region, or city.</p>
    </div>

    <div class="region-controls">
      <Select class="settings-field" label="Country" variant="outlined" bind:value={country}>
        <Option value="Global">Global</Option>
        <Option value="United States">United States</Option>
        <Option value="Germany">Germany</Option>
        <Option value="United Kingdom">United Kingdom</Option>
        <Option value="Japan">Japan</Option>
      </Select>
      <Select class="settings-field" label="Region" variant="outlined" bind:value={region}>
        <Option value="North America">North America</Option>
        <Option value="Europe">Europe</Option>
        <Option value="Asia Pacific">Asia Pacific</Option>
        <Option value="Latin America">Latin America</Option>
        <Option value="Middle East">Middle East</Option>
      </Select>
      <Select class="settings-field" label="City" variant="outlined" bind:value={city}>
        <Option value="All cities">All cities</Option>
        <Option value="Los Angeles">Los Angeles</Option>
        <Option value="Berlin">Berlin</Option>
        <Option value="London">London</Option>
        <Option value="Tokyo">Tokyo</Option>
      </Select>
    </div>

    <div class="region-metrics">
      <div class="metric-tile">
        <span>Top artist</span>
        <strong>Artist Alpha</strong>
      </div>
      <div class="metric-tile">
        <span>Top label</span>
        <strong>Echo Label Group</strong>
      </div>
      <div class="metric-tile">
        <span>Top city</span>
        <strong>Los Angeles</strong>
      </div>
      <div class="metric-tile">
        <span>Streaming share</span>
        <strong>38%</strong>
      </div>
    </div>

    <div class="region-actions">
      <Button variant="raised"><Label>Apply filters</Label></Button>
      <Button variant="outlined"><Label>Reset</Label></Button>
    </div>
  </section>
</section>

<style>
  .listening-stats {
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

  .chart-card {
    background: #ffffff;
    border-radius: 18px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    padding: 22px;
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .chart-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
  }

  .chart-head h2 {
    margin: 0;
    font-size: 1.2rem;
  }

  .chart-head p {
    margin: 6px 0 0;
    color: #6f6f6f;
  }

  .chart-controls {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 220px));
    gap: 12px;
  }

  .chart-body {
    display: grid;
    grid-template-columns: 0px 1fr;
    gap: 8px;
    align-items: center;
  }

  .y-axis {
    display: grid;
    height: 180px;
    align-content: space-between;
    color: #8b8b8b;
    font-size: 0.8rem;
  }

  .chart-area {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  svg {
    width: 100%;
    height: 240px;
  }

  svg line {
    stroke: #e5e7ea;
    stroke-width: 1;
  }

  svg polyline {
    fill: none;
    stroke: #1db954;
    stroke-width: 3;
  }

  svg circle {
    fill: #1db954;
  }

  .x-axis {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    font-size: 0.8rem;
    color: #8b8b8b;
    text-align: center;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 16px;
  }

  .summary-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 10px 18px rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .summary-label {
    color: #6f6f6f;
    font-size: 0.85rem;
  }

  .summary-value {
    font-size: 1.3rem;
    font-weight: 600;
  }

  .region-card {
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
  }

  .section-head p {
    margin: 6px 0 0;
    color: #6f6f6f;
  }

  .region-controls {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
  }

  .region-metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
  }

  .metric-tile {
    background: #f6f8f9;
    border-radius: 12px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    color: #5c5c5c;
  }

  .metric-tile strong {
    color: #1a1a1a;
    font-size: 1rem;
  }

  .region-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }

  :global(.region-actions .mdc-button--raised) {
    background-color: #1db954;
  }

  :global(.region-actions .mdc-button) {
    border-radius: 12px;
  }

  @media (max-width: 1200px) {
    .summary-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .region-metrics {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 900px) {
    .chart-head {
      flex-direction: column;
    }

    .chart-controls {
      grid-template-columns: 1fr;
      width: 100%;
    }

    .summary-grid {
      grid-template-columns: 1fr;
    }

    .region-controls {
      grid-template-columns: 1fr;
    }
  }
</style>
