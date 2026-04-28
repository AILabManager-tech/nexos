'use client';

// Section: S-014 | produits.ProduitsCategoriesNav | i18n: produits.categoriesNav
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';

const ITEMS: Array<{ key: 'bieres' | 'snacks' | 'lotto' | 'essentiels' }> = [
  { key: 'bieres' },
  { key: 'snacks' },
  { key: 'lotto' },
  { key: 'essentiels' },
];

export function ProduitsCategoriesNav() {
  const t = useTranslations('produits.categoriesNav');
  return (
    <nav
      aria-label={t('ariaLabel')}
      className="sticky top-16 lg:top-20 z-30 bg-surface border-b border-border shadow-sm"
    >
      <Container>
        <ul className="flex gap-2 overflow-x-auto py-3" role="list">
          {ITEMS.map(({ key }) => (
            <li key={key} className="shrink-0">
              <a
                href={`#${key}`}
                className="inline-flex items-center h-10 px-4 rounded-full border border-border bg-surface text-text font-semibold text-small hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
              >
                {t(`items.${key}`)}
              </a>
            </li>
          ))}
        </ul>
      </Container>
    </nav>
  );
}
