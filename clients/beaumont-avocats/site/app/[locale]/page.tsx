import { setRequestLocale } from 'next-intl/server';
import { Hero } from '@/components/sections/Hero';
import { Expertises } from '@/components/sections/Expertises';
import { Approche } from '@/components/sections/Approche';
import { Equipe } from '@/components/sections/Equipe';
import { ContactCTA } from '@/components/sections/ContactCTA';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function HomePage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  // Structure P14 rupture 3 (ref S23 BD&P) : rompt le modèle "hero centré + 4 cards
  // services + bios stock". Remplace par :
  //   Hero asymétrique (typo gauche / figure verticale droite) →
  //   Expertises (liste éditoriale numérotée, pas cards) →
  //   Approche (narrative rédigée plutôt que bullets) →
  //   Équipe (biographies photo N&B P17 mono→couleur au scroll) →
  //   ContactCTA
  return (
    <>
      <Hero />
      <Expertises />
      <Approche />
      <Equipe />
      <ContactCTA />
    </>
  );
}
