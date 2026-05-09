import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { LegalContent } from '@/components/sections/LegalContent';
import { getSiteInfo } from '@/lib/site-info';
import { buildMetadata } from '@/lib/seo';
import type { Locale } from '@/i18n/routing';

interface PageProps {
  params: Promise<{ locale: Locale }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({
    locale,
    namespace: 'legal.legalMentions.meta',
  });
  return buildMetadata({
    page: 'legal',
    locale,
    title: t('title'),
    description: t('description'),
    pathname: locale === 'fr' ? '/mentions-legales' : '/en/legal-notice',
  });
}

export default async function LegalMentionsPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: 'legal.legalMentions' });
  const info = getSiteInfo();

  return (
    <LegalContent
      title={t('title')}
      intro={t('intro')}
      lastUpdated="2026-05-08"
    >
      <h2>Éditeur du site</h2>
      <p>
        <strong>{info.legalName}</strong>
        <br />
        Adresse : {info.streetAddress}, {info.city}, {info.region} {info.postalCode}, Canada
        <br />
        Téléphone : {info.phone}
        <br />
        Courriel : <a href={`mailto:${info.email}`}>{info.email}</a>
        <br />
        NEQ : {info.neq}
      </p>

      <h2>Hébergement</h2>
      <p>
        Vercel Inc.
        <br />
        340 S Lemon Ave #4133, Walnut, CA 91789, États-Unis
        <br />
        Site : <a href="https://vercel.com" rel="noopener noreferrer" target="_blank">vercel.com</a>
      </p>

      <h2>Propriété intellectuelle</h2>
      <p>
        Le contenu de ce site (textes, photos, mises en page) est la propriété
        de {info.legalName} ou de ses ayants droit. Toute reproduction, même
        partielle, est interdite sans autorisation écrite préalable.
      </p>

      <h2>Limitations de responsabilité</h2>
      <p>
        Les promotions affichées sont valides en magasin uniquement, dans la
        limite des stocks disponibles. {info.legalName} se réserve le droit de
        modifier ou de retirer une promotion sans préavis.
      </p>

      <h2>Loi applicable et juridiction</h2>
      <p>
        Ce site est régi par les lois de la province de Québec et les lois
        canadiennes applicables. Tout litige relève de la compétence exclusive
        des tribunaux du district judiciaire de Québec.
      </p>
    </LegalContent>
  );
}
