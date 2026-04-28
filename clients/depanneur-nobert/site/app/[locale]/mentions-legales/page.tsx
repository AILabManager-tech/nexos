// Section: S-024 mentions-legales.MentionsContent
import type { Metadata } from 'next';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { LegalNoticeBody } from '@/components/sections/LegalNoticeBody';
import { getClientConfig } from '@/lib/clientConfig';

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'legal.notice.meta' });
  const config = getClientConfig();
  const route = locale === 'fr' ? 'mentions-legales' : 'legal-notice';
  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `${config.baseUrl}/${locale}/${route}`,
      languages: {
        'fr-CA': `${config.baseUrl}/fr/mentions-legales`,
        'en-CA': `${config.baseUrl}/en/legal-notice`,
        'x-default': `${config.baseUrl}/fr/mentions-legales`,
      },
    },
  };
}

export default async function LegalNoticePage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return <LegalNoticeBody />;
}
