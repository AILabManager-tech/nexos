import { defineConfig } from 'vitest/config';
import path from 'node:path';

export default defineConfig({
  test: {
    environment: 'node',
    globals: false,
    include: ['tests/**/*.{test,spec}.ts', 'tests/**/*.{test,spec}.tsx'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      include: ['lib/**/*.ts'],
      exclude: ['lib/**/*.d.ts', 'lib/site-info.ts', 'lib/seo.ts', 'lib/structured-data.ts', 'lib/promotions.ts', 'lib/products.ts', 'lib/consent.ts'],
      thresholds: {
        statements: 80,
        branches: 70,
        functions: 80,
        lines: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '.'),
    },
  },
});
