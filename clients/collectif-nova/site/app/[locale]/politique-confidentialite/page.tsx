import { useTranslations } from 'next-intl';
import { setRequestLocale } from 'next-intl/server';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function PrivacyPolicyPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);
  return <PrivacyContent />;
}

function PrivacyContent() {
  const t = useTranslations('legal.privacy');
  return (
    <article className="mx-auto max-w-prose px-6 py-24">
      <h1 className="text-4xl md:text-5xl">{t('title')}</h1>
      <p className="mt-6 text-ink-soft">{t('intro')}</p>

      <h2 className="mt-12 text-2xl">{t('rpp_label')}</h2>
      <p className="mt-2">
        <strong>{t('rpp_name')}</strong> — {t('rpp_title')}
        <br />
        <a className="underline" href={`mailto:${t('rpp_email')}`}>
          {t('rpp_email')}
        </a>
      </p>

      <h2 className="mt-10 text-2xl">{t('data_title')}</h2>
      <p className="mt-2">{t('data_body')}</p>

      <h2 className="mt-10 text-2xl">{t('purposes_title')}</h2>
      <p className="mt-2">{t('purposes_body')}</p>

      <h2 className="mt-10 text-2xl">{t('retention_title')}</h2>
      <p className="mt-2">{t('retention_body')}</p>

      <h2 className="mt-10 text-2xl">{t('rights_title')}</h2>
      <p className="mt-2">{t('rights_body')}</p>
    </article>
  );
}
