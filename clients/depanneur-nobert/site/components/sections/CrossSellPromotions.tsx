// Section: S-017 | produits.CrossSellPromotions | i18n: produits.crossSell
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { ArrowRight } from 'lucide-react';

export function CrossSellPromotions() {
  const t = useTranslations('produits.crossSell');
  return (
    <section className="bg-primary-subtle py-12 sm:py-16" aria-labelledby="cross-sell-promo-title">
      <Container>
        <div className="rounded-lg bg-surface border border-border p-6 sm:p-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h2 id="cross-sell-promo-title" className="font-heading font-bold text-2xl text-text">
              {t('title')}
            </h2>
            <p className="text-text-muted mt-2">{t('subtitle')}</p>
          </div>
          <Link
            href="/promotions"
            className="inline-flex items-center justify-center gap-2 h-12 px-6 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
          >
            {t('ctaPromotions')}
            <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </Container>
    </section>
  );
}
