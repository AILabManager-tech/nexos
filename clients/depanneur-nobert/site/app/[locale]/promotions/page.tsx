// Sections: S-009 PromotionsHero, S-010 PromotionsList, S-011 PromotionsFAQ, S-012 CrossSellProduits
import type { Metadata } from 'next';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { PromotionsHero } from '@/components/sections/PromotionsHero';
import { PromotionsList } from '@/components/sections/PromotionsList';
import { PromotionsFAQ } from '@/components/sections/PromotionsFAQ';
import { CrossSellProduits } from '@/components/sections/CrossSellProduits';
import { getActivePromotions } from '@/lib/promotions';
import { getClientConfig } from '@/lib/clientConfig';

interface PageProps {
  params: Promise<{ locale: string }>;
}

export const revalidate = 604800; // 1 week ISR

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'promotions.meta' });
  const config = getClientConfig();
  const route = locale === 'fr' ? 'promotions' : 'deals';
  return {
    title: t('title', { ville: config.ville, city: config.ville }),
    description: t('description', { ville: config.ville, city: config.ville }),
    alternates: {
      canonical: `${config.baseUrl}/${locale}/${route}`,
      languages: {
        'fr-CA': `${config.baseUrl}/fr/promotions`,
        'en-CA': `${config.baseUrl}/en/deals`,
        'x-default': `${config.baseUrl}/fr/promotions`,
      },
    },
    openGraph: {
      title: t('ogTitle'),
      description: t('ogDescription', { ville: config.ville, city: config.ville }),
    },
  };
}

export default async function PromotionsPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  const promotions = getActivePromotions();
  return (
    <>
      <PromotionsHero />
      <PromotionsList promotions={promotions} />
      <PromotionsFAQ />
      <CrossSellProduits />
    </>
  );
}
