import { getClientConfig } from '@/lib/clientConfig';
import { getRegularHoraires } from '@/lib/horaires';
import type { Locale } from '@/i18n/routing';

const DAY_TO_SCHEMA: Record<string, string> = {
  monday: 'Monday',
  tuesday: 'Tuesday',
  wednesday: 'Wednesday',
  thursday: 'Thursday',
  friday: 'Friday',
  saturday: 'Saturday',
  sunday: 'Sunday',
};

interface OrganizationSchema {
  '@context': 'https://schema.org';
  '@type': string;
  '@id': string;
  name: string;
  url: string;
  telephone?: string;
  email?: string;
  address?: object;
  openingHoursSpecification?: object[];
  geo?: object;
  areaServed?: string;
  sameAs?: string[];
  image?: string;
  logo?: string;
}

export function buildLocalBusinessSchema(locale: Locale): OrganizationSchema {
  const config = getClientConfig();
  const horaires = getRegularHoraires();

  const openingHours = horaires
    .filter((h) => !h.closed && h.open && h.close)
    .map((h) => ({
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: `https://schema.org/${DAY_TO_SCHEMA[h.day]}`,
      opens: h.open,
      closes: h.close,
    }));

  const schema: OrganizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'ConvenienceStore',
    '@id': `${config.baseUrl}/#localbusiness`,
    name: 'Dépanneur Nobert',
    url: `${config.baseUrl}/${locale}`,
    image: `${config.baseUrl}/og-image.png`,
    logo: `${config.baseUrl}/icon.svg`,
    telephone: config.telephone,
    email: config.email,
    areaServed: config.ville,
    address: {
      '@type': 'PostalAddress',
      streetAddress: config.adresseLigne,
      addressLocality: config.ville,
      addressRegion: 'QC',
      postalCode: config.codePostal,
      addressCountry: 'CA',
    },
  };

  if (openingHours.length > 0) {
    schema.openingHoursSpecification = openingHours;
  }

  return schema;
}

export function buildWebSiteSchema(locale: Locale) {
  const config = getClientConfig();
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${config.baseUrl}/#website`,
    url: `${config.baseUrl}/${locale}`,
    name: 'Dépanneur Nobert',
    inLanguage: locale === 'fr' ? 'fr-CA' : 'en-CA',
    publisher: {
      '@id': `${config.baseUrl}/#localbusiness`,
    },
  };
}

export function buildBreadcrumb(
  locale: Locale,
  trail: Array<{ name: string; url: string }>
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: trail.map((item, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export function buildFaqSchema(
  items: Array<{ question: string; answer: string }>
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  };
}

export function jsonLdScriptProps(data: object) {
  return {
    type: 'application/ld+json',
    dangerouslySetInnerHTML: { __html: JSON.stringify(data).replace(/</g, '\\u003c') },
  };
}
