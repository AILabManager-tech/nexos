"use client";

/**
 * NEXOS v3.0 — Composant Bandeau de Consentement Cookies
 *
 * Conforme Loi 25 du Quebec (art. 8.1) :
 * - Par defaut : seuls cookies essentiels actifs
 * - Consentement manifeste, libre et eclaire
 * - Bouton "Refuser" aussi visible que "Accepter"
 * - Categories : Essentiels / Analytics / Marketing
 * - Choix modifiable ulterieurement
 *
 * Usage :
 *   import { CookieConsent } from "@/components/cookie-consent";
 *   // Dans layout.tsx : <CookieConsent />
 */

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";

// ── Types ──────────────────────────────────────────────────────────

type CookieCategory = "essential" | "analytics" | "marketing";

interface ConsentState {
  essential: boolean; // Toujours true — non desactivable
  analytics: boolean;
  marketing: boolean;
  timestamp: string;
}

const CONSENT_KEY = "nexos-cookie-consent";

const DEFAULT_CONSENT: ConsentState = {
  essential: true,
  analytics: false,
  marketing: false,
  timestamp: "",
};

// ── Hook useConsent ────────────────────────────────────────────────

export function useConsent() {
  const [consent, setConsent] = useState<ConsentState | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem(CONSENT_KEY);
    if (stored) {
      try {
        setConsent(JSON.parse(stored));
      } catch {
        setConsent(null);
      }
    }
  }, []);

  const saveConsent = useCallback((newConsent: ConsentState) => {
    const withTimestamp = { ...newConsent, timestamp: new Date().toISOString() };
    localStorage.setItem(CONSENT_KEY, JSON.stringify(withTimestamp));
    setConsent(withTimestamp);

    // Activer/desactiver Google Analytics selon le consentement
    if (typeof window !== "undefined") {
      if (newConsent.analytics && window.gtag) {
        window.gtag("consent", "update", {
          analytics_storage: "granted",
        });
      } else if (window.gtag) {
        window.gtag("consent", "update", {
          analytics_storage: "denied",
        });
      }
    }
  }, []);

  const hasConsented = consent !== null;
  const isAnalyticsAllowed = consent?.analytics ?? false;
  const isMarketingAllowed = consent?.marketing ?? false;

  return { consent, saveConsent, hasConsented, isAnalyticsAllowed, isMarketingAllowed };
}

// ── Composant CookieConsent ───────────────────────────────────────

export function CookieConsent() {
  const { consent, saveConsent, hasConsented } = useConsent();
  const [showDetails, setShowDetails] = useState(false);
  const [preferences, setPreferences] = useState<ConsentState>(DEFAULT_CONSENT);

  // Ne pas afficher si deja consenti
  if (hasConsented) return null;

  const handleAcceptAll = () => {
    saveConsent({
      essential: true,
      analytics: true,
      marketing: true,
      timestamp: "",
    });
  };

  const handleRejectAll = () => {
    saveConsent({
      essential: true,
      analytics: false,
      marketing: false,
      timestamp: "",
    });
  };

  const handleSavePreferences = () => {
    saveConsent({ ...preferences, essential: true, timestamp: "" });
  };

  const toggleCategory = (category: CookieCategory) => {
    if (category === "essential") return; // Non desactivable
    setPreferences((prev) => ({ ...prev, [category]: !prev[category] }));
  };

  return (
    <div
      role="dialog"
      aria-label="Gestion des cookies"
      aria-modal="true"
      className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg p-4 md:p-6"
    >
      <div className="max-w-4xl mx-auto">
        {/* ── Message principal ── */}
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            Gestion des temoins (cookies)
          </h2>
          <p className="text-sm text-gray-600">
            Nous utilisons des temoins pour ameliorer votre experience sur notre site.
            Conformement a la{" "}
            <strong>Loi 25 du Quebec</strong>, seuls les temoins essentiels sont
            actifs par defaut. Vous pouvez accepter ou refuser les temoins optionnels.
          </p>
        </div>

        {/* ── Details (si ouverts) ── */}
        {showDetails && (
          <div className="mb-4 space-y-3">
            {/* Essentiels */}
            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <input
                type="checkbox"
                checked={true}
                disabled
                aria-label="Temoins essentiels (toujours actifs)"
                className="w-4 h-4 accent-blue-600"
              />
              <div>
                <span className="font-medium text-gray-900">Essentiels</span>
                <span className="ml-2 text-xs text-gray-500">(toujours actifs)</span>
                <p className="text-xs text-gray-500 mt-1">
                  Necessaires au fonctionnement du site. Ne peuvent pas etre desactives.
                </p>
              </div>
            </label>

            {/* Analytics */}
            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer">
              <input
                type="checkbox"
                checked={preferences.analytics}
                onChange={() => toggleCategory("analytics")}
                aria-label="Temoins analytiques"
                className="w-4 h-4 accent-blue-600"
              />
              <div>
                <span className="font-medium text-gray-900">Analytiques</span>
                <p className="text-xs text-gray-500 mt-1">
                  Nous aident a comprendre comment les visiteurs utilisent le site
                  (ex : Google Analytics).
                </p>
              </div>
            </label>

            {/* Marketing */}
            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer">
              <input
                type="checkbox"
                checked={preferences.marketing}
                onChange={() => toggleCategory("marketing")}
                aria-label="Temoins marketing"
                className="w-4 h-4 accent-blue-600"
              />
              <div>
                <span className="font-medium text-gray-900">Marketing</span>
                <p className="text-xs text-gray-500 mt-1">
                  Utilises pour afficher des publicites pertinentes et mesurer leur efficacite.
                </p>
              </div>
            </label>
          </div>
        )}

        {/* ── Boutons ── */}
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
          <button
            onClick={handleRejectAll}
            className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2"
            aria-label="Refuser tous les temoins optionnels"
          >
            Tout refuser
          </button>

          {showDetails ? (
            <button
              onClick={handleSavePreferences}
              className="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              aria-label="Sauvegarder mes preferences de temoins"
            >
              Sauvegarder mes choix
            </button>
          ) : (
            <button
              onClick={() => setShowDetails(true)}
              className="flex-1 px-4 py-2.5 text-sm font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              aria-label="Personnaliser les preferences de temoins"
            >
              Personnaliser
            </button>
          )}

          <button
            onClick={handleAcceptAll}
            className="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            aria-label="Accepter tous les temoins"
          >
            Tout accepter
          </button>
        </div>

        {/* ── Lien politique ── */}
        <p className="mt-3 text-xs text-gray-500 text-center">
          Pour en savoir plus, consultez notre{" "}
          <Link
            href="/politique-confidentialite"
            className="underline hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            politique de confidentialite
          </Link>
          .
        </p>
      </div>
    </div>
  );
}

// ── Composant pour modifier le consentement (footer) ──────────────

export function CookieSettingsButton() {
  const handleOpen = () => {
    localStorage.removeItem(CONSENT_KEY);
    window.location.reload();
  };

  return (
    <button
      onClick={handleOpen}
      className="text-sm text-gray-500 hover:text-gray-700 underline focus:outline-none focus:ring-2 focus:ring-blue-500"
      aria-label="Modifier mes preferences de temoins"
    >
      Gestion des temoins
    </button>
  );
}

// ── Types globaux pour gtag ───────────────────────────────────────

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}
