// Tests Zod schemas — validation formulaires Contact + Newsletter (P4c).
// Vise à empêcher toute régression sur les contrats d'entrée API.
import { describe, expect, it } from 'vitest';
import { ContactSchema, NewsletterSchema } from '../lib/schemas';

describe('NewsletterSchema', () => {
  it('accepte un payload minimal valide', () => {
    const result = NewsletterSchema.safeParse({
      email: 'user@example.com',
      consent: true,
    });
    expect(result.success).toBe(true);
    // Locale par défaut = 'fr' (valeur explicite Loi 25 Québec).
    if (result.success) {
      expect(result.data.locale).toBe('fr');
    }
  });

  it('rejette un email invalide', () => {
    const result = NewsletterSchema.safeParse({
      email: 'not-an-email',
      consent: true,
    });
    expect(result.success).toBe(false);
  });

  it('rejette consent=false (Loi 25 — opt-in obligatoire)', () => {
    const result = NewsletterSchema.safeParse({
      email: 'user@example.com',
      consent: false,
    });
    expect(result.success).toBe(false);
  });

  it('accepte honeypot vide (string < 1 char)', () => {
    const result = NewsletterSchema.safeParse({
      email: 'user@example.com',
      consent: true,
      honeypot: '',
    });
    expect(result.success).toBe(true);
  });

  it('rejette honeypot rempli (bot detection)', () => {
    const result = NewsletterSchema.safeParse({
      email: 'user@example.com',
      consent: true,
      honeypot: 'spambot was here',
    });
    expect(result.success).toBe(false);
  });

  it('rejette email > 254 chars (limite RFC 5321)', () => {
    const longLocal = 'a'.repeat(250);
    const result = NewsletterSchema.safeParse({
      email: `${longLocal}@a.co`,
      consent: true,
    });
    expect(result.success).toBe(false);
  });

  it("accepte locale 'en' explicite", () => {
    const result = NewsletterSchema.safeParse({
      email: 'user@example.com',
      consent: true,
      locale: 'en',
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.locale).toBe('en');
    }
  });

  it("rejette locale autre que 'fr' ou 'en'", () => {
    const result = NewsletterSchema.safeParse({
      email: 'user@example.com',
      consent: true,
      locale: 'es',
    });
    expect(result.success).toBe(false);
  });
});

describe('ContactSchema', () => {
  const baseValid = {
    name: 'Jean Tremblay',
    email: 'jean@example.com',
    message: 'Bonjour, je voudrais des informations sur vos produits.',
    consent: true,
  };

  it('accepte un payload minimal valide', () => {
    const result = ContactSchema.safeParse(baseValid);
    expect(result.success).toBe(true);
  });

  it('rejette name trop court (< 2 chars)', () => {
    const result = ContactSchema.safeParse({ ...baseValid, name: 'A' });
    expect(result.success).toBe(false);
  });

  it('rejette name > 100 chars', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      name: 'A'.repeat(101),
    });
    expect(result.success).toBe(false);
  });

  it('trim les espaces autour du name', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      name: '   Jean Tremblay   ',
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.name).toBe('Jean Tremblay');
    }
  });

  it('rejette message < 10 chars', () => {
    const result = ContactSchema.safeParse({ ...baseValid, message: 'court' });
    expect(result.success).toBe(false);
  });

  it('rejette message > 2000 chars', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      message: 'a'.repeat(2001),
    });
    expect(result.success).toBe(false);
  });

  it('accepte phone vide (champ optionnel)', () => {
    const result = ContactSchema.safeParse({ ...baseValid, phone: '' });
    expect(result.success).toBe(true);
  });

  it('accepte phone format québécois (514) 555-1234', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      phone: '(514) 555-1234',
    });
    expect(result.success).toBe(true);
  });

  it('accepte phone format international +1 514 555 1234', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      phone: '+1 514 555 1234',
    });
    expect(result.success).toBe(true);
  });

  it('rejette phone avec lettres (anti-injection)', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      phone: '514-CALL-NOW',
    });
    expect(result.success).toBe(false);
  });

  it('rejette phone > 20 chars', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      phone: '+1 (514) 555-1234 ext.12345',
    });
    expect(result.success).toBe(false);
  });

  it('rejette honeypot rempli', () => {
    const result = ContactSchema.safeParse({
      ...baseValid,
      honeypot: 'bot',
    });
    expect(result.success).toBe(false);
  });

  it('rejette consent=false (Loi 25)', () => {
    const result = ContactSchema.safeParse({ ...baseValid, consent: false });
    expect(result.success).toBe(false);
  });

  it('rejette consent absent (default consent strict)', () => {
    const { consent: _consent, ...withoutConsent } = baseValid;
    const result = ContactSchema.safeParse(withoutConsent);
    expect(result.success).toBe(false);
  });
});
