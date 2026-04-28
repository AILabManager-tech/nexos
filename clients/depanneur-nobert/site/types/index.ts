export type Locale = 'fr' | 'en';

export type CategorieProduit = 'bieres' | 'snacks' | 'lotto' | 'essentiels';

export interface Promotion {
  id: string;
  category: CategorieProduit;
  title: { fr: string; en: string };
  description?: { fr: string; en: string };
  regularPrice?: number;
  promoPrice?: number;
  validFrom: string;
  validUntil: string;
  image?: string;
  imageAlt?: { fr: string; en: string };
  limitedStock?: boolean;
}

export interface Produit {
  id: string;
  category: CategorieProduit;
  name: { fr: string; en: string };
  description?: { fr: string; en: string };
  format?: string;
  marque?: string;
  origine?: string;
  image?: string;
  imageAlt?: { fr: string; en: string };
  outOfStock?: boolean;
}

export interface Temoignage {
  id: string;
  name: string;
  role: { fr: string; en: string };
  quote: { fr: string; en: string };
  image?: string;
  consentDate?: string;
}

export interface HoraireJour {
  day:
    | 'monday'
    | 'tuesday'
    | 'wednesday'
    | 'thursday'
    | 'friday'
    | 'saturday'
    | 'sunday';
  open?: string;
  close?: string;
  closed?: boolean;
}

export interface Horaires {
  regular: HoraireJour[];
  exceptions?: Array<{ date: string; note: { fr: string; en: string } }>;
}
