// Tests clientConfig — placeholders + override via env (P4c).
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { getClientConfig, getTelHref } from '../lib/clientConfig';

const ENV_KEYS = [
  'NEXT_PUBLIC_VILLE',
  'NEXT_PUBLIC_ADRESSE_LIGNE',
  'NEXT_PUBLIC_CODE_POSTAL',
  'NEXT_PUBLIC_TELEPHONE',
  'NEXT_PUBLIC_EMAIL',
  'NEXT_PUBLIC_RPP_EMAIL',
  'NEXT_PUBLIC_NEQ',
  'NEXT_PUBLIC_ANNEE_FONDATION',
  'NEXT_PUBLIC_SITE_URL',
] as const;

describe('clientConfig — fallbacks placeholders Ph3', () => {
  const saved: Record<string, string | undefined> = {};

  beforeEach(() => {
    for (const key of ENV_KEYS) {
      saved[key] = process.env[key];
      delete process.env[key];
    }
  });

  afterEach(() => {
    for (const key of ENV_KEYS) {
      if (saved[key] === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = saved[key];
      }
    }
  });

  it('sans env : retourne tous les placeholders Ph3 (format {token})', () => {
    const config = getClientConfig();
    expect(config.ville).toBe('{ville}');
    expect(config.adresseLigne).toBe('{adresseLigne}');
    expect(config.codePostal).toBe('{codePostal}');
    expect(config.telephone).toBe('{telephone}');
    expect(config.NEQ).toBe('{NEQ}');
    expect(config.anneeFondation).toBe('{anneeFondation}');
  });

  it('email + rppEmail + baseUrl + domain : valeurs par défaut hardcodées (jamais placeholder)', () => {
    const config = getClientConfig();
    expect(config.email).toBe('info@depanneur-nobert.ca');
    expect(config.rppEmail).toBe('nobert@depanneur-nobert.ca');
    expect(config.baseUrl).toBe('https://depanneur-nobert.ca');
    expect(config.domain).toBe('depanneur-nobert.ca');
  });

  it('currentYear correspond à new Date().getFullYear()', () => {
    const config = getClientConfig();
    expect(config.currentYear).toBe(new Date().getFullYear());
  });

  it('env override : NEXT_PUBLIC_VILLE remplace le placeholder', () => {
    process.env.NEXT_PUBLIC_VILLE = 'Longueuil';
    const config = getClientConfig();
    expect(config.ville).toBe('Longueuil');
    expect(config.city).toBe('Longueuil');
  });

  it('getTelHref retourne # si pas de telephone configuré', () => {
    expect(getTelHref()).toBe('#');
  });

  it('getTelHref nettoie tous les chars non numériques (sauf +)', () => {
    process.env.NEXT_PUBLIC_TELEPHONE = '+1 (514) 555-1234';
    expect(getTelHref()).toBe('tel:+15145551234');
  });

  it('getTelHref accepte numéro sans + (format québécois standard)', () => {
    process.env.NEXT_PUBLIC_TELEPHONE = '(450) 555-9876';
    expect(getTelHref()).toBe('tel:4505559876');
  });
});
