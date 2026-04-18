export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white pt-16 pb-8">
      <div className="max-w-5xl mx-auto px-6">
        <div className="grid md:grid-cols-3 gap-12 mb-12">
          <div>
            <h3 className="font-black text-2xl mb-4">
              DÉPANNEUR<br />
              <span className="text-amber-400">NOBERT</span>
            </h3>
            <p className="text-gray-400 text-sm">
              Commerce de proximité authentique depuis 1987.
              Ton quartier. Ton dépanneur.
            </p>
          </div>

          <div>
            <h4 className="font-bold mb-4 text-amber-400">Lien rapides</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="#" className="hover:text-white transition">À propos</a></li>
              <li><a href="#" className="hover:text-white transition">Nos emplacements</a></li>
              <li><a href="#" className="hover:text-white transition">Politiques</a></li>
              <li><a href="#" className="hover:text-white transition">Contact</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-4 text-amber-400">Nous joindre</h4>
            <p className="text-gray-400 text-sm mb-2">
              (514) 555-0101
            </p>
            <p className="text-gray-400 text-sm">
              Ouvert 24/7 pour toi
            </p>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-500">
          <p>&copy; 2026 Dépanneur Nobert. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
}
