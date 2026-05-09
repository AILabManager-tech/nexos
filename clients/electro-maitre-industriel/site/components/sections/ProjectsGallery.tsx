import Image from 'next/image';
import { useTranslations } from 'next-intl';

// Pattern P06 — Grayscale→Color reveal (ref S27 Puckett Electric, puckettelectric.com)
//
// Règles implémentation :
//   - `filter: grayscale(100%)` par défaut (visuel industriel cohérent avec palette sombre).
//   - `transition: filter 400ms ease-out` (< 500 ms cf. anti-pattern brief).
//   - `group-hover:grayscale-0` ET `group-focus-within:grayscale-0` (a11y clavier).
//   - `prefers-reduced-motion` : transitions forcées ~0 ms dans globals.css ; l'état se toggle
//     instantanément sans animation — pas de suppression d'état (visuel reste fonctionnel).
//   - Overlay accent or (#D4AF37) sur hover pour micro-détail premium (P12 signature couleur).
//
// TODO(client) : les images sont des placeholders SVG. Remplacer par des photos de chantiers réels
// (installation tableau, automate Allen-Bradley, maintenance moteur, etc.), dimensions 800×600,
// AVIF/WebP, < 250 Ko chacune. Alt descriptifs impératifs (pas "photo de projet").

type ProjectKey = 'manufacturing' | 'food-plant' | 'datacenter' | 'warehouse' | 'switchgear' | 'automation';
const PROJECT_KEYS: ProjectKey[] = [
  'manufacturing',
  'food-plant',
  'datacenter',
  'warehouse',
  'switchgear',
  'automation'
];

/**
 * Galerie 6 projets — grayscale par défaut, révélés en couleur au hover/focus (Pattern P06).
 * Transitions CSS pures (`filter` + `transition` 400 ms), `prefers-reduced-motion` géré dans
 * `globals.css`. Overlay accent or 5 % au hover = micro-signature P12.
 *
 * @remarks Limitation actuelle : chaque carte pointe vers `#project-<key>` mais aucune ancre
 * cible n'existe encore (cf. ph5-qa-report.md §6.1, WCAG 2.4.1, 6 erreurs pa11y).
 */
export function ProjectsGallery() {
  const t = useTranslations('home.projects');

  return (
    <section id="projects" aria-labelledby="projects-heading" className="bg-surface">
      <div className="mx-auto max-w-7xl px-6 py-24">
        <div className="max-w-2xl">
          <p className="text-sm uppercase tracking-[0.3em] text-accent">
            {t('eyebrow')}
          </p>
          <h2 id="projects-heading" className="mt-4 text-3xl md:text-5xl">
            {t('title')}
          </h2>
          <p className="mt-4 text-ink-soft">{t('subtitle')}</p>
        </div>

        <ul className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3" aria-label={t('aria_label')}>
          {PROJECT_KEYS.map((key) => (
            <li
              key={key}
              className="group relative block overflow-hidden border border-primary-800 bg-surface-alt focus-within:outline focus-within:outline-2 focus-within:outline-accent"
            >
              <a
                href={`#project-${key}`}
                className="block focus:outline-none"
                aria-label={t(`items.${key}.alt`)}
              >
                <div className="relative aspect-[4/3] w-full overflow-hidden">
                  <Image
                    src={`/images/projects/${key}.svg`}
                    alt={t(`items.${key}.alt`)}
                    fill
                    sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                    className="object-cover grayscale transition-[filter] duration-[400ms] ease-out group-hover:grayscale-0 group-focus-within:grayscale-0"
                  />
                  {/* Overlay accent au hover : micro-signature couleur (P12) */}
                  <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0 bg-accent/0 transition-colors duration-[400ms] group-hover:bg-accent/5 group-focus-within:bg-accent/5"
                  />
                </div>
                <div className="border-t border-primary-800 p-5">
                  <p className="text-xs uppercase tracking-widest text-accent">
                    {t(`items.${key}.sector`)}
                  </p>
                  <p className="mt-2 font-heading text-lg text-ink">
                    {t(`items.${key}.title`)}
                  </p>
                  <p className="mt-1 text-sm text-ink-muted">
                    {t(`items.${key}.summary`)}
                  </p>
                </div>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
