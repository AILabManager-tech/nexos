'use client';

import { useCallback, useEffect, useState } from 'react';

export type ConsentCategory = 'analytics' | 'marketing';

export interface ConsentState {
  essential: true;
  analytics: boolean;
  marketing: boolean;
  timestamp: string;
}

const CONSENT_KEY = 'nobert-cookie-consent';
const CONSENT_EVENT = 'nobert:consent-updated';

export const DEFAULT_CONSENT: ConsentState = {
  essential: true,
  analytics: false,
  marketing: false,
  timestamp: '',
};

function readStored(): ConsentState | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = window.localStorage.getItem(CONSENT_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as ConsentState;
    return { ...parsed, essential: true };
  } catch {
    return null;
  }
}

export function useConsent() {
  const [consent, setConsent] = useState<ConsentState | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    setConsent(readStored());
    setIsReady(true);
    const handler = () => setConsent(readStored());
    window.addEventListener(CONSENT_EVENT, handler);
    return () => window.removeEventListener(CONSENT_EVENT, handler);
  }, []);

  const saveConsent = useCallback((next: Omit<ConsentState, 'timestamp' | 'essential'>) => {
    const value: ConsentState = {
      essential: true,
      analytics: next.analytics,
      marketing: next.marketing,
      timestamp: new Date().toISOString(),
    };
    window.localStorage.setItem(CONSENT_KEY, JSON.stringify(value));
    setConsent(value);
    window.dispatchEvent(new CustomEvent(CONSENT_EVENT));
  }, []);

  const reset = useCallback(() => {
    window.localStorage.removeItem(CONSENT_KEY);
    setConsent(null);
    window.dispatchEvent(new CustomEvent(CONSENT_EVENT));
  }, []);

  return {
    consent,
    isReady,
    hasConsented: consent !== null,
    isAnalyticsAllowed: consent?.analytics ?? false,
    isMarketingAllowed: consent?.marketing ?? false,
    saveConsent,
    reset,
  };
}
