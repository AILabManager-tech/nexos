import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { CookieSettingsButton } from './CookieConsent';
import { getSiteInfo } from '@/lib/site-info';
import { phoneTel } from '@/lib/format';

export function Footer() {
  const t = useTranslations('common.footer');
  const tNav = useTranslations('common.nav');
  const tBrand = useTranslations('common.brand');
  const info = getSiteInfo();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-surface-alt">
      <Container className="grid gap-8 py-12 sm:grid-cols-2 lg:grid-cols-3">
        <div>
          <h2 className="font-heading text-xl font-extrabold text-primary">
            {tBrand('name')}
          </h2>
          <p className="mt-3 max-w-prose text-sm text-text-muted">
            {t('tagline')}
          </p>
        </div>

        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-text">
            {t('columnContactTitle')}
          </h3>
          <ul className="mt-3 space-y-2 text-sm text-text-muted">
            <li>
              <span className="block text-xs uppercase tracking-wide">
                {t('addressLabel')}
              </span>
              <span>{info.streetAddress}, {info.city}, {info.region} {info.postalCode}</span>
            </li>
            <li>
              <span className="block text-xs uppercase tracking-wide">
                {t('phoneLabel')}
              </span>
              <a href={phoneTel(info.phone)} className="font-semibold text-primary hover:underline">
                {info.phone}
              </a>
            </li>
            <li>
              <span className="block text-xs uppercase tracking-wide">
                {t('emailLabel')}
              </span>
              <a href={`mailto:${info.email}`} className="font-semibold text-primary hover:underline">
                {info.email}
              </a>
            </li>
            <li className="text-xs">{t('hoursShortLabel')}</li>
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-text">
            {t('columnLegalTitle')}
          </h3>
          <ul className="mt-3 space-y-2 text-sm">
            <li>
              <Link
                href="/politique-confidentialite"
                className="text-primary hover:underline"
              >
                {t('privacyPolicy')}
              </Link>
            </li>
            <li>
              <Link
                href="/mentions-legales"
                className="text-primary hover:underline"
              >
                {t('legalMentions')}
              </Link>
            </li>
            <li>
              <CookieSettingsButton />
            </li>
            <li className="pt-2 text-xs text-text-muted">
              {t('rppLine', { rppName: info.rppName, rppEmail: info.rppEmail })}
            </li>
          </ul>
          <nav aria-label={tNav('home')} className="mt-4 flex flex-wrap gap-3 text-sm">
            <Link href="/" className="text-primary hover:underline">
              {tNav('home')}
            </Link>
            <Link href="/promotions" className="text-primary hover:underline">
              {tNav('promotions')}
            </Link>
            <Link href="/produits" className="text-primary hover:underline">
              {tNav('products')}
            </Link>
            <Link href="/contact" className="text-primary hover:underline">
              {tNav('contact')}
            </Link>
          </nav>
        </div>
      </Container>

      <div className="border-t border-border bg-background">
        <Container className="flex flex-col items-center justify-between gap-2 py-4 text-xs text-text-muted sm:flex-row">
          <p>{t('copyright', { currentYear, legalName: tBrand('legalName') })}</p>
        </Container>
      </div>
    </footer>
  );
}
