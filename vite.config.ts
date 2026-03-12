import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/slidev-exam-ppts/',
  build: {
    outDir: 'dist',
  },
})
