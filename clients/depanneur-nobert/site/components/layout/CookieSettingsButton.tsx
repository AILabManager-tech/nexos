'use client';

import { useLocale } from 'next-intl';
import { useConsent } from '@/lib/cookieConsent';

export function CookieSettingsButton() {
  const locale = useLocale();
  const { reset } = useConsent();
  const label = locale === 'en' ? 'Cookie settings' : 'Gestion des témoins';
  return (
    <button
      type="button"
      onClick={reset}
      className="underline hover:text-accent focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-accent rounded"
    >
      {label}
    </button>
  );
}
