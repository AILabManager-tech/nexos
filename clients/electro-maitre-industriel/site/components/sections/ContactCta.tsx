import { useTranslations } from 'next-intl';
import { AlertTriangle } from 'lucide-react';

export function ContactCta() {
  const t = useTranslations('home.contactCta');

  return (
    <section
      id="contact"
      aria-labelledby="contact-cta-heading"
      className="bg-surface-alt"
    >
      <div className="mx-auto max-w-5xl px-6 py-24">
        <div className="border-l-4 border-accent pl-8">
          <p className="text-sm uppercase tracking-[0.3em] text-accent">
            {t('eyebrow')}
          </p>
          <h2 id="contact-cta-heading" className="mt-4 text-3xl md:text-5xl">
            {t('title')}
          </h2>
          <p className="mt-4 text-ink-soft max-w-2xl">{t('subtitle')}</p>

          <div className="mt-10 flex flex-wrap gap-4">
            <a
              href={`mailto:${t('email')}`}
              className="rounded-sm bg-primary px-8 py-4 text-ink hover:bg-primary-600 transition-colors"
            >
              {t('cta_primary')}
            </a>
            <a
              href={`tel:${t('phone').replace(/\s/g, '')}`}
              className="inline-flex items-center gap-2 rounded-sm border border-primary-700 px-8 py-4 text-ink hover:bg-surface-raised transition-colors"
            >
              <AlertTriangle aria-hidden="true" className="h-4 w-4 text-accent" />
              {t('cta_secondary')}
            </a>
          </div>

          <p className="mt-6 text-xs text-ink-muted">
            {t('trust_line')}
          </p>
        </div>
      </div>
    </section>
  );
}
