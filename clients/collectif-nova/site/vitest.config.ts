import { resolve } from 'node:path';
import { defineConfig } from 'vitest/config';

// NEXOS invariants tests — protection régression CI sur le contrat de génération
// (headers sécurité, next.config sécurisé, i18n FR/EN, pages Loi 25, middleware,
// robots/sitemap). P9 D1 pilote — voir ROADMAP.md.
export default defineConfig({
  test: {
    include: ['__tests__/**/*.test.ts'],
    environment: 'node',
    globals: false,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, '.'),
    },
  },
});
