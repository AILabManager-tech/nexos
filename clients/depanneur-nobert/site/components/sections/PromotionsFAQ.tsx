// Section: S-011 | promotions.PromotionsFAQ | i18n: promotions.faq
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { getClientConfig } from '@/lib/clientConfig';
import { jsonLdScriptProps, buildFaqSchema } from '@/lib/jsonld';

const ITEM_KEYS = ['duree', 'retrait', 'livraison'] as const;

export function PromotionsFAQ() {
  const t = useTranslations('promotions.faq');
  const { telephone } = getClientConfig();

  const faqItems = ITEM_KEYS.map((k) => ({
    question: t(`items.${k}.question`),
    answer: t(`items.${k}.answer`, { telephone }),
  }));

  return (
    <section className="bg-background py-12 sm:py-16" aria-labelledby="promo-faq-title">
      <Container>
        <div className="max-w-3xl space-y-8">
          <div className="space-y-2">
            <h2 id="promo-faq-title" className="font-heading font-bold text-3xl text-text">
              {t('title')}
            </h2>
            <p className="text-lg text-text-muted">{t('subtitle')}</p>
          </div>
          <ul className="space-y-4">
            {faqItems.map((item, idx) => (
              <li key={idx}>
                <details className="group rounded-lg border border-border bg-surface p-5 open:shadow-card-hover">
                  <summary className="flex cursor-pointer items-center justify-between gap-4 font-semibold text-lg text-text focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded">
                    {item.question}
                    <span aria-hidden="true" className="text-primary text-2xl group-open:rotate-45 transition-transform">
                      +
                    </span>
                  </summary>
                  <p className="mt-3 text-base text-text-muted">{item.answer}</p>
                </details>
              </li>
            ))}
          </ul>
        </div>
        <script {...jsonLdScriptProps(buildFaqSchema(faqItems))} />
      </Container>
    </section>
  );
}
