// Sections: S-013 ProduitsHero, S-014 ProduitsCategoriesNav, S-015 ProduitsGalerie,
// S-016 ProduitsFAQ, S-017 CrossSellPromotions
import type { Metadata } from 'next';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { ProduitsHero } from '@/components/sections/ProduitsHero';
import { ProduitsCategoriesNav } from '@/components/sections/ProduitsCategoriesNav';
import { ProduitsGalerie } from '@/components/sections/ProduitsGalerie';
import { ProduitsFAQ } from '@/components/sections/ProduitsFAQ';
import { CrossSellPromotions } from '@/components/sections/CrossSellPromotions';
import { getClientConfig } from '@/lib/clientConfig';

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'produits.meta' });
  const config = getClientConfig();
  const routeFr = 'produits';
  const routeEn = 'products';
  const route = locale === 'fr' ? routeFr : routeEn;
  return {
    title: t('title', { ville: config.ville, city: config.ville, anneeFondation: config.anneeFondation }),
    description: t('description', { ville: config.ville, city: config.ville, anneeFondation: config.anneeFondation }),
    alternates: {
      canonical: `${config.baseUrl}/${locale}/${route}`,
      languages: {
        'fr-CA': `${config.baseUrl}/fr/${routeFr}`,
        'en-CA': `${config.baseUrl}/en/${routeEn}`,
        'x-default': `${config.baseUrl}/fr/${routeFr}`,
      },
    },
    openGraph: {
      title: t('ogTitle', { ville: config.ville, city: config.ville }),
      description: t('ogDescription'),
    },
  };
}

export default async function ProduitsPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return (
    <>
      <ProduitsHero />
      <ProduitsCategoriesNav />
      <ProduitsGalerie />
      <ProduitsFAQ />
      <CrossSellPromotions />
    </>
  );
}
