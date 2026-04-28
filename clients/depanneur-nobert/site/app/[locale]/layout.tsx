import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale, getTranslations } from 'next-intl/server';
import { Fraunces, Inter } from 'next/font/google';
import { routing, type Locale } from '@/i18n/routing';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { StickyCTA } from '@/components/layout/StickyCTA';
import { CookieConsentBanner } from '@/components/layout/CookieConsentBanner';
import {
  buildLocalBusinessSchema,
  buildWebSiteSchema,
  jsonLdScriptProps,
} from '@/lib/jsonld';
import { getClientConfig } from '@/lib/clientConfig';
import '@/styles/globals.css';

const fraunces = Fraunces({
  subsets: ['latin', 'latin-ext'],
  weight: ['600', '700'],
  variable: '--font-heading',
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin', 'latin-ext'],
  weight: ['400', '600'],
  variable: '--font-body',
  display: 'swap',
});

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

interface LayoutProps {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'home.meta' });
  const config = getClientConfig();

  const ville = config.ville;
  const anneeFondation = config.anneeFondation;

  return {
    metadataBase: new URL(config.baseUrl),
    title: {
      default: t('title', { ville, city: ville }),
      template: `%s · Dépanneur Nobert`,
    },
    description: t('description', { ville, city: ville }),
    openGraph: {
      title: t('ogTitle', { ville, city: ville }),
      description: t('ogDescription', { ville, city: ville, anneeFondation }),
      type: 'website',
      locale: locale === 'fr' ? 'fr_CA' : 'en_CA',
      url: `${config.baseUrl}/${locale}`,
      siteName: 'Dépanneur Nobert',
      images: [
        {
          url: '/og-image.png',
          width: 1200,
          height: 630,
          alt: 'Dépanneur Nobert',
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: t('ogTitle', { ville, city: ville }),
      description: t('ogDescription', { ville, city: ville, anneeFondation }),
    },
    alternates: {
      canonical: `${config.baseUrl}/${locale}`,
      languages: {
        'fr-CA': `${config.baseUrl}/fr`,
        'en-CA': `${config.baseUrl}/en`,
        'x-default': `${config.baseUrl}/fr`,
      },
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}

export default async function LocaleLayout({ children, params }: LayoutProps) {
  const { locale } = await params;
  if (!(routing.locales as readonly string[]).includes(locale)) {
    notFound();
  }
  setRequestLocale(locale);
  const messages = await getMessages();
  const tNav = await getTranslations({ locale, namespace: 'common.nav' });

  const localBusiness = buildLocalBusinessSchema(locale as Locale);
  const website = buildWebSiteSchema(locale as Locale);

  return (
    <html lang={locale === 'fr' ? 'fr-CA' : 'en-CA'} className={`${fraunces.variable} ${inter.variable}`}>
      <body className="bg-background text-text antialiased flex min-h-screen flex-col">
        <a href="#main" className="skip-link">
          {tNav('skipToContent')}
        </a>
        <NextIntlClientProvider messages={messages}>
          <Header />
          <main id="main" className="flex-1">
            {children}
          </main>
          <Footer />
          <StickyCTA />
          <CookieConsentBanner />
        </NextIntlClientProvider>
        <script {...jsonLdScriptProps(localBusiness)} />
        <script {...jsonLdScriptProps(website)} />
      </body>
    </html>
  );
}
