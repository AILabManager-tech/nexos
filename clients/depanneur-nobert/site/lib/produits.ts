import produitsData from '@/data/produits.json';
import type { CategorieProduit, Produit } from '@/types';

export function getProduitsByCategory(
  category: CategorieProduit
): Produit[] {
  return (produitsData as Produit[]).filter((p) => p.category === category);
}

export function getAllCategories(): CategorieProduit[] {
  return ['bieres', 'snacks', 'lotto', 'essentiels'];
}
