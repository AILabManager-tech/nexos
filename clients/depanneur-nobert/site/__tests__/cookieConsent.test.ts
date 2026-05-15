import { describe, expect, it } from 'vitest';
import { DEFAULT_CONSENT } from '../lib/cookieConsent';

describe('cookieConsent — Loi 25 defaults', () => {
  it('essential cookies sont toujours actifs (true par défaut)', () => {
    // Loi 25 Québec : les cookies essentiels au fonctionnement ne nécessitent
    // pas de consentement opt-in mais ne doivent pas servir à du tracking.
    expect(DEFAULT_CONSENT.essential).toBe(true);
  });

  it('analytics est OFF par défaut (opt-in requis)', () => {
    // Loi 25 art. 8.1 : consentement libre, éclairé, spécifique. Aucun
    // tracking analytics avant action utilisateur explicite.
    expect(DEFAULT_CONSENT.analytics).toBe(false);
  });

  it('marketing est OFF par défaut (opt-in requis)', () => {
    expect(DEFAULT_CONSENT.marketing).toBe(false);
  });

  it("timestamp vide par défaut (signale qu'aucun choix n'a été fait)", () => {
    expect(DEFAULT_CONSENT.timestamp).toBe('');
  });
});
