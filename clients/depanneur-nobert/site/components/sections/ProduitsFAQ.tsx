// Section: S-016 | produits.ProduitsFAQ | i18n: produits.faq
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { getClientConfig } from '@/lib/clientConfig';
import { jsonLdScriptProps, buildFaqSchema } from '@/lib/jsonld';

const ITEM_KEYS = ['commandeSpeciale', 'commandeTelephone', 'permisBiere'] as const;

export function ProduitsFAQ() {
  const t = useTranslations('produits.faq');
  const { telephone } = getClientConfig();

  const faqItems = ITEM_KEYS.map((k) => ({
    question: t(`items.${k}.question`),
    answer: t(`items.${k}.answer`, { telephone }),
  }));

  return (
    <section className="bg-surface py-12 sm:py-16" aria-labelledby="prod-faq-title">
      <Container>
        <div className="max-w-3xl space-y-8">
          <div className="space-y-2">
            <h2 id="prod-faq-title" className="font-heading font-bold text-3xl text-text">
              {t('title')}
            </h2>
            <p className="text-lg text-text-muted">{t('subtitle')}</p>
          </div>
          <ul className="space-y-4">
            {faqItems.map((item, idx) => (
              <li key={idx}>
                <details className="group rounded-lg border border-border bg-background-alt p-5 open:shadow-card-hover">
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
