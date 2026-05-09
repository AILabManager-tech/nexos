import {
  Beer,
  Cookie,
  GlassWater,
  Snowflake,
  Ticket,
  Wrench,
  type LucideIcon,
} from 'lucide-react';
import { useLocale, useTranslations } from 'next-intl';
import { Card } from '@/components/ui/Card';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { getCategories } from '@/lib/products';

const ICONS: Record<string, LucideIcon> = {
  bieres: Beer,
  snacks: Cookie,
  boissons: GlassWater,
  loto: Ticket,
  depannage: Wrench,
  glace: Snowflake,
};

export function CategoriesGrid() {
  const t = useTranslations('produits.categoriesGrid');
  const locale = useLocale();
  const categories = getCategories();

  return (
    <Section alt data-manifest-id="S-010">
      <Container>
        <h2 className="font-heading text-h2 text-text">{t('title')}</h2>
        <p className="mt-2 max-w-prose text-text-muted">{t('subtitle')}</p>

        <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((c) => {
            const Icon = ICONS[c.id] ?? Cookie;
            return (
              <li key={c.id}>
                <a href={`#${c.id}`} className="block focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2">
                  <Card className="flex flex-col gap-3">
                    <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent text-accent-foreground">
                      <Icon size={24} aria-hidden="true" />
                    </div>
                    <h3 className="font-heading text-xl font-bold text-text">
                      {locale === 'en' ? c.name_en : c.name_fr}
                    </h3>
                    <p className="text-sm text-text-muted">
                      {locale === 'en' ? c.description_en : c.description_fr}
                    </p>
                  </Card>
                </a>
              </li>
            );
          })}
        </ul>
      </Container>
    </Section>
  );
}
