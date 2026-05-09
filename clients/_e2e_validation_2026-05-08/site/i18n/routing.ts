import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';

export const routing = defineRouting({
  locales: ['fr', 'en'],
  defaultLocale: 'fr',
  localePrefix: 'as-needed',
  pathnames: {
    '/': '/',
    '/promotions': {
      fr: '/promotions',
      en: '/promotions',
    },
    '/produits': {
      fr: '/produits',
      en: '/products',
    },
    '/contact': '/contact',
    '/politique-confidentialite': {
      fr: '/politique-confidentialite',
      en: '/privacy-policy',
    },
    '/mentions-legales': {
      fr: '/mentions-legales',
      en: '/legal-notice',
    },
  },
});

export type Pathnames = keyof typeof routing.pathnames;
export type Locale = (typeof routing.locales)[number];

export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
