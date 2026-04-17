import { useTranslations } from 'next-intl';
import { RevealOnScroll } from '@/components/atoms/RevealOnScroll';

// Section Contact — CTA final éditorial. Promesse directe ("le premier appel est gratuit")
// + 3 canaux (téléphone, courriel, bureau physique) avec dt/dd sobre + trust_line sur
// secret professionnel (signal spécifique secteur juridique).
export function ContactCTA() {
  const t = useTranslations('home.contact');

  return (
    <section id="contact" className="py-20 md:py-28">
      <div className="mx-auto max-w-4xl px-6">
        <RevealOnScroll>
          <p className="text-xs uppercase tracking-[0.18em] text-ink-muted font-medium">
            {t('eyebrow')}
          </p>
          <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
            {t('title')}
          </h2>
          <p className="mt-8 text-lg text-ink-soft leading-relaxed max-w-prose">{t('subtitle')}</p>
        </RevealOnScroll>

        <RevealOnScroll delayMs={120}>
          <dl className="mt-14 grid gap-6 md:grid-cols-3 border-t border-b border-primary-200 py-10">
            <div>
              <dt className="text-xs uppercase tracking-widest text-ink-muted">
                {t('phone_label')}
              </dt>
              <dd className="mt-2 font-display text-xl text-ink">
                <a href={`tel:${t('phone_value').replace(/\s/g, '')}`} className="hover:text-primary transition-colors">
                  {t('phone_value')}
                </a>
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-widest text-ink-muted">
                {t('email_label')}
              </dt>
              <dd className="mt-2 font-display text-xl text-ink break-words">
                <a href={`mailto:${t('email_value')}`} className="hover:text-primary transition-colors">
                  {t('email_value')}
                </a>
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-widest text-ink-muted">
                {t('address_label')}
              </dt>
              <dd className="mt-2 text-sm text-ink-soft leading-relaxed">{t('address_value')}</dd>
            </div>
          </dl>
        </RevealOnScroll>

        <RevealOnScroll delayMs={240}>
          <div className="mt-10 flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <a
              href={`mailto:${t('email_value')}?subject=Prise%20de%20contact%20Beaumont%20Avocats`}
              className="inline-flex items-center gap-2 rounded-sm bg-primary px-6 py-3 text-sm font-medium text-surface hover:bg-primary-600 transition-colors"
            >
              {t('cta_phone')}
              <span aria-hidden="true">→</span>
            </a>
            <p className="text-xs text-ink-muted italic max-w-md">{t('trust_line')}</p>
          </div>
        </RevealOnScroll>
      </div>
    </section>
  );
}
