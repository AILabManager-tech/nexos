import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Dépanneur Nobert',
    short_name: 'Nobert',
    description:
      'Votre dépanneur de quartier authentique. Promotions, bières, lotto, snacks.',
    start_url: '/fr',
    display: 'standalone',
    background_color: '#FFF8E7',
    theme_color: '#8B4513',
    icons: [
      { src: '/icon.svg', sizes: 'any', type: 'image/svg+xml' },
      { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
  };
}
