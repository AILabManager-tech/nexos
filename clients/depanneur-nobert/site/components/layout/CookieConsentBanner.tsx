'use client';

import { useTranslations } from 'next-intl';
import { useState } from 'react';
import { useConsent, DEFAULT_CONSENT } from '@/lib/cookieConsent';
import { Link } from '@/i18n/routing';

export function CookieConsentBanner() {
  const t = useTranslations('common.consent');
  const { hasConsented, isReady, saveConsent } = useConsent();
  const [showDetails, setShowDetails] = useState(false);
  const [analytics, setAnalytics] = useState(DEFAULT_CONSENT.analytics);
  const [marketing, setMarketing] = useState(DEFAULT_CONSENT.marketing);

  if (!isReady || hasConsented) return null;

  const acceptAll = () => saveConsent({ analytics: true, marketing: true });
  const declineAll = () => saveConsent({ analytics: false, marketing: false });
  const savePrefs = () => saveConsent({ analytics, marketing });

  return (
    <div
      role="dialog"
      aria-modal="false"
      aria-labelledby="cookie-banner-title"
      className="fixed inset-x-0 bottom-0 z-50 bg-surface border-t border-border shadow-card-hover pb-[env(safe-area-inset-bottom)]"
    >
      <div className="mx-auto max-w-5xl p-4 sm:p-6">
        <h2 id="cookie-banner-title" className="font-heading font-bold text-lg text-text">
          {t('bannerTitle')}
        </h2>
        <p className="mt-2 text-small text-text">{t('bannerBody')}</p>
        <p className="mt-1 text-small text-text-muted">
          <Link
            href="/politique-confidentialite"
            className="underline hover:text-primary focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
          >
            {t('bannerLearnMore')}
          </Link>
        </p>

        {showDetails && (
          <div className="mt-4 space-y-3">
            <CategoryRow
              title={t('categoryEssentialsTitle')}
              body={t('categoryEssentialsBody')}
              checked
              disabled
              onChange={() => undefined}
              ariaLabel={`${t('categoryEssentialsTitle')} — ${t('categoryEssentialsBody')}`}
            />
            <CategoryRow
              title={t('categoryAnalyticsTitle')}
              body={t('categoryAnalyticsBody')}
              checked={analytics}
              disabled={false}
              onChange={() => setAnalytics((v) => !v)}
              ariaLabel={`${t('categoryAnalyticsTitle')} — ${t('categoryAnalyticsBody')}`}
            />
            <CategoryRow
              title={t('categoryMarketingTitle')}
              body={t('categoryMarketingBody')}
              checked={marketing}
              disabled={false}
              onChange={() => setMarketing((v) => !v)}
              ariaLabel={`${t('categoryMarketingTitle')} — ${t('categoryMarketingBody')}`}
            />
          </div>
        )}

        <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button
            type="button"
            onClick={declineAll}
            className="h-12 rounded border border-border bg-surface text-text font-semibold hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
          >
            {t('actionDecline')}
          </button>
          {showDetails ? (
            <button
              type="button"
              onClick={savePrefs}
              className="h-12 rounded border border-primary bg-surface text-primary font-semibold hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
            >
              {t('actionSave')}
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setShowDetails(true)}
              className="h-12 rounded border border-primary bg-surface text-primary font-semibold hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
            >
              {t('actionCustomize')}
            </button>
          )}
          <button
            type="button"
            onClick={acceptAll}
            className="h-12 rounded bg-primary text-primary-foreground font-semibold hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
          >
            {t('actionAccept')}
          </button>
        </div>

        <p className="mt-3 text-small text-text-muted">
          {t('noticeLaw25', { rppEmail: 'nobert@depanneur-nobert.ca' })}
        </p>
      </div>
    </div>
  );
}

interface CategoryRowProps {
  title: string;
  body: string;
  checked: boolean;
  disabled: boolean;
  onChange: () => void;
  ariaLabel: string;
}

function CategoryRow({ title, body, checked, disabled, onChange, ariaLabel }: CategoryRowProps) {
  return (
    <label className="flex items-start gap-3 rounded border border-border bg-background-alt/50 p-3 cursor-pointer">
      <input
        type="checkbox"
        checked={checked}
        disabled={disabled}
        onChange={onChange}
        aria-label={ariaLabel}
        className="mt-1 h-5 w-5 accent-primary focus-visible:ring-3 focus-visible:ring-primary"
      />
      <div>
        <span className="font-semibold text-text">{title}</span>
        <p className="text-small text-text-muted mt-0.5">{body}</p>
      </div>
    </label>
  );
}
