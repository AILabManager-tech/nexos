import { useTranslations } from 'next-intl';
import { InteractiveDemo } from './InteractiveDemo';

// Hero StoryBrand (P19 — ref S19 Bop Design) :
// - Eyebrow : positionnement client/secteur (SEC-04 PME services).
// - H1 : question frame orientée profitabilité (ref S18 Productive.io).
// - Subtitle : 1 ligne bénéfice mesurable sans jargon SaaS.
// - 2 CTAs : primaire "démo" + secondaire "tarifs" (StoryBrand plan étape 1 → action).
// - Trust line : chiffre + certif + hébergement (confiance B2B).
// Inclut P10 InteractiveDemo À DROITE dans le fold (ref S17 Monday.com — pas un screenshot).
export function Hero() {
  const t = useTranslations('home.hero');

  return (
    <section
      id="top"
      className="relative overflow-hidden border-b border-surface-raised"
    >
      {/* Glow subtil — signal SaaS technique sans surcharge visuelle. */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(8,145,178,0.08),transparent_60%)]"
      />

      <div className="relative mx-auto max-w-7xl px-6 py-16 md:py-24 grid gap-12 md:grid-cols-2 md:items-center">
        <div>
          <p className="inline-flex items-center gap-2 rounded-full border border-surface-raised bg-surface-alt px-3 py-1 text-xs font-medium text-accent-soft">
            <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-accent animate-pulse" />
            {t('eyebrow')}
          </p>

          <h1 className="mt-6 font-display text-5xl md:text-6xl font-bold text-ink leading-[1.05]">
            {t('title_line_1')}
            <br />
            <span className="text-accent">{t('title_line_2')}</span>
          </h1>

          <p className="mt-6 max-w-prose text-lg text-ink-soft leading-relaxed">
            {t('subtitle')}
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="#cta"
              className="inline-flex items-center gap-2 rounded-sm bg-accent px-6 py-3 text-sm font-medium text-surface-dark hover:bg-accent-hover transition-colors"
            >
              {t('cta_primary')}
              <span aria-hidden="true">→</span>
            </a>
            <a
              href="#how"
              className="inline-flex items-center gap-2 rounded-sm border border-surface-raised bg-transparent px-6 py-3 text-sm font-medium text-ink hover:bg-surface-alt transition-colors"
            >
              {t('cta_secondary')}
            </a>
          </div>

          <p className="mt-8 text-xs text-ink-muted">{t('trust_line')}</p>
        </div>

        <div id="demo" className="md:pl-4">
          <InteractiveDemo />
        </div>
      </div>
    </section>
  );
}
