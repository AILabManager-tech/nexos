// Section: S-023 politique-confidentialite.PolitiqueContent
//
// Loi 25 (Québec) — couverture éditoriale obligatoire de la politique :
//   1. Responsable de la protection des renseignements personnels (RPP)
//   2. Renseignements personnels collectés (données personnelles)
//   3. Finalité de la collecte (fins de chaque traitement)
//   4. Durée de conservation (rétention par catégorie de données)
//   5. Droits d'accès, de rectification et de suppression
//   6. Mécanisme de plainte / recours auprès de la Commission d'accès à
//      l'information (complaint workflow)
// Le rendu détaillé vit dans `components/sections/PrivacyPolicyBody.tsx`
// et puise dans `messages/{fr,en}.json` -> `legal.privacy.*`.
import type { Metadata } from 'next';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { PrivacyPolicyBody } from '@/components/sections/PrivacyPolicyBody';
import { getClientConfig } from '@/lib/clientConfig';

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'legal.privacy.meta' });
  const config = getClientConfig();
  const route = locale === 'fr' ? 'politique-confidentialite' : 'privacy-policy';
  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `${config.baseUrl}/${locale}/${route}`,
      languages: {
        'fr-CA': `${config.baseUrl}/fr/politique-confidentialite`,
        'en-CA': `${config.baseUrl}/en/privacy-policy`,
        'x-default': `${config.baseUrl}/fr/politique-confidentialite`,
      },
    },
  };
}

export default async function PrivacyPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  return <PrivacyPolicyBody />;
}
