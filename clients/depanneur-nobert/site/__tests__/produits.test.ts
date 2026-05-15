// Tests produits — catégories + filtrage (P4c).
import { describe, expect, it } from 'vitest';
import { getAllCategories, getProduitsByCategory } from '../lib/produits';

describe('produits — catégories', () => {
  it('getAllCategories retourne les 4 catégories canoniques', () => {
    const categories = getAllCategories();
    expect(categories).toEqual(['bieres', 'snacks', 'lotto', 'essentiels']);
  });

  it('getProduitsByCategory ne retourne que la catégorie demandée', () => {
    for (const category of getAllCategories()) {
      const filtered = getProduitsByCategory(category);
      for (const produit of filtered) {
        expect(produit.category).toBe(category);
      }
    }
  });

  it('getProduitsByCategory retourne un Array (jamais undefined)', () => {
    const result = getProduitsByCategory('bieres');
    expect(Array.isArray(result)).toBe(true);
  });
});
