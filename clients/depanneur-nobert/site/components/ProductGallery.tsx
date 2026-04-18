'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  category: string;
  price?: string;
}

export default function ProductGallery() {
  const [activeCategory, setActiveCategory] = useState('provisions');

  const categories: Record<string, Product[]> = {
    provisions: [
      { id: '1', name: 'Épicerie fine', category: 'provisions', price: 'Dès $2.99' },
      { id: '2', name: 'Produits laitiers', category: 'provisions', price: 'Dès $1.99' },
      { id: '3', name: 'Pains et pâtisseries', category: 'provisions', price: 'Frais quotidien' },
      { id: '4', name: 'Fruits et légumes', category: 'provisions', price: 'Saisonnier' },
    ],
    snacks: [
      { id: '5', name: 'Chips et croustilles', category: 'snacks', price: 'Dès $0.99' },
      { id: '6', name: 'Chocolats et bonbons', category: 'snacks', price: 'Dès $1.49' },
      { id: '7', name: 'Breuvages froids', category: 'snacks', price: 'Dès $1.99' },
      { id: '8', name: 'Café et thé', category: 'snacks', price: 'Dès $3.99' },
    ],
    loterie: [
      { id: '9', name: 'Lotto 6/49', category: 'loterie', price: '$3/billet' },
      { id: '10', name: 'Lotto Max', category: 'loterie', price: '$5/billet' },
      { id: '11', name: 'Banco', category: 'loterie', price: '$2/billet' },
      { id: '12', name: 'Scratch & Win', category: 'loterie', price: '$1-10' },
    ],
  };

  const products = categories[activeCategory] || [];

  return (
    <section id="produits" className="py-24 bg-gradient-to-b from-white to-orange-50">
      <div className="max-w-5xl mx-auto px-6">
        <h2 className="text-4xl md:text-5xl font-black text-amber-900 mb-4">
          Notre catalogue
        </h2>
        <p className="text-gray-600 mb-12">
          P20 Menu galerie — explore nos catégories de produits
        </p>

        {/* Category tabs */}
        <div className="flex gap-3 mb-12 overflow-x-auto pb-2">
          {Object.keys(categories).map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-6 py-3 font-bold whitespace-nowrap rounded-lg transition ${
                activeCategory === cat
                  ? 'bg-amber-700 text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
            >
              {cat === 'provisions' && '📦 Provisions'}
              {cat === 'snacks' && '🍿 Snacks'}
              {cat === 'loterie' && '🎫 Loterie'}
            </button>
          ))}
        </div>

        {/* Product grid P17: scroll-triggered animations */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {products.map((product, idx) => (
            <div
              key={product.id}
              className={`bg-white rounded-lg p-6 shadow-md hover:shadow-xl transition-all duration-500 ${
                idx % 2 === 0 ? 'hover:translate-y-[-4px]' : 'hover:translate-y-[-8px]'
              }`}
              style={{
                animation: `fadeInUp 0.6s ease-out ${idx * 0.1}s both`,
              }}
            >
              <div className="aspect-square bg-gradient-to-br from-amber-100 to-orange-100 rounded-lg mb-4 flex items-center justify-center text-4xl">
                {['📦', '🛍️', '🎫', '📌'][idx % 4]}
              </div>
              <h3 className="font-bold text-gray-900 text-lg">{product.name}</h3>
              {product.price && (
                <p className="text-amber-700 font-semibold text-sm mt-2">
                  {product.price}
                </p>
              )}
            </div>
          ))}
        </div>

        <style jsx>{`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          @media (prefers-reduced-motion: reduce) {
            * {
              animation: none !important;
              transition: none !important;
            }
          }
        `}</style>
      </div>
    </section>
  );
}
