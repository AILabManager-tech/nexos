import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { HeroPromoWeek } from '@/components/sections/HeroPromoWeek';
import { PromosGrid } from '@/components/sections/PromosGrid';
import { NewsletterCta } from '@/components/sections/NewsletterCta';
import { buildMetadata } from '@/lib/seo';
import type { Locale } from '@/i18n/routing';

interface PageProps {
  params: Promise<{ locale: Locale }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'promotions.meta' });
  return buildMetadata({
    page: 'promotions',
    locale,
    title: t('title'),
    description: t('description'),
    pathname: locale === 'fr' ? '/promotions' : '/en/promotions',
  });
}

export default async function PromotionsPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return (
    <>
      <HeroPromoWeek />
      <PromosGrid />
      <NewsletterCta />
    </>
  );
}
