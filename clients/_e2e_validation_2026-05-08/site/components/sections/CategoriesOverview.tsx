import {
  ArrowRight,
  Beer,
  Cookie,
  GlassWater,
  Snowflake,
  Ticket,
  Wrench,
  type LucideIcon,
} from 'lucide-react';
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Card } from '@/components/ui/Card';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';

const ITEMS: { key: string; icon: LucideIcon }[] = [
  { key: 'biere', icon: Beer },
  { key: 'snacks', icon: Cookie },
  { key: 'boissons', icon: GlassWater },
  { key: 'loto', icon: Ticket },
  { key: 'depannage', icon: Wrench },
  { key: 'glace', icon: Snowflake },
];

export function CategoriesOverview() {
  const t = useTranslations('home.categories');
  return (
    <Section data-manifest-id="S-003">
      <Container>
        <div className="mb-8 flex flex-col gap-2">
          <span className="text-sm font-semibold uppercase tracking-wide text-primary">
            {t('eyebrow')}
          </span>
          <h2 className="font-heading text-h2 text-text">{t('title')}</h2>
          <p className="max-w-prose text-text-muted">{t('subtitle')}</p>
        </div>

        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {ITEMS.map(({ key, icon: Icon }) => (
            <li key={key}>
              <Card className="flex flex-col gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent text-accent-foreground">
                  <Icon size={24} aria-hidden="true" />
                </div>
                <h3 className="font-heading text-xl font-bold text-text">
                  {t(`items.${key}.title`)}
                </h3>
                <p className="text-sm text-text-muted">
                  {t(`items.${key}.description`)}
                </p>
              </Card>
            </li>
          ))}
        </ul>

        <div className="mt-8 flex justify-center">
          <Link
            href="/produits"
            className="inline-flex min-h-[48px] items-center gap-2 rounded border border-border-strong px-6 py-3 text-base font-semibold text-primary hover:bg-surface-alt focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
          >
            {t('ctaAllProducts')}
            <ArrowRight size={20} aria-hidden="true" />
          </Link>
        </div>
      </Container>
    </Section>
  );
}
