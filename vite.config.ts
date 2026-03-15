import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/slidev-exam-ppts/',
  build: {
    outDir: 'dist',
  },
  assetsInclude: ['**/*.md'],
  optimizeDeps: {
    include: ['markdown-it', 'prismjs', 'katex']
  }
})
