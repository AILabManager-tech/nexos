'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';

const STORAGE_KEY = 'emi_cookie_consent_v1';

type Consent = {
  essentials: true;
  analytics: boolean;
  marketing: boolean;
  updated_at: string;
};

export function CookieConsent() {
  const t = useTranslations('cookies');
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) setVisible(true);
  }, []);

  const save = (analytics: boolean, marketing: boolean) => {
    const consent: Consent = {
      essentials: true,
      analytics,
      marketing,
      updated_at: new Date().toISOString()
    };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(consent));
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div
      role="dialog"
      aria-labelledby="cookie-title"
      className="fixed inset-x-0 bottom-0 z-50 border-t border-primary-800 bg-surface/95 backdrop-blur"
    >
      <div className="mx-auto flex max-w-5xl flex-col gap-4 px-6 py-5 md:flex-row md:items-center md:justify-between">
        <div className="max-w-2xl">
          <p id="cookie-title" className="font-heading text-lg text-ink">
            {t('banner_title')}
          </p>
          <p className="mt-1 text-sm text-ink-soft">{t('banner_body')}</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => save(false, false)}
            className="rounded-sm border border-primary-700 px-5 py-2 text-sm hover:bg-surface-raised transition-colors"
          >
            {t('reject_all')}
          </button>
          <button
            type="button"
            onClick={() => save(true, false)}
            className="rounded-sm bg-primary px-5 py-2 text-sm text-ink hover:bg-primary-600 transition-colors"
          >
            {t('accept_all')}
          </button>
        </div>
      </div>
    </div>
  );
}
