import { resolve } from 'node:path';
import { defineConfig } from 'vitest/config';

// Configuration Vitest — couvre utilitaires purs (lib/) + Zod schemas + API
// helpers (P4c étend la couverture initiale audit dette 2026-05-15).
// L'alias @/* doit matcher tsconfig.json (paths) pour que les imports type
// `@/data/promotions.json` résolvent en test comme en build Next.
export default defineConfig({
  test: {
    include: ['__tests__/**/*.test.ts', 'lib/**/*.test.ts'],
    environment: 'node',
    globals: false,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, '.'),
    },
  },
});
