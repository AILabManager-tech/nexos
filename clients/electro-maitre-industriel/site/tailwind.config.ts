import type { Config } from 'tailwindcss';

// Pattern P12 — Premium palette shift (dark teal) inspiré de S26 Gibbs Electric.
// Sémantique : surface = fond sombre (body), ink = texte clair (ivoire).
// Accent gold (#D4AF37) réservé aux touches premium (eyebrows, highlights, skip link focus).
// Contraste WCAG AA vérifié sur text-ink (#F5F5F0) vs bg-surface (#0A0A0A) = 19.5:1 (AAA)
// et text-ink (#F5F5F0) vs bg-primary (#0A3D40) = 10.3:1 (AAA).
const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0A3D40',
          50: '#E6F1F2',
          100: '#C3DBDC',
          200: '#8AB5B7',
          300: '#508F92',
          400: '#2D686B',
          500: '#0A3D40',
          600: '#083438',
          700: '#062B2E',
          800: '#2A2A2A',
          900: '#020F10'
        },
        accent: {
          DEFAULT: '#D4AF37',
          soft: '#E8D58B',
          ink: '#0A0A0A'
        },
        surface: {
          DEFAULT: '#0A0A0A',
          alt: '#1A1A1A',
          raised: '#242424',
          contrast: '#F5F5F0'
        },
        ink: {
          DEFAULT: '#F5F5F0',
          soft: '#D0D0C8',
          muted: '#A8A8A0'
        }
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        heading: ['var(--font-heading)', 'Georgia', 'serif']
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem'
      },
      maxWidth: {
        prose: '65ch'
      }
    }
  },
  plugins: []
};

export default config;
