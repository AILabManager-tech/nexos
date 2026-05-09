import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { HeroProduits } from '@/components/sections/HeroProduits';
import { CategoriesGrid } from '@/components/sections/CategoriesGrid';
import { CategorySection } from '@/components/sections/CategorySection';
import { getCategories } from '@/lib/products';
import { buildMetadata } from '@/lib/seo';
import type { Locale } from '@/i18n/routing';

interface PageProps {
  params: Promise<{ locale: Locale }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'produits.meta' });
  return buildMetadata({
    page: 'produits',
    locale,
    title: t('title'),
    description: t('description'),
    pathname: locale === 'fr' ? '/produits' : '/en/products',
  });
}

export default async function ProduitsPage({ params }: PageProps) {
  const { locale } = await params;
  setRequestLocale(locale);
  const categories = getCategories();
  return (
    <>
      <HeroProduits />
      <CategoriesGrid />
      {categories.map((cat, idx) => (
        <CategorySection key={cat.id} category={cat} alt={idx % 2 === 0} />
      ))}
    </>
  );
}
