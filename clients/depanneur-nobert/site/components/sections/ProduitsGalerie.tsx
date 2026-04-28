// Section: S-015 | produits.ProduitsGalerie | i18n: produits.galerie
import { useTranslations, useLocale } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Card } from '@/components/ui/Card';
import { getProduitsByCategory, getAllCategories } from '@/lib/produits';
import type { CategorieProduit } from '@/types';
import type { Locale } from '@/i18n/routing';

export function ProduitsGalerie() {
  const t = useTranslations('produits.galerie');
  const locale = useLocale() as Locale;

  return (
    <section className="bg-background py-12 sm:py-16 lg:py-20" aria-label={t('sectionsLabel')}>
      <Container className="space-y-16">
        {getAllCategories().map((category) => (
          <CategorySection key={category} category={category} t={t} locale={locale} />
        ))}
      </Container>
    </section>
  );
}

interface CategorySectionProps {
  category: CategorieProduit;
  t: ReturnType<typeof useTranslations>;
  locale: Locale;
}

function CategorySection({ category, t, locale }: CategorySectionProps) {
  const produits = getProduitsByCategory(category);
  const titleId = `cat-${category}`;
  const note = (() => {
    if (category === 'bieres') return t('bieres.note');
    if (category === 'essentiels') return t('essentiels.note');
    return null;
  })();

  return (
    <div id={category} className="scroll-mt-32">
      <header className="space-y-2 mb-6">
        <h2 id={titleId} className="font-heading font-bold text-3xl text-text">
          {t(`${category}.title`)}
        </h2>
        <p className="text-lg text-text-muted">{t(`${category}.subtitle`)}</p>
      </header>
      {produits.length === 0 ? (
        <p className="rounded-lg border border-border bg-surface p-6 text-text-muted">
          {t('askInStore')}
        </p>
      ) : (
        <ul aria-labelledby={titleId} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {produits.map((produit) => (
            <li key={produit.id}>
              <Card className="h-full flex flex-col gap-3">
                <p className="text-small uppercase tracking-wider text-text-muted font-semibold">
                  {t('productCardLabel')}
                </p>
                <h3 className="font-heading font-bold text-xl text-text">
                  {produit.name[locale]}
                </h3>
                {produit.format && (
                  <p className="text-small text-text-muted">{produit.format}</p>
                )}
                {produit.outOfStock && (
                  <p className="text-small text-warning font-semibold">
                    {t('outOfStockLabel')}
                  </p>
                )}
              </Card>
            </li>
          ))}
        </ul>
      )}
      {note && (
        <p className="mt-4 rounded border border-info/30 bg-info/5 p-3 text-small text-text">
          {note}
        </p>
      )}
    </div>
  );
}
