'use client';

import { Menu, X } from 'lucide-react';
import { useTranslations } from 'next-intl';
import { useEffect, useState } from 'react';
import { Link, usePathname } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { LanguageSwitcher } from './LanguageSwitcher';
import { cn } from '@/lib/utils';

const NAV_ITEMS = [
  { key: 'home', href: '/' as const },
  { key: 'promotions', href: '/promotions' as const },
  { key: 'products', href: '/produits' as const },
  { key: 'contact', href: '/contact' as const },
];

export function Header() {
  const t = useTranslations('common.nav');
  const tBrand = useTranslations('common.brand');
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    if (open) document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open]);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur-sm">
      <Container className="flex items-center justify-between py-4">
        <Link
          href="/"
          className="font-heading text-2xl font-extrabold tracking-tight text-primary focus-visible:ring-3 focus-visible:ring-primary"
        >
          {tBrand('wordmark')}
        </Link>

        <nav
          aria-label={t('home')}
          className="hidden items-center gap-1 lg:flex"
        >
          {NAV_ITEMS.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.key}
                href={item.href}
                aria-current={active ? 'page' : undefined}
                className={cn(
                  'rounded px-4 py-2 text-base font-semibold text-text transition-colors hover:text-primary',
                  active && 'text-primary underline underline-offset-4',
                )}
              >
                {t(item.key)}
              </Link>
            );
          })}
          <LanguageSwitcher />
        </nav>

        <button
          type="button"
          aria-label={open ? t('closeMenu') : t('openMenu')}
          aria-expanded={open}
          aria-controls="mobile-drawer"
          onClick={() => setOpen((v) => !v)}
          className="inline-flex h-12 w-12 items-center justify-center rounded text-primary lg:hidden focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
        >
          {open ? <X size={24} aria-hidden="true" /> : <Menu size={24} aria-hidden="true" />}
        </button>
      </Container>

      {open && (
        <div
          id="mobile-drawer"
          role="dialog"
          aria-modal="true"
          aria-label={t('openMenu')}
          className="fixed inset-0 top-[73px] z-50 bg-background lg:hidden"
        >
          <Container className="flex flex-col gap-2 py-6">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.key}
                href={item.href}
                className="rounded px-4 py-3 text-lg font-semibold text-text hover:bg-surface-alt"
              >
                {t(item.key)}
              </Link>
            ))}
            <div className="mt-2 border-t border-border pt-4">
              <LanguageSwitcher />
            </div>
          </Container>
        </div>
      )}
    </header>
  );
}
