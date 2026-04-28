// Section: S-004 | home.SocialProofVoisinage | i18n: home.socialProof
import { useTranslations, useLocale } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Card } from '@/components/ui/Card';
import { ArrowRight, Quote } from 'lucide-react';
import { getTemoignages } from '@/lib/temoignages';
import { getClientConfig } from '@/lib/clientConfig';
import type { Locale } from '@/i18n/routing';

export function SocialProofVoisinage() {
  const t = useTranslations('home.socialProof');
  const locale = useLocale() as Locale;
  const { ville, city } = getClientConfig();
  const temoignages = getTemoignages();

  return (
    <section className="bg-surface py-12 sm:py-16 lg:py-20" aria-labelledby="social-title">
      <Container>
        <div className="max-w-3xl space-y-3">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h2 id="social-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle', { ville, city })}</p>
        </div>

        <ul className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {temoignages.map((item) => (
            <li key={item.id}>
              <Card className="h-full flex flex-col gap-4">
                <Quote size={28} aria-hidden="true" className="text-accent-strong" />
                <blockquote className="text-base text-text italic">
                  « {item.quote[locale]} »
                </blockquote>
                <footer className="mt-auto pt-3 border-t border-border">
                  <p className="font-semibold text-text">{item.name}</p>
                  <p className="text-small text-text-muted">{item.role[locale]}</p>
                </footer>
              </Card>
            </li>
          ))}
        </ul>

        <p className="mt-6 text-small text-text-muted">{t('consentNote')}</p>

        <div className="mt-10 rounded-lg bg-background-alt p-6 sm:p-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border border-border">
          <p className="font-semibold text-lg text-text">{t('ctaReminder')}</p>
          <Link
            href="/promotions"
            className="inline-flex items-center justify-center gap-2 h-12 px-5 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
          >
            {t('ctaReminderAction')}
            <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </Container>
    </section>
  );
}
