import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';

export function LeMotDuProprio() {
  const t = useTranslations('home.motProprio');
  return (
    <Section data-manifest-id="S-005">
      <Container>
        <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:items-center">
          <div className="flex h-40 w-40 items-center justify-center rounded-full bg-accent text-6xl font-extrabold text-accent-foreground sm:h-60 sm:w-60">
            <span aria-hidden="true">N</span>
          </div>
          <div className="max-w-prose">
            <span className="text-sm font-semibold uppercase tracking-wide text-primary">
              {t('eyebrow')}
            </span>
            <h2 className="mt-2 font-heading text-h2 text-text">
              {t('title')}
            </h2>
            <blockquote className="mt-4 text-lg leading-relaxed text-text">
              <p>{t('body')}</p>
            </blockquote>
            <p className="mt-4 font-semibold italic text-text-muted">
              {t('signature')}
            </p>
          </div>
        </div>
      </Container>
    </Section>
  );
}
