export type CategoryId =
  | 'bieres'
  | 'snacks'
  | 'boissons'
  | 'loto'
  | 'depannage'
  | 'glace';

export interface Product {
  id: string;
  name_fr: string;
  name_en: string;
  alt_fr: string;
  alt_en: string;
  image: string;
  priceIndicative?: number;
  available: boolean;
}

export interface Category {
  id: CategoryId;
  name_fr: string;
  name_en: string;
  description_fr: string;
  description_en: string;
  icon: string;
  products: Product[];
}
