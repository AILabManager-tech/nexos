import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';

/**
 * Footer — NAP (nom, adresse, téléphone), liens légaux Loi 25 (politique-confidentialite,
 * mentions-legales) et copyright dynamique. I18n : `layout.footer.*`. Liens légaux en
 * accent or (signal premium P12).
 */
export function Footer() {
  const t = useTranslations('layout.footer');
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-primary-800 bg-surface-alt">
      <div className="mx-auto max-w-7xl px-6 py-16 grid gap-10 md:grid-cols-3">
        <div>
          <p className="font-heading text-2xl text-ink">Électro-Maître Industriel</p>
          <address className="mt-4 not-italic text-sm text-ink-soft">
            {t('address')}
            <br />
            <a className="underline text-accent" href={`tel:${t('phone').replace(/\s/g, '')}`}>
              {t('phone')}
            </a>
            <br />
            <a className="underline text-accent" href={`mailto:${t('email')}`}>
              {t('email')}
            </a>
          </address>
        </div>

        <nav aria-label="Liens légaux" className="md:col-start-3">
          <ul className="space-y-3 text-sm">
            <li>
              <Link href="/politique-confidentialite" className="hover:text-accent transition-colors">
                {t('privacy')}
              </Link>
            </li>
            <li>
              <Link href="/mentions-legales" className="hover:text-accent transition-colors">
                {t('legal')}
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="border-t border-primary-800 py-6 text-center text-xs text-ink-muted">
        © {year} Électro-Maître Industriel inc. — {t('rights')}
      </div>
    </footer>
  );
}
