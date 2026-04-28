'use client';

// Section: S-007 | home.NewsletterCTA | i18n: home.newsletter
//
// Loi 25 art. 8 — avis de collecte au point d'inscription. À proximité du
// bouton d'envoi, on affiche :
//   - la finalité de la collecte (purpose) : envoi de la circulaire ;
//   - les renseignements personnels recueillis (adresse courriel) ;
//   - un lien vers la politique de confidentialité (/politique-confidentialite).
import { useTranslations, useLocale } from 'next-intl';
import { useState, type FormEvent } from 'react';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Input } from '@/components/ui/Input';
import { Checkbox } from '@/components/ui/Checkbox';
import { CheckCircle2, AlertCircle } from 'lucide-react';
import { getClientConfig } from '@/lib/clientConfig';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export function NewsletterCTA() {
  const t = useTranslations('home.newsletter');
  const tForms = useTranslations('common.forms');
  const locale = useLocale();
  const { email: contactEmail } = getClientConfig();

  const [email, setEmail] = useState('');
  const [consent, setConsent] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; consent?: string }>({});
  const [status, setStatus] = useState<Status>('idle');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextErrors: typeof errors = {};
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      nextErrors.email = tForms('invalidEmail');
    }
    if (!consent) {
      nextErrors.consent = tForms('consentRequired');
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setStatus('submitting');
    try {
      const formData = new FormData(event.currentTarget);
      const response = await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          consent: true,
          honeypot: formData.get('website') ?? '',
          locale,
        }),
      });
      if (!response.ok) {
        setStatus('error');
        return;
      }
      setStatus('success');
      setEmail('');
      setConsent(false);
    } catch {
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <section className="bg-primary-subtle py-12 sm:py-16" aria-labelledby="newsletter-title">
        <Container>
          <div role="status" className="rounded-lg border border-success bg-success/10 p-6 max-w-2xl">
            <div className="flex items-start gap-3">
              <CheckCircle2 size={24} className="text-success shrink-0 mt-1" aria-hidden="true" />
              <div>
                <h2 id="newsletter-title" className="font-heading font-bold text-xl text-text">
                  {t('successTitle')}
                </h2>
                <p className="mt-2 text-base text-text">{t('successMessage')}</p>
              </div>
            </div>
          </div>
        </Container>
      </section>
    );
  }

  return (
    <section className="bg-primary-subtle py-12 sm:py-16 lg:py-20" aria-labelledby="newsletter-title">
      <Container>
        <div className="grid gap-8 lg:grid-cols-2 items-start">
          <div className="space-y-3 max-w-xl">
            <p className="text-small uppercase tracking-wider text-primary font-semibold">
              {t('eyebrow')}
            </p>
            <h2 id="newsletter-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
              {t('title')}
            </h2>
            <p className="text-lg text-text">{t('subtitle')}</p>
          </div>
          <form
            noValidate
            onSubmit={handleSubmit}
            className="bg-surface rounded-lg border border-border p-6 space-y-4"
          >
            <Input
              label={t('labelEmail')}
              type="email"
              name="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.currentTarget.value)}
              placeholder={t('placeholderEmail')}
              error={errors.email}
            />
            <div hidden aria-hidden="true">
              <label>
                {tForms('honeypotLabel')}
                <input
                  type="text"
                  name="website"
                  tabIndex={-1}
                  autoComplete="off"
                  defaultValue=""
                />
              </label>
            </div>
            <Checkbox
              label={t('consentLabel')}
              required
              name="consent"
              checked={consent}
              onChange={(e) => setConsent(e.currentTarget.checked)}
              description={t('consentNote')}
              error={errors.consent}
            />
            <p className="text-small text-text-muted">
              <Link
                href="/politique-confidentialite"
                className="text-primary font-semibold underline hover:no-underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
              >
                {tForms('linkPrivacy')}
              </Link>
            </p>
            <button
              type="submit"
              disabled={status === 'submitting'}
              className="inline-flex h-12 w-full sm:w-auto items-center justify-center gap-2 px-7 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {status === 'submitting' ? tForms('submitting') : t('ctaSubscribe')}
            </button>
            {status === 'error' && (
              <p role="alert" className="flex items-start gap-2 text-small text-error">
                <AlertCircle size={16} aria-hidden="true" className="mt-0.5" />
                {t('errorMessage', { email: contactEmail })}
              </p>
            )}
          </form>
        </div>
      </Container>
    </section>
  );
}
