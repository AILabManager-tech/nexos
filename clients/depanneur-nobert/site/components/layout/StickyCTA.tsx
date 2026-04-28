'use client';

import { useTranslations } from 'next-intl';
import { Link, usePathname } from '@/i18n/routing';
import { useEffect, useState } from 'react';
import { ArrowRight, X } from 'lucide-react';
import { cn } from '@/lib/cn';

export function StickyCTA() {
  const t = useTranslations('common.stickyCta');
  const pathname = usePathname();
  const [isVisible, setIsVisible] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);

  useEffect(() => {
    setIsDismissed(false);
    const onScroll = () => setIsVisible(window.scrollY > 200);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, [pathname]);

  if (pathname.startsWith('/promotions')) return null;
  if (!isVisible || isDismissed) return null;

  return (
    <div
      className={cn(
        'fixed z-40 transition-all duration-300',
        'inset-x-0 bottom-0 sm:inset-x-auto sm:bottom-6 sm:right-6',
        'pb-[env(safe-area-inset-bottom)]'
      )}
    >
      <div className="bg-primary text-primary-foreground shadow-sticky-cta sm:rounded-lg flex items-stretch">
        <Link
          href="/promotions"
          aria-label={t('ariaLabel')}
          className="flex-1 inline-flex items-center justify-center gap-2 px-5 py-4 sm:py-3 font-semibold focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent focus-visible:ring-inset"
        >
          <span>{t('label')}</span>
          <ArrowRight size={18} aria-hidden="true" />
        </Link>
        <button
          type="button"
          aria-label={t('dismiss')}
          onClick={() => setIsDismissed(true)}
          className="px-3 border-l border-primary-hover hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent focus-visible:ring-inset"
        >
          <X size={18} aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}
