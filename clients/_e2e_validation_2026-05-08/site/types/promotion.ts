export interface Promotion {
  id: string;
  image: string;
  title_fr: string;
  title_en: string;
  alt_fr: string;
  alt_en: string;
  priceBefore: number;
  priceAfter: number;
  unit_fr?: string;
  unit_en?: string;
  validFrom: string;
  validTo: string;
}
