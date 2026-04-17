import type { Metadata } from 'next';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Inter, Bitter } from 'next/font/google';
import { routing } from '@/i18n/routing';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { CookieConsent } from '@/components/layout/CookieConsent';
import '../globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap'
});

const bitter = Bitter({
  subsets: ['latin'],
  variable: '--font-heading',
  display: 'swap',
  weight: ['700', '900']
});

export const metadata: Metadata = {
  metadataBase: new URL('https://electro-maitre-industriel.ca'),
  title: {
    default: 'Électro-Maître Industriel — Électricien industriel premium à Montréal',
    template: '%s · Électro-Maître Industriel'
  },
  description: 'Contractor électrique industriel premium à Montréal-Est. Automatisation, maintenance préventive et urgence 24/7 pour manufacturiers et agroalimentaires.',
  alternates: {
    languages: {
      fr: '/fr',
      en: '/en'
    }
  },
  openGraph: {
    type: 'website',
    locale: 'fr_CA',
    siteName: 'Électro-Maître Industriel'
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
    <html lang={locale} className={`${inter.variable} ${bitter.variable}`}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {/* Skip link — fond accent (or) + texte surface (sombre) = contraste AAA, visibilité maximale */}
          <a
            href="#main"
            className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:rounded-md focus:bg-accent focus:px-4 focus:py-2 focus:text-accent-ink"
          >
            Aller au contenu principal
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
