import type { Metadata } from 'next';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Inter, Fraunces } from 'next/font/google';
import { routing } from '@/i18n/routing';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { CookieConsent } from '@/components/layout/CookieConsent';
import '../globals.css';

// 2 familles Google Fonts (Inter + Fraunces) — LCP-friendly.
// Fraunces display : variable font moderne, rupture vs Garamond classique (P14 rupture 1).
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  weight: ['400', '500', '600', '700']
});

const fraunces = Fraunces({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
  weight: ['700']
});

export const metadata: Metadata = {
  metadataBase: new URL('https://beaumont-avocats.ca'),
  title: {
    default: 'Beaumont Avocats — Droit des affaires · Québec',
    template: '%s · Beaumont Avocats'
  },
  description: 'Cabinet d\'avocats à Montréal. Droit des affaires, transactions commerciales, litige civil et résolution de différends. Conseil stratégique pour les entreprises et leurs dirigeants.',
  alternates: {
    languages: {
      fr: '/fr',
      en: '/en'
    }
  },
  openGraph: {
    type: 'website',
    locale: 'fr_CA',
    siteName: 'Beaumont Avocats'
  }
};

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

type Props = {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
};

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;

  if (!routing.locales.includes(locale as typeof routing.locales[number])) {
    notFound();
  }

  setRequestLocale(locale);
  const messages = await getMessages();

  return (
    <html lang={locale} className={`${inter.variable} ${fraunces.variable}`}>
      <body>
        <NextIntlClientProvider messages={messages}>
          <a
            href="#main"
            className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:rounded-sm focus:bg-primary focus:px-4 focus:py-2 focus:text-surface"
          >
            {locale === 'fr' ? 'Aller au contenu principal' : 'Skip to main content'}
          </a>
          <Header />
          <main id="main">{children}</main>
          <Footer />
          <CookieConsent />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
