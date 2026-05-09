export function formatPrice(amount: number, locale: string = 'fr'): string {
  const lang = locale === 'en' ? 'en-CA' : 'fr-CA';
  return new Intl.NumberFormat(lang, {
    style: 'currency',
    currency: 'CAD',
    minimumFractionDigits: 2,
  }).format(amount);
}

export function formatDate(iso: string, locale: string = 'fr'): string {
  const lang = locale === 'en' ? 'en-CA' : 'fr-CA';
  const d = new Date(iso);
  return d.toLocaleDateString(lang, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function formatDateShort(iso: string, locale: string = 'fr'): string {
  const lang = locale === 'en' ? 'en-CA' : 'fr-CA';
  const d = new Date(iso);
  return d.toLocaleDateString(lang, { month: 'short', day: 'numeric' });
}

export function formatPhone(raw: string): string {
  const digits = raw.replace(/\D/g, '');
  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  }
  return raw;
}

export function phoneTel(raw: string): string {
  const digits = raw.replace(/\D/g, '');
  return `tel:+1${digits.slice(-10)}`;
}
