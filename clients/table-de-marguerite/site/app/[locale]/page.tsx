import { setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { ChefStory } from '@/components/sections/ChefStory';
import { MenuGallery } from '@/components/sections/MenuGallery';
import { Reservation } from '@/components/sections/Reservation';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function HomePage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  // Hiérarchie P08 : narrative chef AVANT le menu (story-first, ref S15 Fiola).
  // Pattern P20 remplace la section menu PDF/liste générique par une galerie d'images.
  return (
    <>
      <Hero />
      <ChefStory />
      <MenuGallery />
      <Reservation />
    </>
  );
}
