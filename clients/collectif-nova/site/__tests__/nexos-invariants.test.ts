// Tests d'invariants structurels NEXOS — protection régression CI.
// P9 D1 pilote : valider que la génération NEXOS reste conforme au contrat
// (sécurité headers, next.config durci, i18n FR/EN, pages Loi 25, middleware,
// robots/sitemap). Ne teste pas du code métier (vertex-pmo n'en a pas) — teste
// que les invariants de plateforme tiennent dans le temps.
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const root = resolve(__dirname, '..');
const read = (relpath: string) => readFileSync(resolve(root, relpath), 'utf8');

describe('vercel.json — headers sécurité', () => {
  const vercel = JSON.parse(read('vercel.json')) as {
    headers: Array<{ source: string; headers: Array<{ key: string; value: string }> }>;
  };
  const root = vercel.headers.find((h) => h.source === '/(.*)');

  it('contient une règle pour /(.*)', () => {
    expect(root).toBeDefined();
  });

  it('contient les 7 headers sécurité obligatoires', () => {
    const keys = root!.headers.map((h) => h.key);
    expect(keys).toEqual(
      expect.arrayContaining([
        'X-Content-Type-Options',
        'X-Frame-Options',
        'Referrer-Policy',
        'Permissions-Policy',
        'X-DNS-Prefetch-Control',
        'Strict-Transport-Security',
        'Content-Security-Policy',
      ]),
    );
  });

  it('X-Content-Type-Options = nosniff', () => {
    const h = root!.headers.find((x) => x.key === 'X-Content-Type-Options');
    expect(h?.value).toBe('nosniff');
  });

  it('X-Frame-Options = DENY', () => {
    const h = root!.headers.find((x) => x.key === 'X-Frame-Options');
    expect(h?.value).toBe('DENY');
  });

  it("CSP contient les directives anti-clickjacking et anti-injection (frame-ancestors 'none', base-uri 'self', form-action 'self')", () => {
    const csp = root!.headers.find((x) => x.key === 'Content-Security-Policy')?.value ?? '';
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp).toContain("base-uri 'self'");
    expect(csp).toContain("form-action 'self'");
  });

  it('HSTS configure max-age >= 1 an avec includeSubDomains + preload', () => {
    const hsts = root!.headers.find((x) => x.key === 'Strict-Transport-Security')?.value ?? '';
    expect(hsts).toMatch(/max-age=\d{8,}/);
    expect(hsts).toContain('includeSubDomains');
    expect(hsts).toContain('preload');
  });

  it('Cache-Control sur /_next/static utilise immutable', () => {
    const staticRule = vercel.headers.find((h) => h.source === '/_next/static/(.*)');
    const cc = staticRule?.headers.find((h) => h.key === 'Cache-Control')?.value ?? '';
    expect(cc).toContain('immutable');
    expect(cc).toContain('max-age=31536000');
  });
});

describe('next.config.mjs — durcissement', () => {
  const cfg = read('next.config.mjs');

  it('poweredByHeader = false (ne révèle pas le framework)', () => {
    expect(cfg).toMatch(/poweredByHeader\s*:\s*false/);
  });

  it('reactStrictMode = true', () => {
    expect(cfg).toMatch(/reactStrictMode\s*:\s*true/);
  });

  it('images.formats inclut avif + webp', () => {
    expect(cfg).toContain("'image/avif'");
    expect(cfg).toContain("'image/webp'");
  });
});

describe('i18n/routing.ts — locales FR/EN', () => {
  const routing = read('i18n/routing.ts');

  it("déclare locales FR et EN", () => {
    expect(routing).toMatch(/locales\s*:\s*\[\s*['"]fr['"]\s*,\s*['"]en['"]\s*\]/);
  });

  it("defaultLocale = 'fr'", () => {
    expect(routing).toMatch(/defaultLocale\s*:\s*['"]fr['"]/);
  });
});

describe('Loi 25 — pages obligatoires présentes', () => {
  it('politique de confidentialité existe sous [locale]/', () => {
    expect(existsSync(resolve(root, 'app/[locale]/politique-confidentialite/page.tsx'))).toBe(true);
  });

  it('mentions légales existent sous [locale]/', () => {
    expect(existsSync(resolve(root, 'app/[locale]/mentions-legales/page.tsx'))).toBe(true);
  });
});

describe('middleware.ts — routage i18n', () => {
  const mw = read('middleware.ts');

  it('importe createMiddleware depuis next-intl/middleware', () => {
    expect(mw).toMatch(/from\s+['"]next-intl\/middleware['"]/);
  });

  it('matcher exclut /api, /_next, /_vercel et les fichiers statiques', () => {
    expect(mw).toMatch(/matcher\s*:/);
    // Exclusions canoniques du matcher NEXOS (cf templates/next-config.template.mjs)
    expect(mw).toContain('api');
    expect(mw).toContain('_next');
    expect(mw).toContain('_vercel');
  });
});

describe('robots.ts + sitemap.ts — SEO', () => {
  it('app/robots.ts existe et exporte default', () => {
    const robots = read('app/robots.ts');
    expect(robots).toMatch(/export\s+default\s+(async\s+)?function/);
  });

  it('app/sitemap.ts existe et exporte default', () => {
    const sitemap = read('app/sitemap.ts');
    expect(sitemap).toMatch(/export\s+default\s+(async\s+)?function/);
  });
});
