/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#17201b',
        moss: '#3f5f49',
        mint: '#dff3e7',
        blush: '#f7ded7',
        amber: '#f3c677',
      },
      boxShadow: {
        soft: '0 18px 50px rgba(23, 32, 27, 0.10)',
      },
    },
  },
  plugins: [],
};
