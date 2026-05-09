import { describe, it, expect } from 'vitest';
import { formatPrice, formatDate, formatDateShort, formatPhone, phoneTel } from '@/lib/format';

describe('formatPrice', () => {
  it('formats CAD currency in French (FR-CA) by default', () => {
    const out = formatPrice(12.5);
    expect(out).toMatch(/12,50/);
    expect(out).toMatch(/\$/);
  });

  it('formats CAD currency in English (EN-CA)', () => {
    const out = formatPrice(12.5, 'en');
    expect(out).toMatch(/12\.50/);
    expect(out).toMatch(/\$/);
  });

  it('keeps two decimals for whole numbers', () => {
    expect(formatPrice(7, 'en')).toMatch(/7\.00/);
  });
});

describe('formatDate', () => {
  it('renders FR-CA long date', () => {
    const out = formatDate('2026-05-08T12:00:00Z', 'fr');
    expect(out).toMatch(/2026/);
    expect(out.toLowerCase()).toMatch(/mai/);
  });

  it('renders EN-CA long date', () => {
    const out = formatDate('2026-05-08T12:00:00Z', 'en');
    expect(out).toMatch(/2026/);
    expect(out.toLowerCase()).toMatch(/may/);
  });
});

describe('formatDateShort', () => {
  it('renders short FR-CA date', () => {
    const out = formatDateShort('2026-05-08T12:00:00Z', 'fr');
    expect(out.length).toBeGreaterThan(0);
    expect(out.toLowerCase()).toMatch(/mai/);
  });

  it('renders short EN-CA date', () => {
    const out = formatDateShort('2026-05-08T12:00:00Z', 'en');
    expect(out).toMatch(/May/);
  });
});

describe('formatPhone', () => {
  it('formats a 10-digit number into Canadian format', () => {
    expect(formatPhone('5145551234')).toBe('(514) 555-1234');
  });

  it('strips non-digit separators before formatting', () => {
    expect(formatPhone('514.555.1234')).toBe('(514) 555-1234');
    expect(formatPhone('514-555-1234')).toBe('(514) 555-1234');
  });

  it('returns the raw input when not exactly 10 digits', () => {
    expect(formatPhone('123')).toBe('123');
    expect(formatPhone('+1 514 555 1234')).toBe('+1 514 555 1234');
  });
});

describe('phoneTel', () => {
  it('builds a tel: URI with leading +1', () => {
    expect(phoneTel('(514) 555-1234')).toBe('tel:+15145551234');
  });

  it('takes the last 10 digits when extra digits present', () => {
    expect(phoneTel('001 514 555 1234')).toBe('tel:+15145551234');
  });
});
