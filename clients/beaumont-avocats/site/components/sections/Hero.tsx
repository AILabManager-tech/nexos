import { useTranslations } from 'next-intl';

// Hero P14 rupture 3 — structure asymétrique (ref S23 BD&P).
// Rompt "hero centré" classique : grande typo serif display à gauche (md:col-span-7),
// bloc éditorial ivoire avec portrait alt-text à droite (md:col-span-5) — proportion 7/5.
// Pas de hero image pleine largeur bruyante. Ton juridique autorité préservé (sobriété
// chromatique, copy conservatrice et directe).
export function Hero() {
  const t = useTranslations('home.hero');

  return (
    <section
      id="top"
      className="border-b border-primary-100"
    >
      <div className="mx-auto max-w-7xl px-6 py-20 md:py-28 grid gap-12 md:grid-cols-12 md:items-end">
        <div className="md:col-span-7">
          <p className="text-xs uppercase tracking-[0.18em] text-ink-muted font-medium">
            {t('eyebrow')}
          </p>
          <h1 className="mt-6 font-display text-5xl md:text-7xl font-bold text-ink leading-[1.02]">
            {t('title_line_1')}
            <br />
            <span className="text-primary">{t('title_line_2')}</span>
            <br />
            {t('title_line_3')}
          </h1>

          <p className="mt-8 max-w-prose text-lg text-ink-soft leading-relaxed">
            {t('subtitle')}
          </p>

          <div className="mt-10 flex flex-wrap gap-3">
            <a
              href="#contact"
              className="inline-flex items-center gap-2 rounded-sm bg-primary px-6 py-3 text-sm font-medium text-surface hover:bg-primary-600 transition-colors"
            >
              {t('cta_primary')}
              <span aria-hidden="true">→</span>
            </a>
            <a
              href="#expertises"
              className="inline-flex items-center gap-2 rounded-sm border border-primary-200 bg-transparent px-6 py-3 text-sm font-medium text-ink hover:bg-surface-alt transition-colors"
            >
              {t('cta_secondary')}
            </a>
          </div>
        </div>

        <figure className="md:col-span-5 md:-mb-6">
          <div className="relative aspect-[3/4] overflow-hidden bg-surface-dark">
            {/* Placeholder éditorial noir-et-blanc : vignette texturale monochrome jusqu'au
                shoot photo du cabinet. Aspect ratio portrait 3/4 rompt le hero landscape. */}
            <div
              role="img"
              aria-label={t('portrait_alt')}
              className="absolute inset-0 bg-[radial-gradient(ellipse_at_30%_20%,rgba(107,30,35,0.20),transparent_55%),radial-gradient(ellipse_at_70%_80%,rgba(245,241,234,0.04),transparent_50%)]"
            />
            <div className="absolute inset-0 bg-[linear-gradient(130deg,rgba(10,10,10,0.82),rgba(10,10,10,0.42)_55%,rgba(43,43,43,0.62))]" />
            <div className="absolute inset-0 flex flex-col justify-end p-8">
              <p className="font-display text-surface text-lg leading-tight">
                {'« La majorité de nos mandats arrivent sur référence d\'un ancien client. »'}
              </p>
              <p className="mt-3 text-xs uppercase tracking-widest text-surface/70">
                Marie-Ève Beaumont · Associée fondatrice
              </p>
            </div>
          </div>
        </figure>
      </div>
    </section>
  );
}
