import { useTranslations } from 'next-intl';
import { Zap } from 'lucide-react';

export function Hero() {
  const t = useTranslations('home.hero');

  return (
    <section
      aria-labelledby="hero-heading"
      className="relative overflow-hidden bg-surface"
    >
      {/* Accent décoratif or (D4_palette=industrial : noir + accent saturé discret).
          asymmetric-strong : band oblique en fond, opacité basse pour ne pas dominer. */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage:
            'linear-gradient(135deg, transparent 45%, #D4AF37 45%, #D4AF37 46%, transparent 46%)'
        }}
      />
      <div className="relative mx-auto grid max-w-7xl gap-12 px-6 py-24 md:grid-cols-5 md:items-center md:py-32">
        <div className="md:col-span-3">
          <p className="flex items-center gap-2 text-sm uppercase tracking-[0.3em] text-accent">
            <Zap aria-hidden="true" className="h-4 w-4" />
            {t('eyebrow')}
          </p>
          <h1
            id="hero-heading"
            className="mt-4 text-4xl md:text-6xl leading-[1.05]"
          >
            {t('title')}
          </h1>
          <p className="mt-6 max-w-xl text-lg text-ink-soft">
            {t('subtitle')}
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <a
              href="#contact"
              className="rounded-sm bg-primary px-8 py-4 text-ink hover:bg-primary-600 transition-colors"
            >
              {t('cta_primary')}
            </a>
            <a
              href="#projects"
              className="rounded-sm border border-primary-700 px-8 py-4 text-ink hover:bg-surface-raised transition-colors"
            >
              {t('cta_secondary')}
            </a>
          </div>
        </div>

        {/* Colonne stat : legacy authority en mode minimal (D1_density=5, heavy).
            TODO(client): remplacer par une photo de chantier industriel en N&B (cohérent avec P06
            galerie) — dimensions 900×1100, AVIF/WebP, < 400 Ko. */}
        <aside className="md:col-span-2 md:-mr-6 md:-my-12">
          <div className="border-l-4 border-accent bg-surface-alt p-8 md:p-10">
            <p className="font-heading text-6xl md:text-7xl text-ink">22</p>
            <p className="mt-2 text-sm uppercase tracking-widest text-ink-muted">
              {t('stat_years')}
            </p>
            <div className="my-8 h-px bg-primary-800" />
            <p className="font-heading text-6xl md:text-7xl text-ink">24/7</p>
            <p className="mt-2 text-sm uppercase tracking-widest text-ink-muted">
              {t('stat_availability')}
            </p>
          </div>
        </aside>
      </div>
    </section>
  );
}
