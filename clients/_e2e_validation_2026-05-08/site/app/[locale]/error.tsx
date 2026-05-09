'use client';

import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ reset }: ErrorProps) {
  const t = useTranslations('common.errors');
  return (
    <Container className="py-20 text-center">
      <h1 className="font-heading text-h1 text-primary">{t('errorTitle')}</h1>
      <p className="mt-4 text-text-muted">{t('errorDescription')}</p>
      <button
        type="button"
        onClick={reset}
        className="mt-6 inline-flex min-h-[48px] items-center rounded bg-primary px-6 py-3 text-primary-foreground hover:bg-primary-hover focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
      >
        {t('errorCta')}
      </button>
    </Container>
  );
}
