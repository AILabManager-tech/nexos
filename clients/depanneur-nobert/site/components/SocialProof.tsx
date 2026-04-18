'use client';

import { Star } from 'lucide-react';

interface Testimonial {
  name: string;
  role: string;
  text: string;
  rating: number;
}

export default function SocialProof() {
  const testimonials: Testimonial[] = [
    {
      name: 'Marie Leduc',
      role: 'Voisine depuis 15 ans',
      text: 'Je viens ici tous les jours. Nobert me connaît par mon nom. C\'est rare de trouver ça encore.',
      rating: 5,
    },
    {
      name: 'Jean-Paul Gagnon',
      role: 'Habitant du quartier',
      text: 'Dépanneur authentique. Pas de vente de jeux vidéo bizarres. Juste ce qu\'il faut pour vivre.',
      rating: 5,
    },
    {
      name: 'Sophie & Marc',
      role: 'Jeune famille',
      text: 'Les kids aiment venir ici après l\'école. Accueil chaleureux. Prix honnêtes. Merci!',
      rating: 5,
    },
  ];

  return (
    <section className="py-24 bg-white">
      <div className="max-w-5xl mx-auto px-6">
        <h2 className="text-4xl md:text-5xl font-black text-amber-900 mb-4">
          Ce que tes voisins disent
        </h2>
        <p className="text-gray-600 mb-12">
          P02 Social proof — avis authentiques de la communauté
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-lg p-8 border-2 border-amber-200"
            >
              <div className="flex gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star
                    key={i}
                    className="w-5 h-5 fill-amber-500 text-amber-500"
                  />
                ))}
              </div>
              <p className="text-gray-800 italic mb-6 font-medium">
                "{testimonial.text}"
              </p>
              <div>
                <p className="font-bold text-amber-900">{testimonial.name}</p>
                <p className="text-sm text-gray-600">{testimonial.role}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Trust indicators */}
        <div className="mt-16 pt-12 border-t-2 border-gray-200">
          <p className="text-center text-gray-600 mb-8">Confiance locales:</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-black text-amber-700">4.9★</div>
              <p className="text-sm text-gray-600 mt-1">Google Reviews</p>
            </div>
            <div>
              <div className="text-3xl font-black text-amber-700">200+</div>
              <p className="text-sm text-gray-600 mt-1">Avis locaux</p>
            </div>
            <div>
              <div className="text-3xl font-black text-amber-700">+50K</div>
              <p className="text-sm text-gray-600 mt-1">Clients réguliers</p>
            </div>
            <div>
              <div className="text-3xl font-black text-amber-700">37</div>
              <p className="text-sm text-gray-600 mt-1">Ans d'histoire</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
