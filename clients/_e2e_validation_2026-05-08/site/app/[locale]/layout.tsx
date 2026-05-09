import type { Metadata } from 'next';
import { Fraunces, Inter } from 'next/font/google';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { StickyMobileCta } from '@/components/layout/StickyMobileCta';
import { CookieConsent } from '@/components/layout/CookieConsent';
import { SkipToContent } from '@/components/layout/SkipToContent';
import { JsonLd } from '@/components/seo/JsonLd';
import { buildOrganizationLd, buildWebSiteLd } from '@/lib/structured-data';
import { routing, type Locale } from '@/i18n/routing';
import { SITE_URL } from '@/lib/site-info';
import '../../styles/globals.css';

const fraunces = Fraunces({
  subsets: ['latin'],
  weight: ['700', '800'],
  variable: '--font-fraunces',
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '600'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Dépanneur Nobert',
    template: '%s | Dépanneur Nobert',
  },
  description:
    'Dépanneur de quartier à Québec. Bières, snacks, loto Québec, dépannage — ouvert 7/7.',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
};

interface LocaleLayoutProps {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function LocaleLayout({
  children,
  params,
}: LocaleLayoutProps) {
  const { locale } = await params;
  if (!(routing.locales as readonly string[]).includes(locale)) {
    notFound();
  }
  setRequestLocale(locale);

  const messages = await getMessages();

  return (
    <html lang={locale} className={`${fraunces.variable} ${inter.variable}`}>
      <body className="min-h-screen flex flex-col">
        <NextIntlClientProvider locale={locale} messages={messages}>
          <SkipToContent />
          <Header />
          <main id="main" className="flex-1">
            {children}
          </main>
          <Footer />
          <StickyMobileCta />
          <CookieConsent />
          <JsonLd data={[buildOrganizationLd(), buildWebSiteLd(locale as Locale)]} />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}
