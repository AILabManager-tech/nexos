'use client';

export default function StorySection() {
  return (
    <section id="nous" className="py-24 bg-amber-50">
      <div className="max-w-4xl mx-auto px-6">
        <h2 className="text-4xl md:text-5xl font-black text-amber-900 mb-12">
          Notre histoire
        </h2>

        {/* P19: StoryBrand framework — You (hero) + Us (guide) */}
        <div className="space-y-8">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-black text-amber-900 mb-4">
                Tu es le héros.
              </h3>
              <p className="text-gray-700 text-lg leading-relaxed mb-4">
                Tu cherches un endroit où on te connaît. Où tes besoins comptent vraiment.
                Où tu n'es pas juste un numéro dans un système. Un vrai voisin parmi les
                tiens.
              </p>
              <p className="text-amber-700 font-bold">
                C'est ce que tu mérites.
              </p>
            </div>
            <div className="bg-gradient-to-br from-amber-200 to-orange-200 aspect-square rounded-lg flex items-center justify-center text-6xl">
              🧑‍🤝‍🧑
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="bg-gradient-to-br from-orange-200 to-amber-200 aspect-square rounded-lg flex items-center justify-center text-6xl order-last md:order-first">
              🏪
            </div>
            <div>
              <h3 className="text-2xl font-black text-amber-900 mb-4">
                Nobert, c'est nous.
              </h3>
              <p className="text-gray-700 text-lg leading-relaxed mb-4">
                Depuis 37 ans, on bâtit une communauté. Pas une chaîne.
              </p>
              <ul className="space-y-3 text-gray-700">
                <li className="flex gap-3">
                  <span>✓</span>
                  <span>On te vend ce qu'il te faut, au juste prix.</span>
                </li>
                <li className="flex gap-3">
                  <span>✓</span>
                  <span>On pense à toi les jours de fête.</span>
                </li>
                <li className="flex gap-3">
                  <span>✓</span>
                  <span>On apprend tes préférences et on s'adapte.</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-white rounded-lg p-8 border-4 border-amber-700">
            <h3 className="text-xl font-black text-amber-900 mb-4">
              Ton action — simple.
            </h3>
            <p className="text-gray-700 text-lg mb-6">
              Viens nous voir au coin de ta rue. Ou appelle-nous pour des questions. On est
              là pour toi — 24/7, 365 jours par année. Zéro complication.
            </p>
            <button className="px-8 py-4 bg-amber-700 text-white font-bold rounded-lg hover:bg-amber-800 transition text-lg">
              Nous appeler maintenant
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
