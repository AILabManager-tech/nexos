'use client';

import { useLocale, useTranslations } from 'next-intl';
import { Link, usePathname } from '@/i18n/routing';

export function Header() {
  const t = useTranslations('layout.header');
  const locale = useLocale();
  const pathname = usePathname();
  const otherLocale = locale === 'fr' ? 'en' : 'fr';

  return (
    <header className="sticky top-0 z-40 border-b border-primary-100 bg-surface/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="font-display text-2xl tracking-tight text-ink">
          La Table de Marguerite
        </Link>
        <nav aria-label="Navigation principale" className="hidden md:block">
          <ul className="flex items-center gap-8 text-sm">
            <li>
              <Link href="/" className="hover:text-primary transition-colors">
                {t('nav.home')}
              </Link>
            </li>
            <li>
              <a href="#histoire" className="hover:text-primary transition-colors">
                {t('nav.histoire')}
              </a>
            </li>
            <li>
              <a href="#menu" className="hover:text-primary transition-colors">
                {t('nav.menu')}
              </a>
            </li>
            <li>
              <a href="#reservation" className="hover:text-primary transition-colors">
                {t('nav.reservation')}
              </a>
            </li>
          </ul>
        </nav>
        <div className="flex items-center gap-4">
          <Link
            href={pathname}
            locale={otherLocale}
            className="text-sm text-ink-muted hover:text-ink transition-colors"
            aria-label={`Switch to ${otherLocale === 'fr' ? 'French' : 'English'}`}
          >
            {t('language_switch')}
          </Link>
          <a
            href="#reservation"
            className="hidden md:inline-flex rounded-sm bg-primary px-5 py-2 text-sm text-surface hover:bg-primary-600 transition-colors"
          >
            {t('cta_short')}
          </a>
        </div>
      </div>
    </header>
  );
}
