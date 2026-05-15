import { defineConfig } from 'vitest/config';

// Configuration Vitest minimale — audit dette 2026-05-15 item 2-tests.
// L'absence de tests Vitest était signalée WARNING par build_validator
// et FAIL par Ph5. Ce premier set couvre les utilitaires purs critiques
// (cn, rateLimit, cookieConsent). Étendre au fur et à mesure.
export default defineConfig({
  test: {
    include: ['__tests__/**/*.test.ts', 'lib/**/*.test.ts'],
    environment: 'node',
    globals: false,
  },
});
