import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        /* Brand global */
        brand: {
          primary: '#FF6B6B',
          bg: '#0D0D0D'
        },
        /* P18 Hero — noir + corail */
        hero: {
          bg: '#0A0A0A',
          accent: '#FF6B6B',
          text: '#F5F5F0'
        },
        /* P18 Services — violet + lavande */
        services: {
          bg: '#1A1E3A',
          accent: '#A78BFA',
          text: '#FFFFFF'
        },
        /* P18 Case Studies — ivoire + or */
        cases: {
          bg: '#F5F5F0',
          accent: '#D4AF37',
          text: '#1A1A1A'
        },
        /* Fallbacks */
        primary: {
          DEFAULT: '#FF6B6B',
          50: '#FFF0F0',
          100: '#FFE0E0',
          500: '#FF6B6B',
          700: '#CC5555',
          900: '#660000'
        },
        surface: {
          DEFAULT: '#FFFFFF',
          alt: '#F5F5F0',
          dark: '#0D0D0D'
        },
        ink: {
          DEFAULT: '#1A1A1A',
          soft: '#4A4A4A',
          muted: '#7A7A7A'
        }
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        display: ['var(--font-display)', 'system-ui', 'sans-serif'],
        serif: ['var(--font-serif)', 'Georgia', 'serif'],
        serif2: ['var(--font-serif2)', 'Georgia', 'serif']
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
