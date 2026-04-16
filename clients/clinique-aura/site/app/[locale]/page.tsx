import { setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { ServicesOverview } from '@/components/sections/ServicesOverview';
import { TestimonialsAdjacentCta } from '@/components/sections/TestimonialsAdjacentCta';

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
      {/* Pattern P02 — Social proof adjacente au CTA : remplace la section ContactCta "simple" */}
      <TestimonialsAdjacentCta />
    </>
  );
}
