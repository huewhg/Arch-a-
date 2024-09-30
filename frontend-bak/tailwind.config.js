/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');

module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./templates/**/*.{html,js}"
  ],
  theme: {
    extend: {

    },
    colors: {
      'red': '#a63333',
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
      gray: colors.slate,
      green: colors.emerald,
      purple: colors.violet,
      pink: colors.fuchsia,
    },
  },
  plugins: [],
}
