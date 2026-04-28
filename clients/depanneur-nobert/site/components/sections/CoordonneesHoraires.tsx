// Section: S-019 | contact.CoordonneesHoraires | i18n: contact.coordonnees
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { HoursTable } from '@/components/sections/HoursTable';
import { getClientConfig, getTelHref } from '@/lib/clientConfig';

export function CoordonneesHoraires() {
  const t = useTranslations('contact.coordonnees');
  const config = getClientConfig();

  return (
    <section className="bg-surface py-12 sm:py-16" aria-labelledby="coord-title">
      <Container>
        <div className="max-w-3xl space-y-3 mb-10">
          <h2 id="coord-title" className="font-heading font-bold text-3xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>
        <div className="grid gap-8 lg:grid-cols-2">
          <dl className="space-y-5">
            <div>
              <dt className="text-small uppercase tracking-wider text-text-muted font-semibold">
                {t('addressLabel')}
              </dt>
              <dd className="text-lg text-text mt-1">
                {t('addressLine', {
                  adresseLigne: config.adresseLigne,
                  ville: config.ville,
                  codePostal: config.codePostal,
                })}
              </dd>
            </div>
            <div>
              <dt className="text-small uppercase tracking-wider text-text-muted font-semibold">
                {t('phoneLabel')}
              </dt>
              <dd className="mt-1">
                <a
                  href={getTelHref()}
                  className="text-lg text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
                >
                  {t('phoneValue', { telephone: config.telephone })}
                </a>
              </dd>
            </div>
            <div>
              <dt className="text-small uppercase tracking-wider text-text-muted font-semibold">
                {t('emailLabel')}
              </dt>
              <dd className="mt-1">
                <a
                  href={`mailto:${config.email}`}
                  className="text-lg text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
                >
                  {t('emailValue', { email: config.email })}
                </a>
              </dd>
            </div>
          </dl>
          <div className="space-y-3">
            <h3 className="text-small uppercase tracking-wider text-text-muted font-semibold">
              {t('hoursLabel')}
            </h3>
            <HoursTable caption={t('hoursTableCaption')} />
            <h3 className="text-small uppercase tracking-wider text-text-muted font-semibold mt-6">
              {t('specialClosuresTitle')}
            </h3>
            <p className="text-base text-text-muted">{t('specialClosuresNote')}</p>
          </div>
        </div>
      </Container>
    </section>
  );
}
