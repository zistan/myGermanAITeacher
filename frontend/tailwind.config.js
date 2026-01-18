/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // German flag colors
        german: {
          black: '#000000',
          red: '#DD0000',
          gold: '#FFCC00',
        },
        // Application colors
        primary: {
          50: '#FFFBEB',
          100: '#FFF4CC',
          200: '#FFE999',
          300: '#FFDD66',
          400: '#FFD133',
          500: '#FFCC00', // German gold
          600: '#CCA300',
          700: '#997A00',
          800: '#665200',
          900: '#332900',
        },
        danger: {
          50: '#FFEBEB',
          100: '#FFCCCC',
          200: '#FF9999',
          300: '#FF6666',
          400: '#FF3333',
          500: '#DD0000', // German red
          600: '#B10000',
          700: '#850000',
          800: '#590000',
          900: '#2D0000',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

