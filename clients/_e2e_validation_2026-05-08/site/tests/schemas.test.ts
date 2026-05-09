import { describe, it, expect } from 'vitest';
import { NewsletterSchema, ContactSchema } from '@/lib/schemas';

describe('NewsletterSchema', () => {
  it('accepts a minimal valid payload', () => {
    const r = NewsletterSchema.safeParse({ email: 'a@b.ca', consent: true });
    expect(r.success).toBe(true);
  });

  it('rejects an invalid email', () => {
    const r = NewsletterSchema.safeParse({ email: 'not-an-email', consent: true });
    expect(r.success).toBe(false);
  });

  it('rejects when consent is not strictly true (Loi 25 opt-in)', () => {
    expect(NewsletterSchema.safeParse({ email: 'a@b.ca', consent: false }).success).toBe(false);
    expect(NewsletterSchema.safeParse({ email: 'a@b.ca' }).success).toBe(false);
  });

  it('allows the optional honeypot field', () => {
    const r = NewsletterSchema.safeParse({ email: 'a@b.ca', consent: true, hp: '' });
    expect(r.success).toBe(true);
  });
});

describe('ContactSchema', () => {
  const valid = {
    name: 'Jean Tremblay',
    email: 'jean@example.ca',
    phone: '514-555-1234',
    message: 'Bonjour, est-ce que vous avez de la glace en stock ?',
    consent: true,
  };

  it('accepts a complete valid payload', () => {
    expect(ContactSchema.safeParse(valid).success).toBe(true);
  });

  it('accepts an empty phone', () => {
    expect(ContactSchema.safeParse({ ...valid, phone: '' }).success).toBe(true);
    const { phone, ...noPhone } = valid;
    void phone;
    expect(ContactSchema.safeParse(noPhone).success).toBe(true);
  });

  it('rejects an empty name', () => {
    expect(ContactSchema.safeParse({ ...valid, name: '' }).success).toBe(false);
  });

  it('rejects a too-short message (< 5 chars)', () => {
    expect(ContactSchema.safeParse({ ...valid, message: 'hi' }).success).toBe(false);
  });

  it('rejects a too-long message (> 1000 chars)', () => {
    expect(ContactSchema.safeParse({ ...valid, message: 'x'.repeat(1001) }).success).toBe(false);
  });

  it('rejects when consent is not strictly true', () => {
    expect(ContactSchema.safeParse({ ...valid, consent: false }).success).toBe(false);
  });
});
