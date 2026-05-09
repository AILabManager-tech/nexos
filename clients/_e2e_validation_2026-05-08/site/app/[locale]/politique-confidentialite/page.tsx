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
    namespace: 'legal.privacyPolicy.meta',
  });
  return buildMetadata({
    page: 'privacy',
    locale,
    title: t('title'),
    description: t('description'),
    pathname: locale === 'fr' ? '/politique-confidentialite' : '/en/privacy-policy',
  });
}

export default async function PrivacyPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: 'legal.privacyPolicy' });
  const info = getSiteInfo();

  return (
    <LegalContent
      title={t('title')}
      intro={t('intro')}
      lastUpdated="2026-05-08"
    >
      <h2>1. Renseignements collectés</h2>
      <p>
        {info.legalName} recueille les renseignements suivants : courriel,
        téléphone, données de navigation (analytique anonyme uniquement avec
        consentement opt-in).
      </p>

      <h2>2. Finalités</h2>
      <ul>
        <li>Inscription et envoi de l&apos;infolettre hebdomadaire des promotions</li>
        <li>Réponse à vos demandes de contact ou de commande</li>
        <li>Statistiques de fréquentation anonymisées (avec consentement)</li>
      </ul>

      <h2>3. Durée de conservation</h2>
      <p>
        Inscription infolettre : 12 mois maximum après la dernière interaction.
        Demandes de contact : 6 mois après le dernier échange. Cookies
        analytiques : 30 jours maximum.
      </p>

      <h2>4. Vos droits : accès, rectification et suppression (Loi 25 du Québec)</h2>
      <p>
        Conformément à la Loi 25, vous disposez des droits d&apos;accès, de
        rectification et de suppression sur vos renseignements personnels, en
        plus du droit de retirer votre consentement et du droit de porter
        plainte auprès de la Commission d&apos;accès à l&apos;information du
        Québec.
      </p>
      <ul>
        <li>Droit d&apos;accès à vos renseignements personnels</li>
        <li>Droit de rectification et de suppression de vos renseignements</li>
        <li>Droit de retirer votre consentement à tout moment</li>
        <li>Droit de porter plainte auprès de la Commission d&apos;accès à l&apos;information du Québec</li>
      </ul>

      <h2>5. Responsable de la protection des renseignements personnels</h2>
      <p>
        <strong>{info.rppName}</strong> — {info.rppTitle}
        <br />
        Courriel : <a href={`mailto:${info.rppEmail}`}>{info.rppEmail}</a>
      </p>

      <h2>6. Services tiers et transferts hors Québec</h2>
      <ul>
        <li>Google Analytics — États-Unis (IP tronquée, pseudonymisée, opt-in uniquement)</li>
        <li>Google Maps — États-Unis (requête de carte uniquement)</li>
        <li>Vercel Inc. — États-Unis (hébergement)</li>
      </ul>

      <h2>7. Incident de confidentialité</h2>
      <p>
        En cas d&apos;incident de confidentialité, vous serez avisé conformément
        à l&apos;article 3.5 de la Loi 25. Pour signaler un incident :{' '}
        <a href={`mailto:${info.rppEmail}`}>{info.rppEmail}</a>.
      </p>
    </LegalContent>
  );
}
