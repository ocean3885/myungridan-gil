/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js',
    'node_modules/preline/dist/*.js',
  ],
  theme: {
    fontFamily: {
      'kor-nanum': ['"NanumGothic"',],
      'notosanskr': ['Noto Sans Kr',],
    },
    extend: {
      utilities: {
        '.webkit-overflow-scrolling-none': {
          '-webkit-overflow-scrolling': 'none',
        },
      },
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('preline/plugin'),
  ],
}

