/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js',
    './node_modules/preline/dist/*.js',
  ],
  theme: {
    fontFamily: {
      'kor-nanum': ['"NanumGothic"',],
      'notosanskr': ['Noto Sans Kr',],
    },
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
    require('preline/plugin'),
  ],
}

