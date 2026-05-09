'use client';

import { ArrowRight } from 'lucide-react';
import { useTranslations } from 'next-intl';
import { Link, usePathname } from '@/i18n/routing';

const HIDDEN_PATHS = new Set<string>([
  '/promotions',
  '/politique-confidentialite',
  '/mentions-legales',
]);

export function StickyMobileCta() {
  const t = useTranslations('common.stickyCta');
  const pathname = usePathname();

  if (HIDDEN_PATHS.has(pathname)) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-30 border-t border-border bg-accent shadow-sticky-cta lg:hidden pb-safe">
      <Link
        href="/promotions"
        aria-label={t('ariaLabel')}
        className="flex min-h-[56px] items-center justify-center gap-2 px-4 py-3 text-base font-semibold text-accent-foreground focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
      >
        <span>{t('label')}</span>
        <ArrowRight size={20} aria-hidden="true" />
      </Link>
    </div>
  );
}
