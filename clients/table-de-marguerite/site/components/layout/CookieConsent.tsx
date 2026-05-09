'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';

const STORAGE_KEY = 'tdm_cookie_consent_v1';

type Consent = {
  essentials: true;
  analytics: boolean;
  marketing: boolean;
  updated_at: string;
};

/**
 * Bandeau de consentement cookies (Loi 25 Québec — opt-in obligatoire).
 *
 * Apparaît si `localStorage[tdm_cookie_consent_v1]` est absent. Deux boutons
 * de visibilité équivalente : "Refuser tout" et "Accepter tout" (la Loi 25
 * art. 8.1 exige que le refus soit aussi simple que l'acceptation). Aucun
 * cookie tiers n'est posé tant que l'utilisateur n'a pas choisi — seul le
 * cookie next-intl `NEXT_LOCALE` (essentiel) est actif par défaut.
 */
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
      className="fixed inset-x-0 bottom-0 z-50 border-t border-primary-100 bg-surface/95 backdrop-blur"
    >
      <div className="mx-auto flex max-w-5xl flex-col gap-4 px-6 py-5 md:flex-row md:items-center md:justify-between">
        <div className="max-w-2xl">
          <p id="cookie-title" className="font-display text-lg text-ink">
            {t('banner_title')}
          </p>
          <p className="mt-1 text-sm text-ink-soft">{t('banner_body')}</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => save(false, false)}
            className="rounded-sm border border-primary-200 px-5 py-2 text-sm hover:bg-surface-alt transition-colors"
          >
            {t('reject_all')}
          </button>
          <button
            type="button"
            onClick={() => save(true, false)}
            className="rounded-sm bg-primary px-5 py-2 text-sm text-surface hover:bg-primary-600 transition-colors"
          >
            {t('accept_all')}
          </button>
        </div>
      </div>
    </div>
  );
}
