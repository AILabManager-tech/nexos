// Section: S-018 | contact.ContactHero | i18n: contact.hero
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Phone, MapPin } from 'lucide-react';
import { getClientConfig, getTelHref } from '@/lib/clientConfig';

export function ContactHero() {
  const t = useTranslations('contact.hero');
  const config = getClientConfig();

  return (
    <section className="bg-background py-12 sm:py-16 lg:py-20 border-b border-border/60" aria-labelledby="contact-hero-title">
      <Container>
        <div className="space-y-6 max-w-3xl">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h1 id="contact-hero-title" className="font-heading font-bold text-4xl sm:text-5xl text-text">
            {t('title')}
          </h1>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
          <p className="text-2xl text-text font-semibold">
            {t('addressDisplay', {
              adresseLigne: config.adresseLigne,
              ville: config.ville,
            })}
          </p>
          <a
            href={getTelHref()}
            aria-label={t('phoneAria', { telephone: config.telephone })}
            className="inline-block text-2xl text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
          >
            {t('phoneDisplay', { telephone: config.telephone })}
          </a>
          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <a
              href={getTelHref()}
              className="inline-flex items-center justify-center gap-2 h-14 px-7 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
            >
              <Phone size={18} aria-hidden="true" />
              {t('ctaCall')}
            </a>
            <a
              href="#maps"
              className="inline-flex items-center justify-center gap-2 h-14 px-7 rounded font-semibold border border-primary text-primary bg-surface hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
            >
              <MapPin size={18} aria-hidden="true" />
              {t('ctaMap')}
            </a>
          </div>
        </div>
      </Container>
    </section>
  );
}
