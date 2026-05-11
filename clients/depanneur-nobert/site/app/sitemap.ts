import type { MetadataRoute } from 'next';
import { getClientConfig } from '@/lib/clientConfig';

interface Route {
  fr: string;
  en: string;
  priority: number;
  changeFrequency: 'weekly' | 'monthly' | 'yearly';
}

const ROUTES: Route[] = [
  { fr: '', en: '', priority: 1.0, changeFrequency: 'weekly' },
  { fr: 'promotions', en: 'deals', priority: 0.9, changeFrequency: 'weekly' },
  { fr: 'produits', en: 'products', priority: 0.7, changeFrequency: 'monthly' },
  { fr: 'contact', en: 'contact', priority: 0.7, changeFrequency: 'yearly' },
  { fr: 'politique-confidentialite', en: 'privacy-policy', priority: 0.3, changeFrequency: 'yearly' },
  { fr: 'mentions-legales', en: 'legal-notice', priority: 0.3, changeFrequency: 'yearly' },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const { baseUrl } = getClientConfig();
  const now = new Date();
  return ROUTES.flatMap((route) => {
    const frUrl = `${baseUrl}/fr${route.fr ? `/${route.fr}` : ''}`;
    const enUrl = `${baseUrl}/en${route.en ? `/${route.en}` : ''}`;
    return [
      {
        url: frUrl,
        lastModified: now,
        changeFrequency: route.changeFrequency,
        priority: route.priority,
        alternates: {
          languages: {
            'fr-CA': frUrl,
            'en-CA': enUrl,
            'x-default': frUrl,
          },
        },
      },
      {
        url: enUrl,
        lastModified: now,
        changeFrequency: route.changeFrequency,
        priority: Math.max(0.3, route.priority - 0.1),
        alternates: {
          languages: {
            'fr-CA': frUrl,
            'en-CA': enUrl,
            'x-default': frUrl,
          },
        },
      },
    ];
  });
}
