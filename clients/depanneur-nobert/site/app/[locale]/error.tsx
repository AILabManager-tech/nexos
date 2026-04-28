'use client';

import { useTranslations } from 'next-intl';
import { useEffect } from 'react';
import { Container } from '@/components/ui/Container';
import { getClientConfig } from '@/lib/clientConfig';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorBoundary({ error, reset }: ErrorProps) {
  const t = useTranslations('common.errors');
  const { telephone } = getClientConfig();

  useEffect(() => {
    console.error('[error.tsx]', error.message, error.digest);
  }, [error]);

  return (
    <section className="bg-background py-20 sm:py-28" aria-labelledby="err-title">
      <Container className="max-w-2xl text-center space-y-6">
        <h1 id="err-title" className="font-heading font-bold text-4xl text-text">
          {t('genericTitle')}
        </h1>
        <p className="text-lg text-text-muted">{t('genericBody', { telephone })}</p>
        <button
          type="button"
          onClick={reset}
          className="inline-flex h-12 items-center justify-center px-6 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
        >
          {t('genericCta')}
        </button>
      </Container>
    </section>
  );
}
