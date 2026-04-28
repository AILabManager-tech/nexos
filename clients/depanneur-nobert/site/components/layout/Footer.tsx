import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Logo } from '@/components/layout/Logo';
import { CookieSettingsButton } from '@/components/layout/CookieSettingsButton';
import { getClientConfig, getTelHref } from '@/lib/clientConfig';

export function Footer() {
  const tFooter = useTranslations('common.footer');
  const tNav = useTranslations('common.nav');
  const config = getClientConfig();

  return (
    <footer className="bg-text text-text-inverse" role="contentinfo">
      <Container className="py-12 lg:py-16 grid gap-10 md:grid-cols-3">
        <div className="space-y-4">
          <Logo color="inverse" />
          <p className="text-small text-text-inverse/80">
            {tFooter('madeWithCare', { ville: config.ville })}
          </p>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-heading font-bold">
            {tFooter('columnNavigate')}
          </h2>
          <ul className="space-y-2 text-base">
            <li>
              <Link
                href="/"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tNav('home')}
              </Link>
            </li>
            <li>
              <Link
                href="/promotions"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tNav('promotions')}
              </Link>
            </li>
            <li>
              <Link
                href="/produits"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tNav('produits')}
              </Link>
            </li>
            <li>
              <Link
                href="/contact"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tNav('contact')}
              </Link>
            </li>
          </ul>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-heading font-bold">
            {tFooter('columnInfos')}
          </h2>
          <ul className="space-y-2 text-base">
            <li>
              {tFooter('address', {
                adresseLigne: config.adresseLigne,
                ville: config.ville,
                codePostal: config.codePostal,
              })}
            </li>
            <li>
              <a
                href={getTelHref()}
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tFooter('phone', { telephone: config.telephone })}
              </a>
            </li>
            <li>
              <a
                href={`mailto:${config.email}`}
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tFooter('email', { email: config.email })}
              </a>
            </li>
          </ul>
        </div>
      </Container>

      <div className="border-t border-text-inverse/20">
        <Container className="py-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-small">
          <p className="text-text-inverse/80">
            {tFooter('copyright', { currentYear: config.currentYear })}
          </p>
          <ul className="flex flex-wrap items-center gap-x-5 gap-y-2">
            <li>
              <Link
                href="/politique-confidentialite"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tFooter('linkPrivacy')}
              </Link>
            </li>
            <li>
              <Link
                href="/mentions-legales"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tFooter('linkLegal')}
              </Link>
            </li>
            <li>
              <Link
                href="/contact"
                className="hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
              >
                {tFooter('linkRpp')}
              </Link>
            </li>
            <li>
              <CookieSettingsButton />
            </li>
          </ul>
        </Container>
      </div>
    </footer>
  );
}
