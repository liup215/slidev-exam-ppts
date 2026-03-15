<template>
  <div class="note-container">
    <header class="note-header">
      <nav class="breadcrumb" aria-label="当前位置">
        <button class="breadcrumb-item" @click="goHome">首页</button>
        <span class="breadcrumb-sep">›</span>
        <button class="breadcrumb-item" @click="goBack">{{ boardName }}</button>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item">{{ groupName }}</span>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item active">{{ chapterTitle }}</span>
      </nav>
      <div class="note-actions">
        <button class="action-btn" @click="goBack" title="返回章节列表">
          <span>←</span> 返回
        </button>
        <a v-if="pptUrl && pptUrl !== '#'" :href="pptUrl" class="action-btn ppt-btn" target="_blank">
          📊 查看 PPT
        </a>
      </div>
    </header>

    <main class="note-content">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载笔记中...</p>
      </div>
      <div v-else-if="error" class="error">
        <h3>⚠️ 加载失败</h3>
        <p>{{ error }}</p>
        <button @click="loadNote" class="retry-btn">重试</button>
      </div>
      <div v-else-if="!content" class="empty">
        <h3>📝 暂无笔记</h3>
        <p>该章节暂时没有笔记内容</p>
      </div>
      <article v-else class="markdown-body" v-html="renderedContent"></article>
    </main>

    <footer class="note-footer">
      <p>基于 <a href="https://sli.dev/" target="_blank">Slidev</a> 构建 | 笔记系统</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { renderMarkdown } from '../utils/markdown'
import 'prismjs/themes/prism-tomorrow.css'

interface Props {
  board: string
  group: string
  chapter: string
}

const props = defineProps<Props>()
const router = useRouter()

const loading = ref(false)
const error = ref('')
const content = ref('')
const boardName = ref('')
const groupName = ref('')
const chapterTitle = ref('')
const pptUrl = ref('')

const renderedContent = computed(() => {
  if (!content.value) return ''
  return renderMarkdown(content.value)
})

// Import all markdown files
const noteModules = import.meta.glob('/notes/**/*.md', { query: '?raw', import: 'default', eager: false })

async function loadNote() {
  loading.value = true
  error.value = ''
  content.value = ''

  try {
    // Try different path patterns to find the note file
    // Pattern 1: /notes/{board}/{group}/{chapter}.md
    const notePath = `/notes/${props.board}/${props.group}/${props.chapter}.md`
    // Pattern 2: /notes/{board}/{chapter}.md
    const altPath = `/notes/${props.board}/${props.chapter}.md`
    // Pattern 3: /notes/{board}/chapter-{number}.md (for cie-9700 style)
    const chapterNum = props.chapter.match(/ch(\d+)$/i)?.[1]
    const chapterPath = chapterNum ? `/notes/${props.board}/chapter-${chapterNum}.md` : null
    
    let loader = noteModules[notePath]
    let foundPath = notePath
    
    if (!loader) {
      loader = noteModules[altPath]
      foundPath = altPath
    }
    
    if (!loader && chapterPath) {
      loader = noteModules[chapterPath]
      foundPath = chapterPath
    }
    
    if (loader) {
      const noteContent = await loader()
      content.value = noteContent as string
    }

    // Load metadata from examBoards data structure
    await loadMetadata()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '未知错误'
  } finally {
    loading.value = false
  }
}

async function loadMetadata() {
  // This would ideally come from a shared data file
  // For now, we'll set basic names based on the URL params
  boardName.value = decodeURIComponent(props.board).replace(/-/g, ' ')
  groupName.value = decodeURIComponent(props.group).replace(/-/g, ' ')
  chapterTitle.value = decodeURIComponent(props.chapter).replace(/-/g, ' ')
  
  // Map to actual names (this should be improved to use shared data)
  const boardMap: Record<string, string> = {
    'cie-9700': 'A-Level Biology (9700)',
    'bio-competition': '生物竞赛'
  }
  
  if (boardMap[props.board]) {
    boardName.value = boardMap[props.board]
  }
}

function goHome() {
  router.push('/')
}

function goBack() {
  router.push('/')
}

watch(() => [props.board, props.group, props.chapter], loadNote, { immediate: true })

onMounted(loadNote)
</script>

<style scoped>
.note-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.note-header {
  margin-bottom: 2rem;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  flex-wrap: wrap;
}

.breadcrumb-item {
  background: none;
  border: none;
  cursor: pointer;
  color: #1a73e8;
  padding: 0.25rem 0.4rem;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: background 0.15s;
}

.breadcrumb-item:hover:not(.active) {
  background: #e8f0fe;
}

.breadcrumb-item.active {
  color: #444;
  cursor: default;
  font-weight: 600;
}

.breadcrumb-sep {
  color: #999;
  font-size: 1rem;
  user-select: none;
}

.note-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #333;
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.15s;
}

.action-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

.ppt-btn {
  background: #1a73e8;
  color: white;
  border-color: #1a73e8;
}

.ppt-btn:hover {
  background: #1557b0;
  border-color: #1557b0;
}

.note-content {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.loading, .error, .empty {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #1a73e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error h3, .empty h3 {
  color: #d93025;
  margin-bottom: 0.5rem;
}

.empty h3 {
  color: #666;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #1a73e8;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.retry-btn:hover {
  background: #1557b0;
}

.note-footer {
  text-align: center;
  margin-top: 3rem;
  color: #999;
  font-size: 0.9rem;
}

.note-footer a {
  color: #1a73e8;
  text-decoration: none;
}

/* Markdown content styles */
.markdown-body :deep(h1) {
  font-size: 2rem;
  color: #1a73e8;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e8f0fe;
}

.markdown-body :deep(h2) {
  font-size: 1.5rem;
  color: #333;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.markdown-body :deep(h3) {
  font-size: 1.25rem;
  color: #444;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.markdown-body :deep(p) {
  line-height: 1.8;
  margin-bottom: 1rem;
  color: #333;
}

.markdown-body :deep(ul), .markdown-body :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.markdown-body :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.markdown-body :deep(code) {
  background: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9em;
}

.markdown-body :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
}

.markdown-body :deep(blockquote) {
  border-left: 4px solid #1a73e8;
  padding-left: 1rem;
  margin-left: 0;
  color: #666;
  font-style: italic;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.markdown-body :deep(th), .markdown-body :deep(td) {
  border: 1px solid #ddd;
  padding: 0.5rem;
}

.markdown-body :deep(th) {
  background: #f8f9fa;
  font-weight: 600;
}

.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.markdown-body :deep(a) {
  color: #1a73e8;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid #eee;
  margin: 2rem 0;
}

@media (max-width: 600px) {
  .note-container {
    padding: 1rem;
  }
  
  .note-content {
    padding: 1rem;
  }
  
  .markdown-body :deep(h1) {
    font-size: 1.5rem;
  }
  
  .markdown-body :deep(h2) {
    font-size: 1.25rem;
  }
}
</style>
