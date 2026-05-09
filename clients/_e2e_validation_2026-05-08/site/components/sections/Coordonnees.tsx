import { Mail, MapPin, Phone } from 'lucide-react';
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { phoneTel } from '@/lib/format';
import { getSiteInfo } from '@/lib/site-info';

export function Coordonnees() {
  const t = useTranslations('contact.coordonnees');
  const info = getSiteInfo();
  const mapUrl = `https://maps.google.com/maps?q=${info.geo.latitude},${info.geo.longitude}&z=15&output=embed`;

  return (
    <Section alt data-manifest-id="S-013">
      <Container>
        <h2 className="font-heading text-h2 text-text">{t('title')}</h2>

        <div className="mt-6 grid gap-8 lg:grid-cols-2">
          <dl className="grid gap-6">
            <div className="flex gap-4">
              <MapPin size={24} aria-hidden="true" className="mt-1 shrink-0 text-primary" />
              <div>
                <dt className="text-sm font-semibold uppercase tracking-wide text-text">
                  {t('addressLabel')}
                </dt>
                <dd className="mt-1 whitespace-pre-line text-text-muted">
                  {info.streetAddress}
                  {'\n'}
                  {info.city}, {info.region} {info.postalCode}
                </dd>
              </div>
            </div>

            <div className="flex gap-4">
              <Phone size={24} aria-hidden="true" className="mt-1 shrink-0 text-primary" />
              <div>
                <dt className="text-sm font-semibold uppercase tracking-wide text-text">
                  {t('phoneLabel')}
                </dt>
                <dd className="mt-1">
                  <a
                    href={phoneTel(info.phone)}
                    className="text-primary hover:underline"
                  >
                    {info.phone}
                  </a>
                </dd>
              </div>
            </div>

            <div className="flex gap-4">
              <Mail size={24} aria-hidden="true" className="mt-1 shrink-0 text-primary" />
              <div>
                <dt className="text-sm font-semibold uppercase tracking-wide text-text">
                  {t('emailLabel')}
                </dt>
                <dd className="mt-1">
                  <a
                    href={`mailto:${info.email}`}
                    className="text-primary hover:underline"
                  >
                    {info.email}
                  </a>
                </dd>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 pt-2">
              <a
                href={phoneTel(info.phone)}
                className="inline-flex min-h-[48px] items-center gap-2 rounded bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground hover:bg-primary-hover focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                <Phone size={18} aria-hidden="true" />
                {t('ctaCall')}
              </a>
              <a
                href={`mailto:${info.email}`}
                className="inline-flex min-h-[48px] items-center gap-2 rounded border border-border-strong px-5 py-3 text-sm font-semibold text-primary hover:bg-surface-alt focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                <Mail size={18} aria-hidden="true" />
                {t('ctaEmail')}
              </a>
            </div>
          </dl>

          <div className="aspect-[4/3] overflow-hidden rounded-lg border border-border lg:aspect-auto">
            <iframe
              src={mapUrl}
              title={t('mapTitle')}
              loading="lazy"
              referrerPolicy="strict-origin-when-cross-origin"
              className="h-full w-full"
            />
          </div>
        </div>
      </Container>
    </Section>
  );
}
