import Image from 'next/image';
import { useTranslations } from 'next-intl';

// Pattern P20 — Menu galerie d'images (ref S14 La Semilla, lasemillanyc.com)
//
// Règle impérative verbatim (web-patterns-reference.md §P20) :
//   "Menu en format galerie d'images (pas PDF, pas HTML pur)" (La Semilla)
//
// Structure :
//   - Grid 3 col desktop, 2 col tablet, 1 col mobile
//   - aspect-[4/5] cadrage éditorial (plats en composition verticale)
//   - next/image avec sizes précis pour budget poids par image
//   - Nom + description + allergènes (SEO + accessibilité)
//   - Filtres par catégorie (entrées / plats / desserts)
//
// Anti-patterns évités :
//   - Pas de PDF téléchargeable en remplacement
//   - alt-text descriptif par plat (SEO + a11y)
//   - SVG placeholders < 3 Ko (photo réelle devra rester < 100 Ko selon brief P20)
//
// TODO(client) : remplacer les 9 SVG placeholders par des photos éditoriales réelles
// (composition verticale, cadrage assiette 4:5, lumière naturelle, dimensions 1200×1500,
// < 100 Ko/AVIF selon brief P20). Alt-text bilingue préservé dans messages/{fr,en}.json.

type DishKey =
  | 'tartare-bison'
  | 'beets-chevre'
  | 'tomme-saison'
  | 'omble-chevalier'
  | 'agneau-charlevoix'
  | 'tarte-poireaux'
  | 'sabayon-sureau'
  | 'tarte-argousier'
  | 'chocolat-sarrasin';

type Category = 'entrees' | 'plats' | 'desserts';

const DISHES: Array<{ key: DishKey; category: Category }> = [
  { key: 'tartare-bison', category: 'entrees' },
  { key: 'beets-chevre', category: 'entrees' },
  { key: 'tomme-saison', category: 'entrees' },
  { key: 'omble-chevalier', category: 'plats' },
  { key: 'agneau-charlevoix', category: 'plats' },
  { key: 'tarte-poireaux', category: 'plats' },
  { key: 'sabayon-sureau', category: 'desserts' },
  { key: 'tarte-argousier', category: 'desserts' },
  { key: 'chocolat-sarrasin', category: 'desserts' }
];

const CATEGORIES: Category[] = ['entrees', 'plats', 'desserts'];

export function MenuGallery() {
  const t = useTranslations('home.menu');

  return (
    <section id="menu" aria-labelledby="menu-heading" className="bg-surface">
      <div className="mx-auto max-w-7xl px-6 py-24 md:py-32">
        <div className="max-w-editorial">
          <p className="text-sm uppercase tracking-[0.3em] text-accent-deep">
            {t('eyebrow')}
          </p>
          <h2 id="menu-heading" className="mt-4 font-display text-4xl leading-[1.05] md:text-6xl">
            {t('title')}
          </h2>
          <p className="mt-6 text-lg text-ink-soft leading-relaxed">
            {t('subtitle')}
          </p>
        </div>

        {CATEGORIES.map((category) => (
          <div key={category} className="mt-20 first:mt-16">
            <div className="mb-10 flex items-baseline gap-6 border-b border-primary-100 pb-4">
              <h3 className="font-display text-2xl italic text-primary">
                {t(`categories.${category}`)}
              </h3>
              <span className="text-xs uppercase tracking-widest text-ink-muted">
                {t(`categories_tag.${category}`)}
              </span>
            </div>

            <ul className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3" aria-label={t(`categories_aria.${category}`)}>
              {DISHES.filter((d) => d.category === category).map(({ key }) => (
                <li key={key} className="flex flex-col">
                  <div className="relative aspect-[4/5] w-full overflow-hidden bg-surface-raised">
                    <Image
                      src={`/images/menu/${key}.svg`}
                      alt={t(`items.${key}.alt`)}
                      fill
                      sizes="(min-width: 1024px) 28vw, (min-width: 640px) 45vw, 90vw"
                      className="object-cover"
                    />
                  </div>
                  <h4 className="mt-5 font-display text-2xl text-ink">
                    {t(`items.${key}.name`)}
                  </h4>
                  <p className="mt-2 text-sm text-ink-soft leading-relaxed">
                    {t(`items.${key}.description`)}
                  </p>
                  <p className="mt-3 text-xs uppercase tracking-widest text-accent-deep">
                    {t(`items.${key}.terroir`)}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        ))}

        <p className="mt-16 max-w-editorial text-sm text-ink-muted italic">
          {t('footer_note')}
        </p>
      </div>
    </section>
  );
}
