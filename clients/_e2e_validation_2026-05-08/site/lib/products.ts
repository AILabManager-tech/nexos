import productsData from '@/site/data/products-categories.json';
import type { Category, CategoryId } from '@/types/product';

export function getCategories(): Category[] {
  return (productsData as { categories: Category[] }).categories;
}

export function getCategoryById(id: CategoryId): Category | undefined {
  return getCategories().find((c) => c.id === id);
}
