import { useTranslations } from 'next-intl';
import Image from 'next/image';

export function Hero() {
  const t = useTranslations('home.hero');

  return (
    <section
      aria-labelledby="hero-heading"
      className="relative overflow-hidden bg-surface"
    >
      <div className="mx-auto grid max-w-7xl gap-12 px-6 py-20 md:grid-cols-12 md:items-end md:py-28 md:gap-20">
        <div className="md:col-span-7">
          <p className="text-sm uppercase tracking-[0.3em] text-accent-deep">
            {t('eyebrow')}
          </p>
          <h1
            id="hero-heading"
            className="mt-6 font-display text-5xl leading-[1.02] md:text-7xl"
          >
            {t('title_line_1')}
            <span className="mt-2 block italic font-normal text-primary">
              {t('title_line_2')}
            </span>
          </h1>
          <p className="mt-8 max-w-editorial text-lg text-ink-soft leading-relaxed">
            {t('subtitle')}
          </p>
        </div>

        {/* Figure éditoriale minimale — D1_density=2, asymmetric-soft (D6).
            TODO(client) : remplacer par une photo produit ou terroir (verre de vin, pain chaud,
            ingrédient signature) 1200×1500, AVIF/WebP, < 350 Ko. */}
        <figure className="relative md:col-span-5 md:-mb-20 md:translate-y-8">
          <div className="relative aspect-[4/5] w-full overflow-hidden">
            <Image
              src="/images/hero-still-life.svg"
              alt={t('image_alt')}
              fill
              sizes="(min-width: 768px) 35vw, 100vw"
              priority
              className="object-cover"
            />
          </div>
          <figcaption className="sr-only">{t('image_caption')}</figcaption>
        </figure>
      </div>
    </section>
  );
}
