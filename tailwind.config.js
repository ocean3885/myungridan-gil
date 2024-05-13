/** @type {import('tailwindcss').Config} */
module.exports = {
  rippleui: {
		removeThemes: ["dark"],
	},
  darkMode: 'selector',
  // important: "html",
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js',
    './node_modules/preline/dist/*.js',
  ],
  theme: {
    fontFamily: {
      'notosanskr': ['"Noto Sans KR"', ],
    },
    extend: {
      screens: {
        print: { raw: 'print' },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('flowbite/plugin'),
    require('preline/plugin'),
    require("rippleui"),
  ],
}

