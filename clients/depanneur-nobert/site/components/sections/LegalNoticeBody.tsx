// Section: S-024 | mentions-legales.MentionsContent | i18n: legal.notice
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { getClientConfig } from '@/lib/clientConfig';

export function LegalNoticeBody() {
  const t = useTranslations('legal.notice');
  const config = getClientConfig();
  const dateMaj = new Date().toISOString().slice(0, 10);

  return (
    <section className="bg-surface py-12 sm:py-16" aria-labelledby="notice-title">
      <Container>
        <article className="max-w-3xl space-y-8 text-base leading-relaxed text-text">
          <header className="space-y-3">
            <h1 id="notice-title" className="font-heading font-bold text-4xl text-text">
              {t('title')}
            </h1>
            <p className="text-small text-text-muted">{t('lastUpdate', { dateMaj })}</p>
          </header>

          <p>{t('intro')}</p>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('editorTitle')}</h2>
            <p>{t('editorBody')}</p>
            <dl className="space-y-2">
              <div>
                <dt className="inline font-semibold">{t('editorName')}</dt>
              </div>
              <div>
                <dt className="inline font-semibold">{t('editorNeqLabel')} : </dt>
                <dd className="inline">{t('editorNeqValue', { NEQ: config.NEQ })}</dd>
              </div>
              <div>
                <dt className="inline font-semibold">{t('editorAddressLabel')} : </dt>
                <dd className="inline">
                  {t('editorAddressValue', {
                    adresseLigne: config.adresseLigne,
                    ville: config.ville,
                    codePostal: config.codePostal,
                  })}
                </dd>
              </div>
              <div>
                <dt className="inline font-semibold">{t('editorPhoneLabel')} : </dt>
                <dd className="inline">{t('editorPhoneValue', { telephone: config.telephone })}</dd>
              </div>
              <div>
                <dt className="inline font-semibold">{t('editorEmailLabel')} : </dt>
                <dd className="inline">
                  <a
                    href={`mailto:${config.email}`}
                    className="text-primary hover:underline"
                  >
                    {t('editorEmailValue', { email: config.email })}
                  </a>
                </dd>
              </div>
              <div>
                <dt className="inline font-semibold">{t('editorRepresentativeLabel')} : </dt>
                <dd className="inline">{t('editorRepresentativeValue')}</dd>
              </div>
            </dl>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('hostingTitle')}</h2>
            <p>{t('hostingBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('ipTitle')}</h2>
            <p>{t('ipBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('linksTitle')}</h2>
            <p>{t('linksBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('liabilityTitle')}</h2>
            <p>{t('liabilityBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('applicableLawTitle')}</h2>
            <p>{t('applicableLawBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('alcoholNoticeTitle')}</h2>
            <p>{t('alcoholNoticeBody')}</p>
          </section>

          <section className="space-y-3">
            <h2 className="font-heading font-bold text-2xl text-text">{t('contactTitle')}</h2>
            <p>
              {t('contactBody', {
                email: config.email,
                telephone: config.telephone,
              })}
            </p>
          </section>
        </article>
      </Container>
    </section>
  );
}
