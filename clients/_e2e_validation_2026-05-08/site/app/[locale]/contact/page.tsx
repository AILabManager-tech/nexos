import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { HeroContact } from '@/components/sections/HeroContact';
import { Coordonnees } from '@/components/sections/Coordonnees';
import { Horaires } from '@/components/sections/Horaires';
import { ContactForm } from '@/components/sections/ContactForm';
import { RppMention } from '@/components/sections/RppMention';
import { JsonLd } from '@/components/seo/JsonLd';
import { buildLocalBusinessLd } from '@/lib/structured-data';
import { buildMetadata } from '@/lib/seo';
import type { Locale } from '@/i18n/routing';

interface PageProps {
  params: Promise<{ locale: Locale }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'contact.meta' });
  return buildMetadata({
    page: 'contact',
    locale,
    title: t('title'),
    description: t('description'),
    pathname: locale === 'fr' ? '/contact' : '/en/contact',
  });
}

export default async function ContactPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return (
    <>
      <HeroContact />
      <Coordonnees />
      <Horaires />
      <ContactForm />
      <RppMention />
      <JsonLd data={buildLocalBusinessLd()} />
    </>
  );
}
