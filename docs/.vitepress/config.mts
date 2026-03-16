import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "A-Level Biology",
  description: "A-Level Biology Study Notes and Slides",
  base: '/slidev-exam-ppts/',
  
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'CIE', link: '/cie/' },
      { text: 'Bio Competition', link: '/bio-competition/' }
    ],

    sidebar: {
      '/cie/': [
        {
          text: 'CIE Biology 9700',
          items: [
            { text: 'Overview', link: '/cie/' },
            {
              text: 'AS Level',
              collapsed: false,
              items: [
                { text: 'Chapter 1: Cell Structure', link: '/cie/as/chapter1' },
                { text: 'Chapter 2: Biological Molecules', link: '/cie/as/chapter2' },
                { text: 'Chapter 3: Cell Membranes', link: '/cie/as/chapter3' }
              ]
            }
          ]
        }
      ],
      '/bio-competition/': [
        {
          text: 'Bio Competition',
          items: [
            { text: 'Overview', link: '/bio-competition/' },
            {
              text: 'Molecular Biology of the Cell',
              collapsed: false,
              items: [
                { text: 'Chapter 7: Control of Gene Expression', link: '/bio-competition/molecular-biology/chapter7' }
              ]
            }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/liup215/slidev-exam-ppts' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026-present'
    }
  }
})
