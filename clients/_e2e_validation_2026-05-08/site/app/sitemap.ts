import type { MetadataRoute } from 'next';
import { SITE_URL } from '@/lib/site-info';

const ROUTES: { fr: string; en: string; priority: number; changefreq: 'daily' | 'weekly' | 'monthly' }[] = [
  { fr: '/', en: '/en', priority: 1.0, changefreq: 'weekly' },
  { fr: '/promotions', en: '/en/promotions', priority: 0.9, changefreq: 'weekly' },
  { fr: '/produits', en: '/en/products', priority: 0.8, changefreq: 'monthly' },
  { fr: '/contact', en: '/en/contact', priority: 0.7, changefreq: 'monthly' },
  { fr: '/politique-confidentialite', en: '/en/privacy-policy', priority: 0.3, changefreq: 'monthly' },
  { fr: '/mentions-legales', en: '/en/legal-notice', priority: 0.3, changefreq: 'monthly' },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const items: MetadataRoute.Sitemap = [];
  for (const route of ROUTES) {
    items.push({
      url: `${SITE_URL}${route.fr}`,
      lastModified: now,
      changeFrequency: route.changefreq,
      priority: route.priority,
      alternates: {
        languages: {
          fr: `${SITE_URL}${route.fr}`,
          en: `${SITE_URL}${route.en}`,
        },
      },
    });
    items.push({
      url: `${SITE_URL}${route.en}`,
      lastModified: now,
      changeFrequency: route.changefreq,
      priority: route.priority,
      alternates: {
        languages: {
          fr: `${SITE_URL}${route.fr}`,
          en: `${SITE_URL}${route.en}`,
        },
      },
    });
  }
  return items;
}
