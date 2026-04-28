'use client';

// Section: S-010 | promotions.PromotionsList | i18n: promotions.list
import { useTranslations, useLocale } from 'next-intl';
import { useMemo, useState } from 'react';
import { Container } from '@/components/ui/Container';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import type { Locale } from '@/i18n/routing';
import type { CategorieProduit, Promotion } from '@/types';

const FILTER_KEYS = ['all', 'bieres', 'snacks', 'essentiels'] as const;
type FilterKey = (typeof FILTER_KEYS)[number];

const FILTER_LABEL: Record<FilterKey, 'filterAll' | 'filterBieres' | 'filterSnacks' | 'filterEssentiels'> = {
  all: 'filterAll',
  bieres: 'filterBieres',
  snacks: 'filterSnacks',
  essentiels: 'filterEssentiels',
};

interface PromotionsListProps {
  promotions: Promotion[];
}

export function PromotionsList({ promotions }: PromotionsListProps) {
  const t = useTranslations('promotions.list');
  const locale = useLocale() as Locale;
  const [filter, setFilter] = useState<FilterKey>('all');

  const filtered = useMemo(() => {
    if (filter === 'all') return promotions;
    return promotions.filter((p) => p.category === (filter as CategorieProduit));
  }, [filter, promotions]);

  const fmtDate = (iso: string) =>
    new Date(iso).toLocaleDateString(locale === 'fr' ? 'fr-CA' : 'en-CA', {
      day: 'numeric',
      month: 'long',
    });

  return (
    <section className="bg-surface py-12 sm:py-16 lg:py-20" aria-labelledby="promo-list-title">
      <Container>
        <div className="max-w-3xl space-y-3 mb-8">
          <h2 id="promo-list-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>

        <div role="group" aria-label={t('filterAriaLabel')} className="flex flex-wrap gap-2 mb-8">
          {FILTER_KEYS.map((key) => {
            const isActive = filter === key;
            return (
              <button
                key={key}
                type="button"
                onClick={() => setFilter(key)}
                aria-pressed={isActive}
                className={`h-11 px-4 rounded-full font-semibold text-small border transition-colors focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary ${
                  isActive
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-surface text-text border-border hover:bg-primary-subtle'
                }`}
              >
                {t(FILTER_LABEL[key])}
              </button>
            );
          })}
        </div>

        {filtered.length === 0 ? (
          <div className="rounded-lg border border-border bg-background-alt p-6">
            <h3 className="font-heading font-bold text-xl text-text">
              {t('emptyState.title')}
            </h3>
            <p className="text-text-muted mt-2">{t('emptyState.subtitle')}</p>
          </div>
        ) : (
          <ul className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((promo) => {
              const validDate = fmtDate(promo.validUntil);
              const savings =
                promo.regularPrice && promo.promoPrice
                  ? (promo.regularPrice - promo.promoPrice).toFixed(2)
                  : null;
              return (
                <li key={promo.id}>
                  <Card className="h-full flex flex-col gap-3">
                    <Badge variant="accent">
                      {t(FILTER_LABEL[promo.category as FilterKey] ?? 'filterAll')}
                    </Badge>
                    <h3 className="font-heading font-bold text-xl text-text">
                      {promo.title[locale]}
                    </h3>
                    {promo.regularPrice && promo.promoPrice && (
                      <div className="space-y-1">
                        <p className="text-text">
                          <span className="text-small text-text-muted">
                            {t('regularPriceLabel')} :
                          </span>{' '}
                          <span className="line-through text-text-muted">
                            {promo.regularPrice.toFixed(2)} $
                          </span>
                        </p>
                        <p>
                          <span className="text-small text-text-muted">
                            {t('promoPriceLabel')} :
                          </span>{' '}
                          <span className="font-bold text-2xl text-primary">
                            {promo.promoPrice.toFixed(2)} $
                          </span>
                        </p>
                        {savings && (
                          <p className="text-small text-success font-semibold">
                            {t('savingsLabel')} {savings} $
                          </p>
                        )}
                      </div>
                    )}
                    <p className="text-small text-text-muted mt-auto">
                      {t('validUntilLabel', { date: validDate })}
                    </p>
                    {promo.limitedStock && (
                      <p className="text-small text-warning font-semibold">
                        {t('limitedStockLabel')}
                      </p>
                    )}
                  </Card>
                </li>
              );
            })}
          </ul>
        )}
      </Container>
    </section>
  );
}
