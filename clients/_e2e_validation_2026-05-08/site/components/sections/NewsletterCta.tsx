'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Checkbox } from '@/components/ui/Checkbox';
import { Container } from '@/components/ui/Container';
import { Input } from '@/components/ui/Input';
import { Section } from '@/components/ui/Section';
import { NewsletterSchema, type NewsletterInput } from '@/lib/schemas';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export function NewsletterCta() {
  const t = useTranslations('home.newsletter');
  const tForms = useTranslations('common.forms');
  const tConsent = useTranslations('common.consent');
  const [status, setStatus] = useState<Status>('idle');
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<NewsletterInput>({
    resolver: zodResolver(NewsletterSchema),
    defaultValues: { email: '', consent: undefined as unknown as true, hp: '' },
  });

  const onSubmit = async (data: NewsletterInput) => {
    setStatus('submitting');
    try {
      const res = await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        setStatus('error');
        return;
      }
      setStatus('success');
      reset();
    } catch {
      setStatus('error');
    }
  };

  return (
    <Section alt data-manifest-id="S-006">
      <Container className="max-w-3xl">
        <div className="mb-6 text-center">
          <span className="text-sm font-semibold uppercase tracking-wide text-primary">
            {t('eyebrow')}
          </span>
          <h2 className="mt-2 font-heading text-h2 text-text">{t('title')}</h2>
          <p className="mt-2 text-text-muted">{t('subtitle')}</p>
        </div>

        {status === 'success' ? (
          <p className="rounded border border-success bg-surface p-4 text-center text-success">
            {t('successMessage')}
          </p>
        ) : (
          <form
            onSubmit={handleSubmit(onSubmit)}
            noValidate
            className="flex flex-col gap-4"
          >
            <div className="hidden">
              <label htmlFor="hp-news">{tForms('honeypotLabel')}</label>
              <input
                type="text"
                id="hp-news"
                tabIndex={-1}
                autoComplete="off"
                {...register('hp')}
              />
            </div>

            <div className="flex flex-col gap-2 sm:flex-row">
              <label htmlFor="newsletter-email" className="sr-only">
                {t('emailLabel')}
              </label>
              <Input
                id="newsletter-email"
                type="email"
                placeholder={t('emailPlaceholder')}
                invalid={!!errors.email}
                autoComplete="email"
                {...register('email')}
                className="flex-1"
              />
              <button
                type="submit"
                disabled={status === 'submitting'}
                className="inline-flex min-h-[48px] items-center justify-center gap-2 rounded bg-primary px-6 py-3 text-base font-semibold text-primary-foreground hover:bg-primary-hover disabled:opacity-50 focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                {t('ctaSubscribe')}
              </button>
            </div>
            {errors.email && (
              <p className="text-sm text-error">{tForms('invalidEmail')}</p>
            )}

            <Checkbox
              {...register('consent')}
              invalid={!!errors.consent}
              label={tForms('labelNewsletterConsent')}
              detail={tConsent('newsletterConsentText')}
            />
            {errors.consent && (
              <p className="text-sm text-error">{tForms('consentRequired')}</p>
            )}

            {status === 'error' && (
              <p className="rounded border border-error bg-surface p-3 text-sm text-error">
                {t('errorMessage')}
              </p>
            )}

            <p className="text-xs text-text-muted">{t('consentReminder')}</p>
            {/* Finalité (Loi 25) + lien politique de confidentialité — exigés près du formulaire */}
            <p className="text-xs text-text-muted">
              {t('purposeNotice')}{' '}
              <Link
                href="/politique-confidentialite"
                className="underline hover:text-primary"
              >
                {t('privacyLinkLabel')}
              </Link>
              .
            </p>
          </form>
        )}
      </Container>
    </Section>
  );
}
