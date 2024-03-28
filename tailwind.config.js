/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js',
    './node_modules/preline/dist/*.js',
  ],
  theme: {
    fontFamily: {
      'notosanskr': ['"Noto Sans KR"', ],
    },
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
    require('preline/plugin'),
  ],
}

