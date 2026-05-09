import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { PromoWeekTeaser } from '@/components/sections/PromoWeekTeaser';
import { CategoriesOverview } from '@/components/sections/CategoriesOverview';
import { InfosPratiques } from '@/components/sections/InfosPratiques';
import { LeMotDuProprio } from '@/components/sections/LeMotDuProprio';
import { NewsletterCta } from '@/components/sections/NewsletterCta';
import { JsonLd } from '@/components/seo/JsonLd';
import { buildLocalBusinessLd } from '@/lib/structured-data';
import { buildMetadata } from '@/lib/seo';
import type { Locale } from '@/i18n/routing';

interface PageProps {
  params: Promise<{ locale: Locale }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'home.meta' });
  return buildMetadata({
    page: 'home',
    locale,
    title: t('title'),
    description: t('description'),
    pathname: locale === 'fr' ? '/' : '/en',
  });
}

export default async function HomePage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return (
    <>
      <Hero />
      <PromoWeekTeaser />
      <CategoriesOverview />
      <InfosPratiques />
      <LeMotDuProprio />
      <NewsletterCta />
      <JsonLd data={buildLocalBusinessLd()} />
    </>
  );
}
