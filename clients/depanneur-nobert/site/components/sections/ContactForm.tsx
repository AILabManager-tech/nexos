'use client';

// Section: S-021 | contact.ContactForm | i18n: contact.form
//
// Loi 25 art. 8 — avis de collecte au point de collecte (point-of-collection
// notice). La présente section affiche, à proximité du bouton d'envoi :
//   - la finalité de la collecte (purpose) ;
//   - les renseignements personnels recueillis (nom, courriel, téléphone) ;
//   - un lien vers la politique de confidentialité (/politique-confidentialite) ;
//   - l'identification du RPP via la zone <ContactNoteRPP /> adjacente.
import { useTranslations, useLocale } from 'next-intl';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Checkbox } from '@/components/ui/Checkbox';
import { CheckCircle2, AlertCircle } from 'lucide-react';
import { ContactSchema, type ContactPayload } from '@/lib/schemas';
import { getClientConfig } from '@/lib/clientConfig';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export function ContactForm() {
  const t = useTranslations('contact.form');
  const tForms = useTranslations('common.forms');
  const locale = useLocale() as 'fr' | 'en';
  const { telephone, rppEmail } = getClientConfig();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ContactPayload>({
    resolver: zodResolver(ContactSchema),
    defaultValues: {
      consent: undefined as unknown as true,
      locale,
    },
  });

  const [status, setStatus] = useState<Status>('idle');

  const onSubmit = async (data: ContactPayload) => {
    setStatus('submitting');
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
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
    <section className="bg-surface py-12 sm:py-16" aria-labelledby="contact-form-title">
      <Container>
        <div className="grid gap-10 lg:grid-cols-[1fr_2fr]">
          <div className="space-y-3">
            <h2 id="contact-form-title" className="font-heading font-bold text-3xl text-text">
              {t('title')}
            </h2>
            <p className="text-lg text-text-muted">{t('subtitle')}</p>
            <p className="text-small text-text-muted">
              {t('consentNote', { rppEmail })}
            </p>
          </div>
          {status === 'success' ? (
            <div role="status" className="rounded-lg border border-success bg-success/10 p-6">
              <div className="flex items-start gap-3">
                <CheckCircle2 size={24} className="text-success shrink-0 mt-1" aria-hidden="true" />
                <div>
                  <h3 className="font-heading font-bold text-xl text-text">{t('successTitle')}</h3>
                  <p className="mt-2 text-base text-text">{t('successMessage')}</p>
                </div>
              </div>
            </div>
          ) : (
            <form
              noValidate
              onSubmit={handleSubmit(onSubmit)}
              className="space-y-5 bg-background-alt rounded-lg border border-border p-6 sm:p-8"
            >
              <Input
                label={t('labelName')}
                required
                autoComplete="name"
                placeholder={tForms('placeholderName')}
                error={errors.name?.message ? tForms('required') : undefined}
                {...register('name')}
              />
              <Input
                label={t('labelEmail')}
                type="email"
                required
                autoComplete="email"
                placeholder={tForms('placeholderEmail')}
                error={errors.email?.message ? tForms('invalidEmail') : undefined}
                {...register('email')}
              />
              <Input
                label={t('labelPhone')}
                type="tel"
                autoComplete="tel"
                placeholder={tForms('placeholderPhone')}
                error={errors.phone?.message ? tForms('invalidPhone') : undefined}
                {...register('phone')}
              />
              <Textarea
                label={t('labelMessage')}
                required
                placeholder={tForms('placeholderMessage')}
                error={errors.message?.message ? tForms('messageMinLength') : undefined}
                {...register('message')}
              />
              <div hidden aria-hidden="true">
                <label>
                  {tForms('honeypotLabel')}
                  <input
                    type="text"
                    tabIndex={-1}
                    autoComplete="off"
                    {...register('honeypot')}
                  />
                </label>
              </div>
              <Checkbox
                label={t('labelConsent')}
                required
                error={errors.consent?.message ? tForms('consentRequired') : undefined}
                {...register('consent')}
              />
              <p className="text-small text-text-muted">
                {t('consentNote', { rppEmail })}{' '}
                <Link
                  href="/politique-confidentialite"
                  className="text-primary font-semibold underline hover:no-underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
                >
                  {tForms('linkPrivacy')}
                </Link>
              </p>
              <input type="hidden" {...register('locale')} />
              <button
                type="submit"
                disabled={status === 'submitting'}
                className="inline-flex h-14 w-full sm:w-auto items-center justify-center px-7 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {status === 'submitting' ? t('submitting') : t('submit')}
              </button>
              {status === 'error' && (
                <p role="alert" className="flex items-start gap-2 text-small text-error">
                  <AlertCircle size={16} aria-hidden="true" className="mt-0.5" />
                  {t('errorMessage', { telephone })}
                </p>
              )}
            </form>
          )}
        </div>
      </Container>
    </section>
  );
}
