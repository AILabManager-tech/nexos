// Sections: S-018 ContactHero, S-019 CoordonneesHoraires, S-020 MapsEmbed,
// S-021 ContactForm, S-022 ContactNoteRPP
import type { Metadata } from 'next';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { ContactHero } from '@/components/sections/ContactHero';
import { CoordonneesHoraires } from '@/components/sections/CoordonneesHoraires';
import { MapsEmbed } from '@/components/sections/MapsEmbed';
import { ContactForm } from '@/components/sections/ContactForm';
import { ContactNoteRPP } from '@/components/sections/ContactNoteRPP';
import { getClientConfig } from '@/lib/clientConfig';

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'contact.meta' });
  const config = getClientConfig();
  return {
    title: t('title', { ville: config.ville, city: config.ville }),
    description: t('description', { ville: config.ville, city: config.ville }),
    alternates: {
      canonical: `${config.baseUrl}/${locale}/contact`,
      languages: {
        'fr-CA': `${config.baseUrl}/fr/contact`,
        'en-CA': `${config.baseUrl}/en/contact`,
        'x-default': `${config.baseUrl}/fr/contact`,
      },
    },
    openGraph: {
      title: t('ogTitle'),
      description: t('ogDescription', { ville: config.ville, city: config.ville }),
    },
  };
}

export default async function ContactPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return (
    <>
      <ContactHero />
      <CoordonneesHoraires />
      <MapsEmbed />
      <ContactForm />
      <ContactNoteRPP />
    </>
  );
}
