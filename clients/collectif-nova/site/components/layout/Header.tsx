'use client';

import { useLocale, useTranslations } from 'next-intl';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Header() {
  const locale = useLocale();
  const pathname = usePathname();
  const t = useTranslations('header');

  const otherLocale = locale === 'fr' ? 'en' : 'fr';

  return (
    <header className="sticky top-0 z-40 bg-black/90 backdrop-blur border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link href="/" className="font-bold text-xl">
          Collectif Nova
        </Link>

        <nav className="hidden md:flex gap-8">
          <Link href="#services" className="hover:text-brand-primary transition">
            {t('services')}
          </Link>
          <Link href="#cases" className="hover:text-brand-primary transition">
            {t('projects')}
          </Link>
          <Link href="#contact" className="hover:text-brand-primary transition">
            {t('contact')}
          </Link>
        </nav>

        <div className="flex items-center gap-4">
          <Link
            href={pathname.replace(/^\/[^/]+/, '')}
            locale={otherLocale}
            className="text-xs opacity-60 hover:opacity-100 transition"
          >
            {otherLocale.toUpperCase()}
          </Link>
          <button className="px-4 py-2 bg-brand-primary text-black rounded-lg hover:opacity-90 transition">
            {t('cta')}
          </button>
        </div>
      </div>
    </header>
  );
}
