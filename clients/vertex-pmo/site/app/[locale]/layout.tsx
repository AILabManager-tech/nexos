import type { Metadata } from 'next';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Inter, Space_Grotesk } from 'next/font/google';
import { routing } from '@/i18n/routing';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { CookieConsent } from '@/components/layout/CookieConsent';
import '../globals.css';

// 2 familles Google Fonts seulement (Inter + Space Grotesk) — LCP-friendly.
// Mono géré par fallback ui-monospace système (pas de 3e famille) → voir globals.css.
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  weight: ['400', '500', '600', '700']
});

// Une seule weight Space Grotesk pour minimiser la charge Google Fonts (LCP <= 2.5s).
// Les titres utilisent uniquement font-bold (700). Inter gère 400-700 pour le corps.
const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
  weight: ['700']
});

export const metadata: Metadata = {
  metadataBase: new URL('https://vertex-pmo.com'),
  title: {
    default: 'Vertex PMO — Pilotage projet unifié pour PME de services',
    template: '%s · Vertex PMO'
  },
  description: 'Le SaaS PMO qui révèle la profitabilité projet en temps réel — sans tableur, sans retro-saisie, sans surprise en fin de mois. Conçu pour les PME de services.',
  alternates: {
    languages: {
      fr: '/fr',
      en: '/en'
    }
  },
  openGraph: {
    type: 'website',
    locale: 'fr_CA',
    siteName: 'Vertex PMO'
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
    <html lang={locale} className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <body>
        <NextIntlClientProvider messages={messages}>
          <a
            href="#main"
            className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:rounded-sm focus:bg-accent focus:px-4 focus:py-2 focus:text-surface-dark"
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
