import { ArrowUp } from 'lucide-react';
import Image from 'next/image';
import { useLocale, useTranslations } from 'next-intl';
import { Card } from '@/components/ui/Card';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { formatPrice } from '@/lib/format';
import type { Category } from '@/types/product';

interface CategorySectionProps {
  category: Category;
  alt?: boolean;
}

export function CategorySection({ category, alt }: CategorySectionProps) {
  const t = useTranslations('produits.category');
  const tCat = useTranslations('produits.category');
  const locale = useLocale();

  const title =
    category.id === 'bieres'
      ? tCat('categoryTitles.biere')
      : tCat(`categoryTitles.${category.id}`);
  const intro =
    category.id === 'bieres'
      ? tCat('categoryIntros.biere')
      : tCat(`categoryIntros.${category.id}`);

  return (
    <Section
      alt={alt}
      data-manifest-id="S-011"
      id={category.id}
      aria-labelledby={`cat-${category.id}-title`}
    >
      <Container>
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <h2
              id={`cat-${category.id}-title`}
              className="font-heading text-h2 text-text"
            >
              {title}
            </h2>
            <p className="mt-2 max-w-prose text-text-muted">{intro}</p>
          </div>
          <a
            href="#top"
            className="hidden text-sm text-primary underline sm:inline-flex sm:items-center sm:gap-1"
          >
            <ArrowUp size={16} aria-hidden="true" />
            {t('anchorLabel')}
          </a>
        </div>

        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {category.products.map((p) => {
            const name = locale === 'en' ? p.name_en : p.name_fr;
            const altText = locale === 'en' ? p.alt_en : p.alt_fr;
            return (
              <li key={p.id}>
                <Card className="flex h-full flex-col gap-3">
                  <div className="relative aspect-square overflow-hidden rounded bg-surface-alt">
                    <Image
                      src={p.image}
                      alt={altText}
                      fill
                      sizes="(min-width: 1024px) 33vw, 50vw"
                      className="object-cover"
                    />
                  </div>
                  <h3 className="font-heading text-lg font-bold text-text">
                    {name}
                  </h3>
                  {p.priceIndicative !== undefined && (
                    <p className="text-sm text-text-muted">
                      <span className="block text-xs uppercase tracking-wide">
                        {t('indicativePriceLabel')}
                      </span>
                      <span className="text-base font-semibold text-primary">
                        {formatPrice(p.priceIndicative, locale)}
                      </span>
                    </p>
                  )}
                  {!p.available && (
                    <p className="mt-auto text-xs italic text-error">
                      {t('outOfStockLabel')}
                    </p>
                  )}
                </Card>
              </li>
            );
          })}
        </ul>
      </Container>
    </Section>
  );
}
