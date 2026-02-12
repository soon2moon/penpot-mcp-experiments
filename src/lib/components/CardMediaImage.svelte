<script lang="ts">
import { Media, MediaContent } from '@smui/card';

export let src: string | null | undefined = null;
export let alt = '';
export let aspectRatio: '16x9' | 'square' = '16x9';
export let icon: string = 'image';
export let eager = false;

let loaded = false;
let errored = false;

const handleLoad = () => (loaded = true);
const handleError = () => {
    errored = true;
    loaded = true;
};
</script>

<Media aspectRatio={aspectRatio} class="media">
    <MediaContent class="content">
        {#if src && !errored}
            <img
                class="img"
                src={src}
                alt={alt}
                loading={eager ? 'eager' : 'lazy'}
                decoding="async"
                on:load={handleLoad}
                on:error={handleError}
            />
        {/if}

        {#if !src || errored || !loaded}
            <div class="placeholder" aria-hidden="true">
                <span class="material-icons">{icon}</span>
            </div>
        {/if}
    </MediaContent>
</Media>

<style>
.media :global(.mdc-card__media) {
    position: relative;
    overflow: hidden;
    background: #222;
}

.content {
    height: 100%;
}

.img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.placeholder {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0.06),
        rgba(255, 255, 255, 0.12),
        rgba(255, 255, 255, 0.06)
        );
    background-size: 200% 100%;
    animation: shimmer 1.2s linear infinite;
}

.placeholder :global(.material-icons) {
    opacity: 0.6;
}

@keyframes shimmer {
0% { background-position: 200% 0; }
100% { background-position: -200% 0; }
}
</style>

