import { setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { ServicesOverview } from '@/components/sections/ServicesOverview';
import { ProjectsGallery } from '@/components/sections/ProjectsGallery';
import { ContactCta } from '@/components/sections/ContactCta';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function HomePage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <>
      <Hero />
      <ServicesOverview />
      {/* Pattern P06 — Galerie de projets grayscale→color au hover (ref S27 Puckett Electric) */}
      <ProjectsGallery />
      <ContactCta />
    </>
  );
}
