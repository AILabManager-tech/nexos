import { useTranslations } from 'next-intl';
import { Quote } from 'lucide-react';

// Pattern P02 — Social proof adjacente au CTA (Bloor Jane S05 : +2× leads/mois).
// Proximité imposée : témoignages ET CTA dans la MÊME section, MÊME viewport
// (2 colonnes desktop, stack mobile). Loi 25 : prénom + initiale + ville uniquement
// (pas d'adresse complète, pas de photo sans consentement signé).

type TestimonialKey = 'marie' | 'julien' | 'sophie';
const TESTIMONIAL_KEYS: TestimonialKey[] = ['marie', 'julien', 'sophie'];

export function TestimonialsAdjacentCta() {
  const t = useTranslations('home.testimonialsCta');

  return (
    <section
      id="contact"
      aria-labelledby="testimonials-cta-heading"
      className="bg-surface"
    >
      <div className="mx-auto max-w-7xl px-6 py-24">
        <h2 id="testimonials-cta-heading" className="sr-only">
          {t('sr_heading')}
        </h2>

        <div className="grid gap-12 md:grid-cols-2 md:items-center">
          {/* Colonne témoignages — "social proof" */}
          <ul className="space-y-6" aria-label={t('testimonials_aria_label')}>
            {TESTIMONIAL_KEYS.map((key) => (
              <li
                key={key}
                className="rounded-3xl bg-surface-alt p-6 ring-1 ring-primary-100"
              >
                <Quote
                  aria-hidden="true"
                  className="h-6 w-6 text-primary"
                />
                <blockquote className="mt-3 text-ink">
                  <p className="italic">“{t(`items.${key}.quote`)}”</p>
                </blockquote>
                <figcaption className="mt-4 text-sm text-ink-muted">
                  <strong className="not-italic text-ink-soft">
                    {t(`items.${key}.author`)}
                  </strong>
                  {' · '}
                  {t(`items.${key}.role`)}
                </figcaption>
              </li>
            ))}
          </ul>

          {/* Colonne CTA — "call to action adjacent" */}
          <div className="md:pl-8">
            <p className="text-sm uppercase tracking-widest text-primary">
              {t('eyebrow')}
            </p>
            <p className="mt-4 font-heading text-3xl md:text-5xl text-ink">
              {t('title')}
            </p>
            <p className="mt-4 text-ink-soft">{t('subtitle')}</p>

            <div className="mt-10 flex flex-wrap gap-4">
              <a
                href="https://clinique-aura.ca/rdv"
                className="rounded-full bg-primary px-8 py-4 text-surface hover:bg-primary-600 transition-colors"
              >
                {t('cta_primary')}
              </a>
              <a
                href="tel:+15145550199"
                className="rounded-full border border-primary-300 px-8 py-4 text-ink hover:bg-surface-alt transition-colors"
              >
                {t('cta_secondary')}
              </a>
            </div>

            <p className="mt-6 text-xs text-ink-muted">
              {t('trust_line')}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
