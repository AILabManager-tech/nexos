import Image from 'next/image';
import { useTranslations } from 'next-intl';

export function Hero() {
  const t = useTranslations('home.hero');

  return (
    <section
      aria-labelledby="hero-heading"
      className="relative overflow-hidden bg-surface"
    >
      <div className="mx-auto grid max-w-7xl gap-12 px-6 py-24 md:grid-cols-2 md:items-center md:py-32">
        <div>
          <p className="text-sm uppercase tracking-widest text-primary">
            {t('eyebrow')}
          </p>
          <h1
            id="hero-heading"
            className="mt-4 text-4xl md:text-6xl leading-tight"
          >
            {t('title')}
          </h1>
          <p className="mt-6 max-w-lg text-lg text-ink-soft">
            {t('subtitle')}
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <a
              href="#contact"
              className="rounded-full bg-primary px-8 py-4 text-surface hover:bg-primary-600 transition-colors"
            >
              {t('cta_primary')}
            </a>
            <a
              href="#services"
              className="rounded-full border border-primary-300 px-8 py-4 text-ink hover:bg-surface-alt transition-colors"
            >
              {t('cta_secondary')}
            </a>
          </div>
        </div>

        {/* Pattern P04 — Hero émotionnel. TODO(client): remplacer /images/hero-therapist.jpg par une photo réelle d'une thérapeute accueillant un·e patient·e (cadre clinique chaleureux, ivoire/bois clair, AUCUN stock footage générique). Consigne : format 1200x1200, < 400 Ko (AVIF/WebP), LCP-friendly. */}
        <figure className="relative isolate">
          <div className="relative aspect-square w-full overflow-hidden rounded-3xl shadow-lg ring-1 ring-primary-100">
            <Image
              src="/images/hero-therapist.jpg"
              alt={t('image_alt')}
              fill
              sizes="(min-width: 768px) 40vw, 100vw"
              priority
              className="object-cover"
            />
            {/* Overlay doux pour garantir contraste AA si caption superposée (haut/bas = zones safe) */}
            <div
              aria-hidden="true"
              className="pointer-events-none absolute inset-x-0 bottom-0 h-28 bg-gradient-to-t from-ink/70 via-ink/20 to-transparent"
            />
            <figcaption className="absolute inset-x-6 bottom-6 text-sm text-surface drop-shadow-md">
              {t('image_caption')}
            </figcaption>
          </div>
        </figure>
      </div>
    </section>
  );
}
