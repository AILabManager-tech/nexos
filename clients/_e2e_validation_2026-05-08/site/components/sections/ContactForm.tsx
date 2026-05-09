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
import { Textarea } from '@/components/ui/Textarea';
import { ContactSchema, type ContactInput } from '@/lib/schemas';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export function ContactForm() {
  const t = useTranslations('contact.form');
  const tForms = useTranslations('common.forms');
  const [status, setStatus] = useState<Status>('idle');

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ContactInput>({
    resolver: zodResolver(ContactSchema),
    defaultValues: {
      name: '',
      email: '',
      phone: '',
      message: '',
      consent: undefined as unknown as true,
      hp: '',
    },
  });

  const onSubmit = async (data: ContactInput) => {
    setStatus('submitting');
    try {
      const res = await fetch('/api/contact', {
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
    <Section alt data-manifest-id="S-015">
      <Container className="max-w-3xl">
        <h2 className="font-heading text-h2 text-text">{t('title')}</h2>
        <p className="mt-2 text-text-muted">{t('subtitle')}</p>
        {/* Finalité (Loi 25) + lien politique de confidentialité — exigés près du formulaire */}
        <p className="mt-3 text-sm text-text-muted">
          {t('purposeNotice')}{' '}
          <Link
            href="/politique-confidentialite"
            className="underline hover:text-primary"
          >
            {t('privacyLinkLabel')}
          </Link>
          .
        </p>

        {status === 'success' ? (
          <p className="mt-6 rounded border border-success bg-surface p-4 text-success">
            {t('successMessage')}
          </p>
        ) : (
          <form
            onSubmit={handleSubmit(onSubmit)}
            noValidate
            className="mt-6 grid gap-4"
          >
            <div className="hidden">
              <label htmlFor="hp-contact">{tForms('honeypotLabel')}</label>
              <input
                type="text"
                id="hp-contact"
                tabIndex={-1}
                autoComplete="off"
                {...register('hp')}
              />
            </div>

            <div className="grid gap-2">
              <label htmlFor="contact-name" className="text-sm font-semibold text-text">
                {t('labelName')}
              </label>
              <Input
                id="contact-name"
                autoComplete="name"
                invalid={!!errors.name}
                {...register('name')}
              />
              {errors.name && (
                <p className="text-sm text-error">{tForms('required')}</p>
              )}
            </div>

            <div className="grid gap-2">
              <label htmlFor="contact-email" className="text-sm font-semibold text-text">
                {tForms('labelEmail')}
              </label>
              <Input
                id="contact-email"
                type="email"
                autoComplete="email"
                invalid={!!errors.email}
                {...register('email')}
              />
              {errors.email && (
                <p className="text-sm text-error">{tForms('invalidEmail')}</p>
              )}
            </div>

            <div className="grid gap-2">
              <label htmlFor="contact-phone" className="text-sm font-semibold text-text">
                {tForms('labelPhone')}
              </label>
              <Input
                id="contact-phone"
                type="tel"
                autoComplete="tel"
                placeholder={tForms('placeholderPhone')}
                {...register('phone')}
              />
            </div>

            <div className="grid gap-2">
              <label htmlFor="contact-message" className="text-sm font-semibold text-text">
                {t('labelMessage')}
              </label>
              <Textarea
                id="contact-message"
                rows={5}
                invalid={!!errors.message}
                {...register('message')}
              />
              {errors.message && (
                <p className="text-sm text-error">{tForms('messageTooShort')}</p>
              )}
            </div>

            <Checkbox
              {...register('consent')}
              invalid={!!errors.consent}
              label={t('labelConsent')}
              detail={t('consentDetail')}
            />
            {errors.consent && (
              <p className="text-sm text-error">{tForms('consentRequired')}</p>
            )}

            {status === 'error' && (
              <p className="rounded border border-error bg-surface p-3 text-sm text-error">
                {t('errorMessage')}
              </p>
            )}

            <button
              type="submit"
              disabled={status === 'submitting'}
              className="inline-flex min-h-[48px] items-center justify-center gap-2 rounded bg-primary px-6 py-3 text-base font-semibold text-primary-foreground hover:bg-primary-hover disabled:opacity-50 focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
            >
              {t('ctaSend')}
            </button>
          </form>
        )}
      </Container>
    </Section>
  );
}
