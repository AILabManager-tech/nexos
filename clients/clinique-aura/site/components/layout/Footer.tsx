import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';

export function Footer() {
  const t = useTranslations('layout.footer');
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-primary-100 bg-surface-alt">
      <div className="mx-auto max-w-7xl px-6 py-16 grid gap-10 md:grid-cols-3">
        <div>
          <p className="font-heading text-2xl text-ink">Clinique Aura</p>
          <address className="mt-4 not-italic text-sm text-ink-soft">
            {t('address')}
            <br />
            <a className="underline" href={`tel:${t('phone').replace(/\s/g, '')}`}>
              {t('phone')}
            </a>
            <br />
            <a className="underline" href={`mailto:${t('email')}`}>
              {t('email')}
            </a>
          </address>
        </div>

        <nav aria-label="Liens légaux" className="md:col-start-3">
          <ul className="space-y-3 text-sm">
            <li>
              <Link href="/politique-confidentialite" className="hover:text-primary transition-colors">
                {t('privacy')}
              </Link>
            </li>
            <li>
              <Link href="/mentions-legales" className="hover:text-primary transition-colors">
                {t('legal')}
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="border-t border-primary-100 py-6 text-center text-xs text-ink-muted">
        © {year} Clinique Aura inc. — {t('rights')}
      </div>
    </footer>
  );
}
