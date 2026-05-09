import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { getCategories } from '@/lib/products';

export function HeroProduits() {
  const t = useTranslations('produits.hero');
  const tCat = useTranslations('produits.category.categoryTitles');
  const categories = getCategories();

  return (
    <section
      data-manifest-id="S-009"
      className="bg-background py-12 sm:py-16 lg:py-20"
    >
      <Container>
        <h1 className="font-heading text-h1 text-primary">{t('title')}</h1>
        <p className="mt-4 max-w-prose text-lg text-text">{t('subtitle')}</p>
        <nav aria-label={t('anchorsLabel')} className="mt-6 flex flex-wrap gap-2">
          {categories.map((c) => (
            <a
              key={c.id}
              href={`#${c.id}`}
              className="inline-flex min-h-[40px] items-center rounded-full border border-border-strong bg-surface px-4 py-2 text-sm font-semibold text-primary hover:bg-surface-alt focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
            >
              {tCat(c.id === 'bieres' ? 'biere' : c.id)}
            </a>
          ))}
        </nav>
      </Container>
    </section>
  );
}
