// Section: S-022 | contact.ContactNoteRPP | i18n: contact.rpp
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { ShieldCheck, ArrowRight } from 'lucide-react';
import { getClientConfig } from '@/lib/clientConfig';

export function ContactNoteRPP() {
  const t = useTranslations('contact.rpp');
  const { rppEmail } = getClientConfig();

  return (
    <section id="rpp" className="bg-info/5 py-12 sm:py-16" aria-labelledby="rpp-title">
      <Container>
        <div className="rounded-lg border border-info/40 bg-surface p-6 sm:p-10 max-w-3xl space-y-4">
          <div className="flex items-start gap-3">
            <ShieldCheck size={28} className="text-info shrink-0" aria-hidden="true" />
            <div>
              <h2 id="rpp-title" className="font-heading font-bold text-2xl text-text">
                {t('title')}
              </h2>
              <p className="mt-2 text-base text-text">{t('body')}</p>
            </div>
          </div>
          <dl className="space-y-2 text-base text-text">
            <div>
              <dt className="inline font-semibold">{t('rppName')} — </dt>
              <dd className="inline text-text-muted">{t('rppRole')}</dd>
            </div>
            <div>
              <dt className="sr-only">RPP email</dt>
              <dd>
                <a
                  href={`mailto:${rppEmail}`}
                  className="text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
                >
                  {t('rppEmail', { rppEmail })}
                </a>
              </dd>
            </div>
          </dl>
          <p className="text-small text-text-muted">{t('incidentNote', { rppEmail })}</p>
          <Link
            href="/politique-confidentialite"
            className="inline-flex items-center gap-2 text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
          >
            {t('linkPrivacy')}
            <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </Container>
    </section>
  );
}
