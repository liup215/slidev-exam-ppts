import MarkdownIt from 'markdown-it'
import Prism from 'prismjs'

// Load common Prism languages
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-css'
import 'prismjs/components/prism-markdown'

// KaTeX for math rendering
import katex from 'katex'
import 'katex/dist/katex.min.css'

// Create markdown-it instance with options
export const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: (code: string, lang: string) => {
    if (lang && Prism.languages[lang]) {
      return Prism.highlight(code, Prism.languages[lang], lang)
    }
    return code
  }
})

// Custom KaTeX plugin for math rendering
const mathRegex = /\$\$(.+?)\$\$/gs
const inlineMathRegex = /\$(.+?)\$/g

export function renderMath(content: string): string {
  // Render block math
  let result = content.replace(mathRegex, (match, tex) => {
    try {
      return katex.renderToString(tex.trim(), {
        displayMode: true,
        throwOnError: false
      })
    } catch (e) {
      return match
    }
  })
  
  // Render inline math
  result = result.replace(inlineMathRegex, (match, tex) => {
    try {
      return katex.renderToString(tex.trim(), {
        displayMode: false,
        throwOnError: false
      })
    } catch (e) {
      return match
    }
  })
  
  return result
}

export function renderMarkdown(content: string): string {
  const html = md.render(content)
  return renderMath(html)
}
