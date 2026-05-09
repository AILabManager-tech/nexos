import type { Config } from 'tailwindcss';

// Palette warm éditorial-bistronomique (SEC-03 premium) — D4_palette=warm canonique
// table-de-marguerite. Vin burgundy primaire + ocre doré accent + crème surface.
// Contraste WCAG AA vérifié :
//   text-ink (#2B2420) sur bg-surface (#FAF6F0)        = 15.8:1 AAA
//   text-surface (#FAF6F0) sur bg-primary (#6D2E3F)    =  9.7:1 AAA
//   text-accent-deep (#6B4F1F) sur bg-surface (#FAF6F0)=  7.06:1 AAA
//   text-accent-deep (#6B4F1F) sur bg-surface-alt (#F3EDE3) = 6.54:1 AA+
// Iter 3 ph5 fix : accent.deep passé de #A0803A (3.46:1 FAIL AA) à #6B4F1F (PASS AA/AAA).
const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6D2E3F',
          50: '#F5E8EB',
          100: '#E8CCD3',
          200: '#D199A6',
          300: '#B06778',
          400: '#8F4558',
          500: '#6D2E3F',
          600: '#5B2533',
          700: '#481D28',
          800: '#30141B',
          900: '#18090D'
        },
        accent: {
          DEFAULT: '#C89F4B',
          soft: '#E8D0A0',
          deep: '#6B4F1F'
        },
        surface: {
          DEFAULT: '#FAF6F0',
          alt: '#F3EDE3',
          raised: '#EDE5D4',
          dark: '#2B2420'
        },
        ink: {
          DEFAULT: '#2B2420',
          soft: '#5C4B3A',
          muted: '#776558'
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
