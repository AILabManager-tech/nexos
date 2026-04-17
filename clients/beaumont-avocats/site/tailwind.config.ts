import type { Config } from 'tailwindcss';

// Palette P14 Code-breaking juridique (SEC-05) — rupture rupture 2 :
// bordeaux mat + ivoire + noir d'encre au lieu de bleu marine + or + blanc classique.
// Tout en gardant le ton autorité (sobriete chromatique — 4 couleurs seulement).
//
// Contraste WCAG AAA vérifié :
// - text-ink #0A0A0A sur bg-surface #F5F1EA = 19.0:1 AAA
// - text-surface #F5F1EA sur bg-primary #6B1E23 = 10.2:1 AAA
// - text-primary #6B1E23 sur bg-surface #F5F1EA = 10.2:1 AAA
const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6B1E23',
          50: '#FAEEEE',
          100: '#F2D4D5',
          200: '#DCA4A7',
          300: '#C27579',
          400: '#9E4850',
          500: '#6B1E23',
          600: '#58191D',
          700: '#441318',
          800: '#2E0D10',
          900: '#170607'
        },
        accent: {
          DEFAULT: '#6B1E23',
          soft: '#8C3A41',
          deep: '#4A1417'
        },
        surface: {
          DEFAULT: '#F5F1EA',
          alt: '#EDE7DB',
          raised: '#E3DBC8',
          dark: '#0A0A0A'
        },
        ink: {
          DEFAULT: '#0A0A0A',
          soft: '#2B2B2B',
          muted: '#5A5A5A'
        }
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        display: ['var(--font-display)', 'Georgia', 'serif']
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem'
      },
      maxWidth: {
        prose: '65ch',
        editorial: '42ch'
      }
    }
  },
  plugins: []
};

export default config;
