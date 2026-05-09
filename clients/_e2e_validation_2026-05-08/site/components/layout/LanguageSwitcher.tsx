'use client';

import { useLocale, useTranslations } from 'next-intl';
import { usePathname, useRouter } from '@/i18n/routing';

export function LanguageSwitcher() {
  const t = useTranslations('common.nav');
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();
  const target = locale === 'fr' ? 'en' : 'fr';
  const targetLabel = target === 'en' ? t('switchToEn') : t('switchToFr');

  const handleSwitch = () => {
    router.replace(pathname, { locale: target });
  };

  return (
    <button
      type="button"
      onClick={handleSwitch}
      aria-label={`${t('languageSwitcher')} : ${targetLabel}`}
      className="inline-flex items-center gap-1 rounded px-3 py-2 text-sm font-semibold text-primary hover:bg-surface-alt focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
    >
      <span aria-hidden="true">{target.toUpperCase()}</span>
      <span className="sr-only">{targetLabel}</span>
    </button>
  );
}
