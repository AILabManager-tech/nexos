'use client';

import { useEffect, useState } from 'react';

export default function Hero() {
  const [inView, setInView] = useState(false);

  useEffect(() => {
    setInView(true);
  }, []);

  return (
    <section className="relative overflow-hidden pt-20 pb-32">
      {/* Anti-polish background: raw wood texture effect */}
      <div className="absolute inset-0 bg-gradient-to-b from-amber-900 via-amber-800 to-orange-900 opacity-90"></div>
      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: `
            repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(255,255,255,.1) 2px, rgba(255,255,255,.1) 4px),
            repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,.05) 2px, rgba(0,0,0,.05) 4px)
          `,
        }}
      ></div>

      <div className="relative max-w-4xl mx-auto px-6 z-10">
        <div
          className={`space-y-6 transition-all duration-700 ${
            inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          }`}
        >
          {/* P09: 3-word brand messaging */}
          <div className="space-y-4">
            <h1 className="text-7xl md:text-8xl font-black text-white leading-tight">
              TON<br />
              <span className="text-amber-200">DÉPANNEUR.</span><br />
              TON<br />
              <span className="text-orange-300">QUARTIER.</span>
            </h1>
            <p className="text-2xl md:text-3xl text-amber-100 font-bold max-w-2xl">
              Depuis 1987. Authentique. Local. Pour toi.
            </p>
          </div>

          {/* P13: Anti-polish authenticity */}
          <div className="grid grid-cols-3 gap-4 mt-12 pt-8 border-t-2 border-amber-700">
            <div className="text-center">
              <div className="text-5xl font-black text-amber-200">37</div>
              <p className="text-amber-100 text-sm font-medium mt-2">Ans de<br />confiance</p>
            </div>
            <div className="text-center">
              <div className="text-5xl font-black text-orange-300">500+</div>
              <p className="text-amber-100 text-sm font-medium mt-2">Produits en<br />stock</p>
            </div>
            <div className="text-center">
              <div className="text-5xl font-black text-amber-200">24/7</div>
              <p className="text-amber-100 text-sm font-medium mt-2">Ouvert pour<br />toi</p>
            </div>
          </div>

          <p className="text-amber-50 text-lg italic mt-8 max-w-xl leading-relaxed">
            Pas de chaîne. Pas de marketing tape-à-l'œil.<br />
            Juste un vrai dépanneur qui te connaît.
          </p>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-b from-transparent to-white"></div>
    </section>
  );
}
