import { Clock, MapPin, Phone } from 'lucide-react';
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { getSiteInfo } from '@/lib/site-info';
import { phoneTel } from '@/lib/format';

export function InfosPratiques() {
  const t = useTranslations('home.infosPratiques');
  const info = getSiteInfo();
  const mapUrl = `https://maps.google.com/maps?q=${info.geo.latitude},${info.geo.longitude}&z=15&output=embed`;

  return (
    <Section alt data-manifest-id="S-004">
      <Container>
        <div className="mb-8 flex flex-col gap-2">
          <span className="text-sm font-semibold uppercase tracking-wide text-primary">
            {t('eyebrow')}
          </span>
          <h2 className="font-heading text-h2 text-text">{t('title')}</h2>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          <div className="grid gap-6">
            <div className="flex gap-4">
              <MapPin
                size={24}
                aria-hidden="true"
                className="mt-1 shrink-0 text-primary"
              />
              <div>
                <h3 className="font-heading text-xl font-bold text-text">
                  {t('addressBlockTitle')}
                </h3>
                <p className="mt-1 text-text-muted">
                  {info.streetAddress}, {info.city}, {info.region} {info.postalCode}
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <Clock
                size={24}
                aria-hidden="true"
                className="mt-1 shrink-0 text-primary"
              />
              <div>
                <h3 className="font-heading text-xl font-bold text-text">
                  {t('hoursBlockTitle')}
                </h3>
                <p className="mt-1 text-text-muted">7/7 — 7h à 23h</p>
              </div>
            </div>

            <div className="flex gap-4">
              <Phone
                size={24}
                aria-hidden="true"
                className="mt-1 shrink-0 text-primary"
              />
              <div>
                <h3 className="font-heading text-xl font-bold text-text">
                  {t('phoneBlockTitle')}
                </h3>
                <p className="mt-1 text-text-muted">{t('phoneNote')}</p>
                <a
                  href={phoneTel(info.phone)}
                  className="mt-2 inline-flex min-h-[48px] items-center gap-2 rounded bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground hover:bg-primary-hover focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
                >
                  <Phone size={18} aria-hidden="true" />
                  {t('ctaCall')}
                </a>
              </div>
            </div>
          </div>

          <div className="aspect-[4/3] overflow-hidden rounded-lg border border-border lg:aspect-[16/10]">
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
