// Section: S-023 | politique-confidentialite.PolitiqueContent | i18n: legal.privacy
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { getClientConfig } from '@/lib/clientConfig';

const DATA_KEYS = [
  'newsletter',
  'contact',
  'phoneOrder',
  'analytics',
  'cookiesEssentials',
] as const;

const THIRD_PARTY_KEYS = ['vercel', 'googleAnalytics', 'googleMaps', 'resend'] as const;

const RIGHTS_KEYS = [
  'access',
  'rectification',
  'deletion',
  'portability',
  'withdraw',
  'complaint',
  'deindex',
] as const;

export function PrivacyPolicyBody() {
  const t = useTranslations('legal.privacy');
  const config = getClientConfig();
  const dateMaj = new Date().toISOString().slice(0, 10);

  return (
    <section className="bg-surface py-12 sm:py-16" aria-labelledby="privacy-title">
      <Container>
        <article className="max-w-3xl space-y-8 text-base leading-relaxed text-text">
          <header className="space-y-3">
            <h1 id="privacy-title" className="font-heading font-bold text-4xl text-text">
              {t('title')}
            </h1>
            <p className="text-small text-text-muted">{t('lastUpdate', { dateMaj })}</p>
          </header>

          <p>{t('intro')}</p>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('rppTitle')}</h2>
            <p>{t('rppBody')}</p>
            <ul className="list-none space-y-1 ml-0">
              <li><strong>{t('rppName')}</strong> — {t('rppRole')}</li>
              <li>
                <a
                  href={`mailto:${config.rppEmail}`}
                  className="text-primary font-semibold hover:underline"
                >
                  {t('rppEmail', { rppEmail: config.rppEmail })}
                </a>
              </li>
              <li>{t('rppAddress', {
                adresseLigne: config.adresseLigne,
                ville: config.ville,
                codePostal: config.codePostal,
              })}</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('dataTitle')}</h2>
            <p>{t('dataIntro')}</p>
            <dl className="space-y-4">
              {DATA_KEYS.map((key) => (
                <div key={key} className="rounded border border-border p-4 bg-background-alt/40">
                  <dt className="font-semibold text-text">{t(`dataItems.${key}.label`)}</dt>
                  <dd className="text-text-muted mt-1">
                    <strong>{t(`dataItems.${key}.fields`)}</strong>{' '}
                    {t(`dataItems.${key}.purpose`)}{' '}
                    <em>{t(`dataItems.${key}.retention`)}</em>
                  </dd>
                </div>
              ))}
            </dl>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('purposesTitle')}</h2>
            <p>{t('purposesBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('consentTitle')}</h2>
            <p>{t('consentBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('thirdPartiesTitle')}</h2>
            <p>{t('thirdPartiesIntro')}</p>
            <ul className="space-y-3 ml-0 list-none">
              {THIRD_PARTY_KEYS.map((key) => (
                <li key={key} className="rounded border border-border p-4 bg-background-alt/40">
                  <strong>{t(`thirdPartiesItems.${key}.name`)}</strong> ({t(`thirdPartiesItems.${key}.country`)}) —{' '}
                  {t(`thirdPartiesItems.${key}.service`)} : {t(`thirdPartiesItems.${key}.purpose`)}
                </li>
              ))}
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('transferTitle')}</h2>
            <p>{t('transferBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('rightsTitle')}</h2>
            <p>{t('rightsIntro')}</p>
            <ul className="list-disc pl-6 space-y-2">
              {RIGHTS_KEYS.map((key) => (
                <li key={key}>{t(`rightsItems.${key}`)}</li>
              ))}
            </ul>
            <p className="text-small text-text-muted">{t('rightsResponseTime')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('incidentTitle')}</h2>
            <p>{t('incidentBody', { rppEmail: config.rppEmail })}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('securityTitle')}</h2>
            <p>{t('securityBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('minorsTitle')}</h2>
            <p>{t('minorsBody', { rppEmail: config.rppEmail })}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('updatesTitle')}</h2>
            <p>{t('updatesBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('contactTitle')}</h2>
            <p>{t('contactBody', {
              rppEmail: config.rppEmail,
              adresseLigne: config.adresseLigne,
              ville: config.ville,
              codePostal: config.codePostal,
            })}</p>
          </section>
        </article>
      </Container>
    </section>
  );
}
