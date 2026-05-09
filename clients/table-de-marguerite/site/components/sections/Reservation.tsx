import { useTranslations } from 'next-intl';
import { Phone, Mail } from 'lucide-react';

/**
 * CTA réservation — S-004 (page home, ordre 4).
 *
 * Placée APRÈS le menu (P08 + P20 capitalisent sur l'investissement narratif
 * cheffe + appétit visuel galerie). Deux CTA primaires : tel: et mailto: —
 * volontairement pas de plateforme de réservation tierce (positionnement
 * premium artisanal). Trust line affiche les heures d'ouverture.
 */
export function Reservation() {
  const t = useTranslations('home.reservation');

  return (
    <section
      id="reservation"
      aria-labelledby="reservation-heading"
      className="bg-surface-alt"
    >
      <div className="mx-auto max-w-5xl px-6 py-24 md:py-32">
        <div className="text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-accent-deep">
            {t('eyebrow')}
          </p>
          <h2 id="reservation-heading" className="mt-4 font-display text-4xl md:text-6xl">
            {t('title')}
          </h2>
          <p className="mx-auto mt-6 max-w-editorial text-lg text-ink-soft leading-relaxed">
            {t('subtitle')}
          </p>
        </div>

        <div className="mt-14 flex flex-wrap justify-center gap-5">
          <a
            href={`tel:${t('phone').replace(/\s/g, '')}`}
            className="inline-flex items-center gap-3 rounded-sm bg-primary px-8 py-4 text-surface hover:bg-primary-600 transition-colors"
          >
            <Phone aria-hidden="true" className="h-5 w-5" />
            {t('cta_phone')}
          </a>
          <a
            href={`mailto:${t('email')}`}
            className="inline-flex items-center gap-3 rounded-sm border border-primary-300 px-8 py-4 text-ink hover:bg-surface-raised transition-colors"
          >
            <Mail aria-hidden="true" className="h-5 w-5 text-accent-deep" />
            {t('cta_email')}
          </a>
        </div>

        <p className="mt-10 text-center text-sm text-ink-muted italic">
          {t('trust_line')}
        </p>
      </div>
    </section>
  );
}
