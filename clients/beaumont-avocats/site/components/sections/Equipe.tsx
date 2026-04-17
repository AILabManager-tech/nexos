import { useTranslations } from 'next-intl';
import { RevealOnScroll } from '@/components/atoms/RevealOnScroll';

// Section Équipe — 4 biographies avec "photos" noir et blanc éditoriales.
// P14 rupture 3 : bios avec photos N&B (pas le "corporate headshot" stock).
// P17 : au scroll, les portraits passent de grayscale à grayscale-0 (mono → couleur),
// combiné avec fade-in. Effet signature qui ne distrait pas du texte (ton juridique préservé).
// Placeholder gradient monochrome jusqu'au shoot photo réel (documenté dans phase-I-report).
export function Equipe() {
  const t = useTranslations('home.equipe');
  const members = ['m1', 'm2', 'm3', 'm4'] as const;

  // Gradient variations pour différencier les placeholders sans être bruyants.
  const placeholderGradients = [
    'bg-[linear-gradient(145deg,#0A0A0A,#2B2B2B_50%,#5A5A5A)]',
    'bg-[linear-gradient(120deg,#2B2B2B,#0A0A0A_60%,#2B2B2B)]',
    'bg-[linear-gradient(165deg,#5A5A5A,#2B2B2B_40%,#0A0A0A)]',
    'bg-[linear-gradient(195deg,#0A0A0A,#5A5A5A_50%,#2B2B2B)]'
  ];

  return (
    <section id="equipe" className="bg-surface-alt border-b border-primary-100 py-20 md:py-28">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.18em] text-ink-muted font-medium">
            {t('eyebrow')}
          </p>
          <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
            {t('title')}
          </h2>
          <p className="mt-6 text-lg text-ink-soft leading-relaxed max-w-prose">{t('intro')}</p>
        </div>

        <ul className="mt-16 grid gap-10 md:grid-cols-2 lg:grid-cols-4">
          {members.map((m, idx) => (
            <li key={m}>
              <RevealOnScroll grayscale delayMs={idx * 120} threshold={0.25}>
                <figure>
                  <div
                    role="img"
                    aria-label={t(`members.${m}.image_alt`)}
                    className={`relative aspect-[3/4] w-full overflow-hidden ${placeholderGradients[idx % placeholderGradients.length]}`}
                  >
                    {/* Vignette texturale — placeholder jusqu'au shoot photo du cabinet. */}
                    <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_40%,rgba(255,255,255,0.08),transparent_60%)]" />
                    <div className="absolute inset-0 bg-[linear-gradient(180deg,transparent_60%,rgba(0,0,0,0.35))]" />
                  </div>
                  <figcaption className="mt-4">
                    <p className="font-display text-xl text-ink font-bold leading-tight">
                      {t(`members.${m}.name`)}
                    </p>
                    <p className="mt-1 text-xs uppercase tracking-widest text-primary">
                      {t(`members.${m}.role`)}
                    </p>
                    <p className="mt-3 text-sm text-ink-soft leading-relaxed">
                      {t(`members.${m}.bio`)}
                    </p>
                  </figcaption>
                </figure>
              </RevealOnScroll>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
