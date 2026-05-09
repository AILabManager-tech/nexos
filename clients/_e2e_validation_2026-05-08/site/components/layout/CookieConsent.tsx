'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Button } from '@/components/ui/Button';
import { Checkbox } from '@/components/ui/Checkbox';
import {
  CONSENT_KEY,
  DEFAULT_CONSENT,
  useConsent,
  type ConsentState,
} from '@/lib/consent';

export function CookieConsent() {
  const t = useTranslations('common.consent');
  const { hasConsented, saveConsent } = useConsent();
  const [details, setDetails] = useState(false);
  const [prefs, setPrefs] = useState<ConsentState>(DEFAULT_CONSENT);

  if (hasConsented) return null;

  const handleAcceptAll = () =>
    saveConsent({
      essential: true,
      analytics: true,
      marketing: true,
      timestamp: '',
    });

  const handleRejectAll = () =>
    saveConsent({
      essential: true,
      analytics: false,
      marketing: false,
      timestamp: '',
    });

  const handleSave = () =>
    saveConsent({ ...prefs, essential: true, timestamp: '' });

  const toggle = (key: 'analytics' | 'marketing') =>
    setPrefs((p) => ({ ...p, [key]: !p[key] }));

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={t('cookieTitle')}
      className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-surface p-4 shadow-lg sm:p-6"
    >
      <div className="mx-auto max-w-4xl">
        <h2 className="font-heading text-lg font-bold text-text">
          {t('cookieTitle')}
        </h2>
        <p className="mt-2 text-sm text-text-muted">{t('cookieBanner')}</p>

        {details && (
          <div className="mt-4 space-y-3 rounded border border-border bg-background p-4">
            <Checkbox
              checked
              disabled
              label={t('cookieEssentialLabel')}
              detail={t('cookieEssentialDescription')}
              onChange={() => undefined}
            />
            <Checkbox
              checked={prefs.analytics}
              onChange={() => toggle('analytics')}
              label={t('cookieAnalyticsLabel')}
              detail={t('cookieAnalyticsDescription')}
            />
            <Checkbox
              checked={prefs.marketing}
              onChange={() => toggle('marketing')}
              label={t('cookieMarketingLabel')}
              detail={t('cookieMarketingDescription')}
            />
          </div>
        )}

        <div className="mt-4 flex flex-col gap-2 sm:flex-row">
          <Button variant="secondary" className="flex-1" onClick={handleRejectAll}>
            {t('cookieDeclineAll')}
          </Button>
          {details ? (
            <Button variant="primary" className="flex-1" onClick={handleSave}>
              {t('cookieSavePreferences')}
            </Button>
          ) : (
            <Button
              variant="ghost"
              className="flex-1"
              onClick={() => setDetails(true)}
            >
              {t('cookieCustomize')}
            </Button>
          )}
          <Button variant="primary" className="flex-1" onClick={handleAcceptAll}>
            {t('cookieAcceptAll')}
          </Button>
        </div>

        <p className="mt-3 text-center text-xs text-text-muted">
          {t('privacyNotice')}{' '}
          <Link
            href="/politique-confidentialite"
            className="font-semibold text-primary underline"
          >
            {t('privacyLink')}
          </Link>
        </p>
      </div>
    </div>
  );
}

export function CookieSettingsButton() {
  const t = useTranslations('common.consent');
  const handleClick = () => {
    try {
      localStorage.removeItem(CONSENT_KEY);
    } catch {
      /* ignore */
    }
    window.location.reload();
  };
  return (
    <button
      type="button"
      onClick={handleClick}
      className="text-sm text-primary underline hover:text-primary-hover focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
    >
      {t('cookieTitle')}
    </button>
  );
}
