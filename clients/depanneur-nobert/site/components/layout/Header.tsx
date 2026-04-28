'use client';

import { useTranslations } from 'next-intl';
import { Link, usePathname } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Logo } from '@/components/layout/Logo';
import { LanguageSwitcher } from '@/components/layout/LanguageSwitcher';
import { Menu, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { cn } from '@/lib/cn';

const NAV_ITEMS: Array<{
  href: '/' | '/promotions' | '/produits' | '/contact';
  label: 'home' | 'promotions' | 'produits' | 'contact';
  highlight?: boolean;
}> = [
  { href: '/', label: 'home' },
  { href: '/promotions', label: 'promotions', highlight: true },
  { href: '/produits', label: 'produits' },
  { href: '/contact', label: 'contact' },
];

export function Header() {
  const t = useTranslations('common.nav');
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  return (
    <header
      className="sticky top-0 z-40 bg-surface border-b border-border shadow-sm"
      role="banner"
    >
      <Container className="flex items-center justify-between h-16 lg:h-20">
        <Link
          href="/"
          aria-label="Dépanneur Nobert"
          className="focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
        >
          <Logo />
        </Link>

        <nav aria-label="Primary" className="hidden lg:flex items-center gap-6">
          <ul className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const isActive =
                item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={isActive ? 'page' : undefined}
                    className={cn(
                      'inline-flex items-center px-4 py-2 rounded text-base font-semibold',
                      'transition-colors duration-150',
                      'focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2',
                      isActive
                        ? 'text-primary bg-primary-subtle'
                        : 'text-text hover:text-primary hover:bg-primary-subtle',
                      item.highlight && !isActive && 'text-primary'
                    )}
                  >
                    {t(item.label)}
                  </Link>
                </li>
              );
            })}
          </ul>
          <LanguageSwitcher />
        </nav>

        <div className="flex items-center gap-2 lg:hidden">
          <LanguageSwitcher />
          <button
            type="button"
            aria-label={isOpen ? t('closeMenu') : t('openMenu')}
            aria-expanded={isOpen}
            aria-controls="mobile-nav"
            onClick={() => setIsOpen((prev) => !prev)}
            className="inline-flex h-12 w-12 items-center justify-center rounded text-text hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
          >
            {isOpen ? <X size={24} aria-hidden="true" /> : <Menu size={24} aria-hidden="true" />}
          </button>
        </div>
      </Container>

      {isOpen && (
        <nav
          id="mobile-nav"
          aria-label="Mobile"
          className="lg:hidden border-t border-border bg-surface"
        >
          <ul className="flex flex-col gap-1 p-4">
            {NAV_ITEMS.map((item) => {
              const isActive =
                item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={isActive ? 'page' : undefined}
                    onClick={() => setIsOpen(false)}
                    className={cn(
                      'block px-4 py-3 rounded text-lg font-semibold',
                      'focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary',
                      isActive
                        ? 'text-primary bg-primary-subtle'
                        : 'text-text hover:bg-primary-subtle'
                    )}
                  >
                    {t(item.label)}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      )}
    </header>
  );
}
