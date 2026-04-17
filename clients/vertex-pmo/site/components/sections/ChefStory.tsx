import Image from 'next/image';
import { useTranslations } from 'next-intl';

// Pattern P08 — Story-first design (ref S15 Fiola, fioladc.com)
//
// Règle impérative verbatim (web-patterns-reference.md §P08) :
//   "Story-first design — le parcours et la philosophie avant le menu" (Fiola)
//
// Placement : ENTRE Hero et MenuGallery. L'investissement émotionnel précède l'exposition
// produit. La CTA de réservation (Reservation section) est placée APRÈS le menu pour
// capitaliser sur la projection narrative + appétit visuel.
//
// Anti-patterns évités :
//   - Pas de corporate-speak ("Notre mission est de…")
//   - Copy éditoriale 2-3 paragraphes (pas liste à puces marketing)
//   - Photo terroir/humaine (pas stock)

export function ChefStory() {
  const t = useTranslations('home.chefStory');

  return (
    <section
      id="histoire"
      aria-labelledby="chef-story-heading"
      className="bg-surface-alt"
    >
      <div className="mx-auto max-w-7xl px-6 py-24 md:py-32">
        <div className="grid gap-12 md:grid-cols-12 md:items-center md:gap-16">
          {/* Portrait — asymétrie D6 asymmetric-soft : figure débordant légèrement en haut. */}
          <figure className="md:col-span-5 md:-mt-12">
            <div className="relative aspect-[4/5] w-full overflow-hidden">
              <Image
                src="/images/chef-portrait.svg"
                alt={t('image_alt')}
                fill
                sizes="(min-width: 768px) 35vw, 100vw"
                className="object-cover"
              />
            </div>
            <figcaption className="mt-4 text-xs uppercase tracking-widest text-ink-muted">
              {t('image_caption')}
            </figcaption>
          </figure>

          <div className="md:col-span-7 md:pl-6">
            <p className="text-sm uppercase tracking-[0.3em] text-accent-deep">
              {t('eyebrow')}
            </p>
            <h2
              id="chef-story-heading"
              className="mt-4 font-display text-4xl leading-[1.05] md:text-5xl"
            >
              {t('title')}
            </h2>

            <div className="mt-10 space-y-6 text-lg leading-relaxed text-ink-soft">
              <p>{t('p1')}</p>
              <p>{t('p2')}</p>
              <p className="italic text-primary">{t('p3_quote')}</p>
            </div>

            <p className="mt-12 text-sm text-ink-muted">
              <span className="mr-2 font-display not-italic text-ink">
                {t('signature_name')}
              </span>
              · {t('signature_role')}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
