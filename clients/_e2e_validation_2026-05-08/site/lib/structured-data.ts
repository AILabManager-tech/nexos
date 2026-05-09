import { getHours, getSiteInfo, SITE_URL } from './site-info';

export function buildOrganizationLd() {
  const info = getSiteInfo();
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: info.legalName,
    url: SITE_URL,
    email: info.email,
    telephone: info.phone,
    address: {
      '@type': 'PostalAddress',
      streetAddress: info.streetAddress,
      addressLocality: info.city,
      postalCode: info.postalCode,
      addressRegion: info.region,
      addressCountry: info.country,
    },
  };
}

export function buildWebSiteLd(locale: 'fr' | 'en') {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Dépanneur Nobert',
    url: SITE_URL,
    inLanguage: locale === 'fr' ? 'fr-CA' : 'en-CA',
  };
}

export function buildLocalBusinessLd() {
  const info = getSiteInfo();
  const hours = getHours();
  const dayMap: Record<string, string> = {
    monday: 'Monday',
    tuesday: 'Tuesday',
    wednesday: 'Wednesday',
    thursday: 'Thursday',
    friday: 'Friday',
    saturday: 'Saturday',
    sunday: 'Sunday',
  };
  return {
    '@context': 'https://schema.org',
    '@type': ['LocalBusiness', 'ConvenienceStore'],
    name: info.legalName,
    url: SITE_URL,
    telephone: info.phone,
    email: info.email,
    address: {
      '@type': 'PostalAddress',
      streetAddress: info.streetAddress,
      addressLocality: info.city,
      postalCode: info.postalCode,
      addressRegion: info.region,
      addressCountry: info.country,
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: info.geo.latitude,
      longitude: info.geo.longitude,
    },
    openingHoursSpecification: hours.weekly
      .filter((d) => !d.closed)
      .map((d) => ({
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: dayMap[d.day],
        opens: d.open,
        closes: d.close,
      })),
  };
}

export function buildBreadcrumbLd(
  items: { name: string; url: string }[],
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      name: item.name,
      item: item.url,
    })),
  };
}
