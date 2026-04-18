'use client';

export default function LocationPages() {
  const locations = [
    {
      name: 'Nobert - Plateau Mont-Royal',
      address: '4155 avenue Mont-Royal Est, Montréal QC H1X 3X2',
      phone: '(514) 555-0101',
      hours: '6h-24h',
      nearby: 'Métro Mont-Royal • Parc Lafontaine',
    },
    {
      name: 'Nobert - Griffintown',
      address: '1245 rue Notre-Dame Ouest, Montréal QC H3C 1K4',
      phone: '(514) 555-0102',
      hours: '7h-23h',
      nearby: 'Métro Lionel-Groulx • Canal Lachine',
    },
    {
      name: 'Nobert - Rosemont-La Petite-Patrie',
      address: '5678 rue Beaubien Est, Montréal QC H1T 2X4',
      phone: '(514) 555-0103',
      hours: '6h-24h',
      nearby: 'Métro Beaubien • Parc Maisonneuve',
    },
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-white to-amber-50">
      <div className="max-w-5xl mx-auto px-6">
        <h2 className="text-4xl md:text-5xl font-black text-amber-900 mb-4">
          Nos emplacements
        </h2>
        <p className="text-gray-600 mb-12">
          P11 Page par localisation — dépanneur + [ville] (SEO optimisé)
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {locations.map((loc, idx) => (
            <div
              key={idx}
              className="bg-white rounded-lg p-6 border-2 border-amber-200 hover:shadow-lg transition"
            >
              <h3 className="text-xl font-black text-amber-900 mb-4">
                {loc.name}
              </h3>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="font-bold text-amber-700">Adresse</p>
                  <p className="text-gray-700">{loc.address}</p>
                </div>
                <div>
                  <p className="font-bold text-amber-700">Téléphone</p>
                  <a href={`tel:${loc.phone}`} className="text-blue-600 hover:underline">
                    {loc.phone}
                  </a>
                </div>
                <div>
                  <p className="font-bold text-amber-700">Heures</p>
                  <p className="text-gray-700">{loc.hours}</p>
                </div>
                <div>
                  <p className="font-bold text-amber-700">À proximité</p>
                  <p className="text-gray-700">{loc.nearby}</p>
                </div>
              </div>
              <button className="w-full mt-4 px-4 py-2 bg-amber-700 text-white font-bold rounded-lg hover:bg-amber-800 transition text-sm">
                Voir sur Google Maps
              </button>
            </div>
          ))}
        </div>

        {/* Schema.org LocalBusiness structured data for SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'LocalBusiness',
              name: 'Dépanneur Nobert',
              image: 'https://depanneur-nobert.local/og-image.png',
              description: 'Commerce de proximité authentique — provisions, snacks, loterie.',
              url: 'https://depanneur-nobert.local',
              telephone: '(514) 555-0101',
              areaServed: ['Plateau Mont-Royal', 'Griffintown', 'Rosemont'],
              priceRange: '$',
              aggregateRating: {
                '@type': 'AggregateRating',
                ratingValue: '4.9',
                reviewCount: '200',
              },
            }),
          }}
        />
      </div>
    </section>
  );
}
