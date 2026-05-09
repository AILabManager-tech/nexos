import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { getSiteInfo } from '@/lib/site-info';

export function RppMention() {
  const t = useTranslations('contact.rpp');
  const info = getSiteInfo();

  return (
    <Section data-manifest-id="S-016" aria-labelledby="rpp-title">
      <Container className="max-w-3xl">
        <h2 id="rpp-title" className="font-heading text-h2 text-text">
          {t('title')}
        </h2>
        <p className="mt-3 max-w-prose text-text-muted">{t('body')}</p>
        <dl className="mt-6 grid gap-3 text-sm">
          <div className="flex flex-wrap gap-2">
            <dt className="font-semibold text-text">{t('rppNameLabel')} :</dt>
            <dd className="text-text-muted">{info.rppName}</dd>
          </div>
          <div className="flex flex-wrap gap-2">
            <dt className="font-semibold text-text">{t('rppTitleLabel')} :</dt>
            <dd className="text-text-muted">{info.rppTitle}</dd>
          </div>
          <div className="flex flex-wrap gap-2">
            <dt className="font-semibold text-text">{t('rppEmailLabel')} :</dt>
            <dd>
              <a
                href={`mailto:${info.rppEmail}`}
                className="text-primary hover:underline"
              >
                {info.rppEmail}
              </a>
            </dd>
          </div>
        </dl>
        <Link
          href="/politique-confidentialite"
          className="mt-4 inline-block text-sm font-semibold text-primary underline hover:text-primary-hover"
        >
          {t('privacyLinkLabel')}
        </Link>
      </Container>
    </Section>
  );
}
