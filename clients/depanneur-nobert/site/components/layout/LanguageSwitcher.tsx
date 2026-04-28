'use client';

import { useTranslations } from 'next-intl';
import { useLocale } from 'next-intl';
import { usePathname, useRouter } from '@/i18n/routing';
import { type Locale } from '@/i18n/routing';
import { useTransition } from 'react';

export function LanguageSwitcher() {
  const t = useTranslations('common.languageSwitcher');
  const locale = useLocale() as Locale;
  const router = useRouter();
  const pathname = usePathname();
  const [isPending, startTransition] = useTransition();

  const otherLocale: Locale = locale === 'fr' ? 'en' : 'fr';

  const handleSwitch = () => {
    startTransition(() => {
      router.replace(pathname, { locale: otherLocale });
    });
  };

  return (
    <button
      type="button"
      onClick={handleSwitch}
      disabled={isPending}
      aria-label={t('ariaLabel')}
      className="inline-flex items-center gap-2 rounded px-3 py-2 text-small font-semibold text-text hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
    >
      <span aria-hidden="true">{locale === 'fr' ? 'EN' : 'FR'}</span>
      <span className="sr-only">{t(otherLocale)}</span>
    </button>
  );
}
