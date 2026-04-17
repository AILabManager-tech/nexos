import { setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { ProblemSolution } from '@/components/sections/ProblemSolution';
import { HowItWorks } from '@/components/sections/HowItWorks';
import { CTA } from '@/components/sections/CTA';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function HomePage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  // Structure StoryBrand P19 (ref S19 Bop Design, case study Productive.io S18) :
  //   Hero (accroche client-héros + CTA + démo P10 in-hero) →
  //   ProblemSolution (problème client reconnu, stat 33%) →
  //   HowItWorks (plan 3 étapes Connecter/Visualiser/Agir, pas 10) →
  //   CTA (résultat attendu + dernier appel).
  // Démo interactive P10 est LIVRÉE DANS le Hero (ref S17 Monday.com — pas un screenshot).
  return (
    <>
      <Hero />
      <ProblemSolution />
      <HowItWorks />
      <CTA />
    </>
  );
}
