/**
 * Variables d'interpolation client (kickoff dependencies).
 * Lues depuis l'environnement avec des placeholders explicites en fallback,
 * conformément à la décision Ph3 (préserver les placeholders next-intl
 * tant que les 6 variables critiques ne sont pas fixées par le client).
 */

export interface ClientConfig {
  ville: string;
  city: string;
  adresseLigne: string;
  codePostal: string;
  telephone: string;
  email: string;
  rppEmail: string;
  NEQ: string;
  anneeFondation: string;
  currentYear: number;
  baseUrl: string;
  domain: string;
}

const placeholder = (token: string): string => `{${token}}`;

export function getClientConfig(): ClientConfig {
  const ville = process.env.NEXT_PUBLIC_VILLE ?? placeholder('ville');
  return {
    ville,
    city: ville,
    adresseLigne:
      process.env.NEXT_PUBLIC_ADRESSE_LIGNE ?? placeholder('adresseLigne'),
    codePostal:
      process.env.NEXT_PUBLIC_CODE_POSTAL ?? placeholder('codePostal'),
    telephone: process.env.NEXT_PUBLIC_TELEPHONE ?? placeholder('telephone'),
    email: process.env.NEXT_PUBLIC_EMAIL ?? 'info@depanneur-nobert.ca',
    rppEmail:
      process.env.NEXT_PUBLIC_RPP_EMAIL ?? 'nobert@depanneur-nobert.ca',
    NEQ: process.env.NEXT_PUBLIC_NEQ ?? placeholder('NEQ'),
    anneeFondation:
      process.env.NEXT_PUBLIC_ANNEE_FONDATION ?? placeholder('anneeFondation'),
    currentYear: new Date().getFullYear(),
    baseUrl:
      process.env.NEXT_PUBLIC_SITE_URL ?? 'https://depanneur-nobert.ca',
    domain: 'depanneur-nobert.ca',
  };
}

export function getTelHref(): string {
  const tel = process.env.NEXT_PUBLIC_TELEPHONE;
  if (!tel) return '#';
  return `tel:${tel.replace(/[^0-9+]/g, '')}`;
}
