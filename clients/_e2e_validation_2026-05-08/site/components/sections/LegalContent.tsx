import type { ReactNode } from 'react';
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { getSiteInfo } from '@/lib/site-info';

interface LegalContentProps {
  title: string;
  intro: string;
  lastUpdated: string;
  children: ReactNode;
}

export function LegalContent({
  title,
  intro,
  lastUpdated,
  children,
}: LegalContentProps) {
  const t = useTranslations('legal.content');
  const info = getSiteInfo();

  return (
    <Section data-manifest-id="S-017" id="top">
      <Container className="max-w-3xl">
        <h1 className="font-heading text-h1 text-primary">{title}</h1>
        <p className="mt-2 text-sm text-text-muted">
          {t('lastUpdatedLabel', { date: lastUpdated })}
        </p>
        <p className="mt-4 max-w-prose text-text">{intro}</p>

        <article className="prose mt-6 max-w-prose text-text [&_h2]:font-heading [&_h2]:text-2xl [&_h2]:font-bold [&_h2]:mt-8 [&_h2]:mb-3 [&_h3]:font-heading [&_h3]:text-xl [&_h3]:mt-6 [&_h3]:mb-2 [&_p]:my-3 [&_ul]:list-disc [&_ul]:pl-6 [&_ul]:my-3 [&_li]:my-1">
          {children}
        </article>

        <p className="mt-8 text-sm text-text-muted">
          {t('contactRppPrompt', { rppEmail: info.rppEmail })}
        </p>
        <a
          href="#top"
          className="mt-4 inline-block text-sm text-primary underline"
        >
          {t('backToTopLabel')}
        </a>
      </Container>
    </Section>
  );
}
