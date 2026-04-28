// Section: S-003 | home.CategoriesProduits | i18n: home.categories
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Beer, Cookie, Ticket, ShoppingBasket, ArrowRight } from 'lucide-react';

const CATEGORIES = [
  { key: 'bieres' as const, Icon: Beer, anchor: 'bieres' },
  { key: 'snacks' as const, Icon: Cookie, anchor: 'snacks' },
  { key: 'lotto' as const, Icon: Ticket, anchor: 'lotto' },
  { key: 'essentiels' as const, Icon: ShoppingBasket, anchor: 'essentiels' },
];

export function CategoriesProduits() {
  const t = useTranslations('home.categories');

  return (
    <section className="bg-background py-12 sm:py-16 lg:py-20" aria-labelledby="cat-title">
      <Container>
        <div className="max-w-3xl space-y-3">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h2 id="cat-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>

        <ul className="mt-10 grid gap-4 grid-cols-2 lg:grid-cols-4">
          {CATEGORIES.map(({ key, Icon, anchor }) => (
            <li key={key}>
              <Link
                href={{ pathname: '/produits', hash: anchor }}
                className="group h-full flex flex-col items-start gap-3 rounded-lg border border-border bg-surface p-5 hover:bg-primary-subtle hover:border-primary transition-colors focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
              >
                <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-accent text-accent-foreground">
                  <Icon size={22} aria-label={t(`items.${key}.iconAlt`)} />
                </span>
                <h3 className="font-heading font-bold text-lg text-text">
                  {t(`items.${key}.title`)}
                </h3>
                <p className="text-small text-text-muted">
                  {t(`items.${key}.description`)}
                </p>
                <span className="mt-auto inline-flex items-center gap-1 text-primary font-semibold text-small group-hover:underline">
                  {t(`items.${key}.cta`)}
                  <ArrowRight size={14} aria-hidden="true" />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  );
}
