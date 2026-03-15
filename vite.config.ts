import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import fs from 'fs'

// 自定义插件：复制 notes 目录
const copyNotesPlugin = () => ({
  name: 'copy-notes',
  writeBundle() {
    const srcDir = path.resolve(__dirname, 'notes')
    const destDir = path.resolve(__dirname, 'dist', 'notes')
    
    if (fs.existsSync(srcDir)) {
      fs.cpSync(srcDir, destDir, { recursive: true, force: true })
      console.log('✅ Notes copied to dist/notes')
    }
  }
})

export default defineConfig({
  plugins: [vue(), copyNotesPlugin()],
  base: '/slidev-exam-ppts/',
  build: {
    outDir: 'dist',
  },
  assetsInclude: ['**/*.md'],
  optimizeDeps: {
    include: ['markdown-it', 'prismjs', 'katex']
  }
})
