import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';

export function Footer() {
  const t = useTranslations('layout.footer');
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-surface-raised bg-surface-alt">
      <div className="mx-auto max-w-7xl px-6 py-16 grid gap-10 md:grid-cols-3">
        <div>
          <p className="font-display text-2xl font-bold text-ink">
            Vertex<span className="text-accent">.</span>PMO
          </p>
          <p className="mt-3 text-sm text-ink-soft max-w-xs">{t('tagline')}</p>
          <address className="mt-6 not-italic text-sm text-ink-soft">
            {t('address')}
            <br />
            <a className="underline hover:text-accent-soft transition-colors" href={`tel:${t('phone').replace(/\s/g, '')}`}>
              {t('phone')}
            </a>
            <br />
            <a className="underline hover:text-accent-soft transition-colors" href={`mailto:${t('email')}`}>
              {t('email')}
            </a>
          </address>
          <p className="mt-6 text-xs text-ink-muted">{t('hours')}</p>
        </div>

        <nav aria-label="Liens légaux" className="md:col-start-3">
          <ul className="space-y-3 text-sm">
            <li>
              <Link href="/politique-confidentialite" className="text-ink-soft hover:text-accent-soft transition-colors">
                {t('privacy')}
              </Link>
            </li>
            <li>
              <Link href="/mentions-legales" className="text-ink-soft hover:text-accent-soft transition-colors">
                {t('legal')}
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="border-t border-surface-raised py-6 text-center text-xs text-ink-muted">
        © {year} Vertex PMO inc. — {t('rights')}
      </div>
    </footer>
  );
}
