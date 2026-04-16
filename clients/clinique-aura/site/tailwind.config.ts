import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8B6344',
          50: '#FAF6F1',
          100: '#F5EDE3',
          200: '#E8D3BD',
          300: '#D4A574',
          400: '#B8896A',
          500: '#8B6344',
          600: '#6F4E35',
          700: '#533A28',
          800: '#37271B',
          900: '#1C130D'
        },
        accent: {
          DEFAULT: '#D4A574',
          soft: '#E8D3BD'
        },
        surface: {
          DEFAULT: '#FAF8F4',
          alt: '#F5EFE6',
          dark: '#2D2420'
        },
        ink: {
          DEFAULT: '#2D2420',
          soft: '#5C4B3A',
          muted: '#8A7864'
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
