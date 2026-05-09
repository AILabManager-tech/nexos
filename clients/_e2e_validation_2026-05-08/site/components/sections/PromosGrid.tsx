import Image from 'next/image';
import { useLocale, useTranslations } from 'next-intl';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { formatDate, formatPrice } from '@/lib/format';
import { getActivePromotions } from '@/lib/promotions';

export function PromosGrid() {
  const t = useTranslations('promotions.grid');
  const locale = useLocale();
  const promos = getActivePromotions();

  if (promos.length === 0) {
    return (
      <Section alt data-manifest-id="S-008">
        <Container className="text-center">
          <h2 className="font-heading text-h2 text-text">{t('emptyTitle')}</h2>
          <p className="mt-3 text-text-muted">{t('emptyMessage')}</p>
        </Container>
      </Section>
    );
  }

  return (
    <Section alt data-manifest-id="S-008">
      <Container>
        <h2 className="mb-8 font-heading text-h2 text-text">{t('title')}</h2>
        <ul className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {promos.map((p) => {
            const title = locale === 'en' ? p.title_en : p.title_fr;
            const alt = locale === 'en' ? p.alt_en : p.alt_fr;
            const savings = p.priceBefore - p.priceAfter;
            return (
              <li key={p.id}>
                <Card className="flex h-full flex-col gap-3">
                  <div className="relative aspect-[4/3] overflow-hidden rounded bg-surface-alt">
                    <Image
                      src={p.image}
                      alt={alt}
                      fill
                      sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                      className="object-cover"
                    />
                    <Badge className="absolute left-3 top-3">
                      {t('savingsLabel', { amount: formatPrice(savings, locale) })}
                    </Badge>
                  </div>
                  <h3 className="font-heading text-xl font-bold text-text">
                    {title}
                  </h3>
                  <div className="flex items-baseline gap-3">
                    <span className="text-sm text-text-muted line-through">
                      {t('previousPriceLabel')} {formatPrice(p.priceBefore, locale)}
                    </span>
                    <span className="text-2xl font-extrabold text-primary">
                      {formatPrice(p.priceAfter, locale)}
                    </span>
                  </div>
                  <div className="mt-auto flex flex-wrap gap-2 text-xs text-text-muted">
                    <span>{t('validityLabel', { dateEnd: formatDate(p.validTo, locale) })}</span>
                    <span aria-hidden="true">·</span>
                    <span>{t('inStoreOnlyLabel')}</span>
                  </div>
                </Card>
              </li>
            );
          })}
        </ul>
      </Container>
    </Section>
  );
}
