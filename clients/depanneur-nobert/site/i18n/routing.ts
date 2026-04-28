import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';

export const routing = defineRouting({
  locales: ['fr', 'en'],
  defaultLocale: 'fr',
  localePrefix: {
    mode: 'always',
  },
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
    '/contact': {
      fr: '/contact',
      en: '/contact',
    },
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

export type Locale = (typeof routing.locales)[number];

export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
