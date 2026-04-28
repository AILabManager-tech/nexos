'use client';

// Section: S-020 | contact.MapsEmbed | i18n: contact.maps
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { useConsent } from '@/lib/cookieConsent';
import { useState } from 'react';
import { MapPin } from 'lucide-react';
import { getClientConfig } from '@/lib/clientConfig';

export function MapsEmbed() {
  const t = useTranslations('contact.maps');
  const { isMarketingAllowed, saveConsent, isAnalyticsAllowed } = useConsent();
  const [showFallback, setShowFallback] = useState(false);
  const config = getClientConfig();

  const mapQuery = `${config.adresseLigne}, ${config.ville} ${config.codePostal}`;
  const embedUrl = `https://maps.google.com/maps?q=${encodeURIComponent(
    mapQuery
  )}&output=embed`;

  const handleLoad = () => {
    saveConsent({ analytics: isAnalyticsAllowed, marketing: true });
  };

  return (
    <section id="maps" className="bg-background py-12 sm:py-16" aria-labelledby="maps-title">
      <Container>
        <div className="max-w-3xl space-y-3 mb-8">
          <h2 id="maps-title" className="font-heading font-bold text-3xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>

        {isMarketingAllowed ? (
          <div className="aspect-[16/9] rounded-lg overflow-hidden border border-border bg-surface">
            <iframe
              title={t('imageAlt', { ville: config.ville, city: config.city })}
              src={embedUrl}
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              className="w-full h-full"
            />
          </div>
        ) : (
          <div className="rounded-lg border border-info/40 bg-info/5 p-6 sm:p-8 space-y-4">
            <div className="flex items-start gap-3">
              <MapPin size={28} className="text-info shrink-0" aria-hidden="true" />
              <div>
                <h3 className="font-heading font-bold text-xl text-text">
                  {t('placeholderTitle')}
                </h3>
                <p className="text-text-muted mt-2 text-base">
                  {t('placeholderBody')}
                </p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 pt-2">
              <button
                type="button"
                onClick={handleLoad}
                className="inline-flex items-center justify-center gap-2 h-12 px-6 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                {t('ctaLoad')}
              </button>
              <button
                type="button"
                onClick={() => setShowFallback(true)}
                className="inline-flex items-center justify-center h-12 px-6 rounded font-semibold border border-border bg-surface text-text hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
              >
                {t('ctaCancel')}
              </button>
            </div>
            <p className="text-small text-text-muted">{t('consentNote')}</p>
            {showFallback && (
              <div className="rounded border border-border bg-surface p-4 mt-3">
                <h4 className="font-semibold text-text">{t('fallbackTitle')}</h4>
                <p className="text-base text-text-muted mt-1">
                  {t('fallbackBody', {
                    adresseLigne: config.adresseLigne,
                    ville: config.ville,
                    codePostal: config.codePostal,
                  })}
                </p>
              </div>
            )}
          </div>
        )}
      </Container>
    </section>
  );
}
