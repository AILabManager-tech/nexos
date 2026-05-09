'use client';

import { useCallback, useEffect, useState } from 'react';

export type ConsentState = {
  essential: boolean;
  analytics: boolean;
  marketing: boolean;
  timestamp: string;
};

export const CONSENT_KEY = 'nexos-cookie-consent';

export const DEFAULT_CONSENT: ConsentState = {
  essential: true,
  analytics: false,
  marketing: false,
  timestamp: '',
};

export function useConsent() {
  const [consent, setConsent] = useState<ConsentState | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(CONSENT_KEY);
      if (stored) {
        setConsent(JSON.parse(stored) as ConsentState);
      }
    } catch {
      setConsent(null);
    }
  }, []);

  const saveConsent = useCallback((next: ConsentState) => {
    const withTs = { ...next, timestamp: new Date().toISOString() };
    try {
      localStorage.setItem(CONSENT_KEY, JSON.stringify(withTs));
    } catch {
      /* ignore */
    }
    setConsent(withTs);
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('consent', 'update', {
        analytics_storage: next.analytics ? 'granted' : 'denied',
        ad_storage: next.marketing ? 'granted' : 'denied',
      });
    }
  }, []);

  return {
    consent,
    saveConsent,
    hasConsented: consent !== null,
    isAnalyticsAllowed: consent?.analytics ?? false,
    isMarketingAllowed: consent?.marketing ?? false,
  };
}

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}
