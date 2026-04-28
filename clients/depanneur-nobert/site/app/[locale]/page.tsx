// Sections: S-001 Hero, S-002 PromotionsHighlight, S-003 CategoriesProduits,
// S-004 SocialProofVoisinage, S-005 InfosPratiques, S-006 StoryBrand, S-007 NewsletterCTA
import { setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { PromotionsHighlight } from '@/components/sections/PromotionsHighlight';
import { CategoriesProduits } from '@/components/sections/CategoriesProduits';
import { SocialProofVoisinage } from '@/components/sections/SocialProofVoisinage';
import { InfosPratiques } from '@/components/sections/InfosPratiques';
import { StoryBrand } from '@/components/sections/StoryBrand';
import { NewsletterCTA } from '@/components/sections/NewsletterCTA';

interface HomePageProps {
  params: Promise<{ locale: string }>;
}

export default async function HomePage({ params }: HomePageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return (
    <>
      <Hero />
      <PromotionsHighlight />
      <CategoriesProduits />
      <SocialProofVoisinage />
      <InfosPratiques />
      <StoryBrand />
      <NewsletterCTA />
    </>
  );
}
