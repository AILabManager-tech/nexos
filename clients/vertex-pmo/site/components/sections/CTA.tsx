import { useTranslations } from 'next-intl';

// P19 StoryBrand étape "Appel à l'action" — dernier CTA de la page, présentation du "moment
// de décision" plutôt qu'une pile de features. Deux CTAs : primaire (démo) + secondaire
// (humain). Trust line : essai gratuit 14 j + sans CC + support humain (anti-friction B2B).
export function CTA() {
  const t = useTranslations('home.cta');

  return (
    <section
      id="cta"
      className="relative overflow-hidden border-t border-surface-raised bg-surface-alt py-20 md:py-28"
    >
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,rgba(8,145,178,0.10),transparent_60%)]"
      />
      <div className="relative mx-auto max-w-3xl px-6 text-center">
        <p className="text-xs uppercase tracking-widest text-accent-soft font-medium">
          {t('eyebrow')}
        </p>
        <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
          {t('title')}
        </h2>
        <p className="mt-6 text-ink-soft leading-relaxed">{t('subtitle')}</p>

        <div className="mt-10 flex flex-wrap justify-center gap-3">
          <a
            href="mailto:hello@vertex-pmo.com?subject=Demo%20Vertex%20PMO"
            className="inline-flex items-center gap-2 rounded-sm bg-accent px-6 py-3 text-sm font-medium text-surface-dark hover:bg-accent-hover transition-colors"
          >
            {t('cta_primary')}
            <span aria-hidden="true">→</span>
          </a>
          <a
            href="mailto:hello@vertex-pmo.com?subject=Parler%20a%20un%20humain"
            className="inline-flex items-center gap-2 rounded-sm border border-surface-raised bg-transparent px-6 py-3 text-sm font-medium text-ink hover:bg-surface-raised transition-colors"
          >
            {t('cta_secondary')}
          </a>
        </div>

        <p className="mt-8 text-xs text-ink-muted">{t('trust_line')}</p>
      </div>
    </section>
  );
}
