// Section: S-005 | home.InfosPratiques | i18n: home.infosPratiques
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { MapPin, Phone } from 'lucide-react';
import { HoursTable } from '@/components/sections/HoursTable';
import { getClientConfig, getTelHref } from '@/lib/clientConfig';

export function InfosPratiques() {
  const t = useTranslations('home.infosPratiques');
  const config = getClientConfig();

  return (
    <section className="bg-background py-12 sm:py-16 lg:py-20" aria-labelledby="infos-title">
      <Container>
        <div className="max-w-3xl space-y-3 mb-10">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h2 id="infos-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          <div className="space-y-6">
            <div>
              <h3 className="text-small uppercase tracking-wider text-text-muted font-semibold">
                {t('addressLabel')}
              </h3>
              <p className="text-lg text-text mt-1">
                {t('addressLine', {
                  adresseLigne: config.adresseLigne,
                  ville: config.ville,
                  codePostal: config.codePostal,
                })}
              </p>
            </div>
            <div>
              <h3 className="text-small uppercase tracking-wider text-text-muted font-semibold">
                {t('phoneLabel')}
              </h3>
              <a
                href={getTelHref()}
                aria-label={t('phoneAria', { telephone: config.telephone })}
                className="text-lg text-primary font-semibold mt-1 inline-block hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
              >
                {t('phoneValue', { telephone: config.telephone })}
              </a>
            </div>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/contact"
                className="inline-flex items-center justify-center gap-2 h-12 px-5 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                <MapPin size={18} aria-hidden="true" />
                {t('ctaMap')}
              </Link>
              <a
                href={getTelHref()}
                className="inline-flex items-center justify-center gap-2 h-12 px-5 rounded font-semibold border border-primary text-primary bg-surface hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                <Phone size={18} aria-hidden="true" />
                {t('ctaCall')}
              </a>
            </div>
          </div>
          <div className="bg-surface border border-border rounded-lg p-6">
            <h3 className="text-small uppercase tracking-wider text-text-muted font-semibold mb-3">
              {t('hoursLabel')}
            </h3>
            <HoursTable caption={t('hoursLabel')} />
            <p className="text-small text-text-muted mt-4">{t('hoursNote')}</p>
          </div>
        </div>
      </Container>
    </section>
  );
}
