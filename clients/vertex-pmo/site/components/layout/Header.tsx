'use client';

import { useLocale, useTranslations } from 'next-intl';
import { Link, usePathname } from '@/i18n/routing';

export function Header() {
  const t = useTranslations('layout.header');
  const locale = useLocale();
  const pathname = usePathname();
  const otherLocale = locale === 'fr' ? 'en' : 'fr';

  return (
    <header className="sticky top-0 z-40 border-b border-surface-raised bg-surface/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2 font-display text-xl font-bold tracking-tight text-ink">
          <span aria-hidden="true" className="inline-block h-6 w-6 rounded-sm bg-gradient-to-br from-accent to-accent-hover" />
          Vertex<span className="text-accent">.</span>PMO
        </Link>
        <nav aria-label="Navigation principale" className="hidden md:block">
          <ul className="flex items-center gap-8 text-sm text-ink-soft">
            <li>
              <a href="#demo" className="hover:text-ink transition-colors">
                {t('nav.demo')}
              </a>
            </li>
            <li>
              <a href="#problem" className="hover:text-ink transition-colors">
                {t('nav.problem')}
              </a>
            </li>
            <li>
              <a href="#how" className="hover:text-ink transition-colors">
                {t('nav.how')}
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
            href="#cta"
            className="hidden md:inline-flex rounded-sm bg-accent px-5 py-2 text-sm font-medium text-surface-dark hover:bg-accent-hover transition-colors"
          >
            {t('cta_short')}
          </a>
        </div>
      </div>
    </header>
  );
}
