/**
 * Format a numeric amount as Canadian dollars (`fr-CA` or `en-CA`).
 *
 * @param amount - Amount in CAD (e.g. `12.5`).
 * @param locale - `'fr'` (default) or `'en'`.
 * @returns Locale-aware currency string with two decimals.
 */
export function formatPrice(amount: number, locale: string = 'fr'): string {
  const lang = locale === 'en' ? 'en-CA' : 'fr-CA';
  return new Intl.NumberFormat(lang, {
    style: 'currency',
    currency: 'CAD',
    minimumFractionDigits: 2,
  }).format(amount);
}

/**
 * Format an ISO date string as a long Canadian date.
 *
 * @param iso - ISO 8601 date string.
 * @param locale - `'fr'` (default) or `'en'`.
 * @returns e.g. `8 mai 2026` (FR) or `May 8, 2026` (EN).
 */
export function formatDate(iso: string, locale: string = 'fr'): string {
  const lang = locale === 'en' ? 'en-CA' : 'fr-CA';
  const d = new Date(iso);
  return d.toLocaleDateString(lang, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Format an ISO date string as a short Canadian date (no year).
 *
 * @param iso - ISO 8601 date string.
 * @param locale - `'fr'` (default) or `'en'`.
 * @returns e.g. `8 mai` (FR) or `May 8` (EN).
 */
export function formatDateShort(iso: string, locale: string = 'fr'): string {
  const lang = locale === 'en' ? 'en-CA' : 'fr-CA';
  const d = new Date(iso);
  return d.toLocaleDateString(lang, { month: 'short', day: 'numeric' });
}

/**
 * Format a 10-digit Canadian phone number into `(XXX) XXX-XXXX`.
 * Returns the raw input unchanged if it is not exactly 10 digits.
 *
 * @param raw - Input that may contain non-digit separators.
 */
export function formatPhone(raw: string): string {
  const digits = raw.replace(/\D/g, '');
  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  }
  return raw;
}

/**
 * Build a `tel:` URI from any phone-like string. Keeps the last 10 digits
 * and prefixes the North-American country code.
 *
 * @param raw - Input that may contain non-digit separators or extra digits.
 */
export function phoneTel(raw: string): string {
  const digits = raw.replace(/\D/g, '');
  return `tel:+1${digits.slice(-10)}`;
}
