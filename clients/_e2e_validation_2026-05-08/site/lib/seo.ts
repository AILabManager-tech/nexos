import type { Metadata } from 'next';
import { SITE_URL } from './site-info';

type SeoPage =
  | 'home'
  | 'promotions'
  | 'produits'
  | 'contact'
  | 'privacy'
  | 'legal';

interface BuildMetadataArgs {
  page: SeoPage;
  locale: 'fr' | 'en';
  title: string;
  description: string;
  pathname: string;
}

const PATHS_FR: Record<SeoPage, string> = {
  home: '/',
  promotions: '/promotions',
  produits: '/produits',
  contact: '/contact',
  privacy: '/politique-confidentialite',
  legal: '/mentions-legales',
};

const PATHS_EN: Record<SeoPage, string> = {
  home: '/en',
  promotions: '/en/promotions',
  produits: '/en/products',
  contact: '/en/contact',
  privacy: '/en/privacy-policy',
  legal: '/en/legal-notice',
};

export function buildMetadata({
  page,
  locale,
  title,
  description,
  pathname,
}: BuildMetadataArgs): Metadata {
  const canonical = `${SITE_URL}${pathname}`;
  return {
    title,
    description,
    alternates: {
      canonical,
      languages: {
        fr: `${SITE_URL}${PATHS_FR[page]}`,
        en: `${SITE_URL}${PATHS_EN[page]}`,
        'x-default': `${SITE_URL}${PATHS_FR[page]}`,
      },
    },
    openGraph: {
      title,
      description,
      url: canonical,
      siteName: 'Dépanneur Nobert',
      locale: locale === 'fr' ? 'fr_CA' : 'en_CA',
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}
