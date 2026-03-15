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
  // Go back to home (chapter list view)
  router.push('/')
}

watch(() => [props.board, props.group, props.chapter], loadNote, { immediate: true })

onMounted(loadNote)
</script>

<style scoped>
/* ===== 基础布局 ===== */
.note-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ===== 头部区域 ===== */
.note-header {
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

/* 面包屑导航 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
  font-size: 0.9rem;
  flex-wrap: wrap;
}

.breadcrumb-item {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.95);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.breadcrumb-item:hover:not(.active) {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.breadcrumb-item.active {
  color: #fff;
  cursor: default;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.3);
}

.breadcrumb-sep {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  user-select: none;
}

/* 操作按钮 */
.note-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.ppt-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-color: transparent;
}

.ppt-btn:hover {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
}

/* ===== 内容区域 ===== */
.note-content {
  flex: 1;
  background: #fff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 10px 15px -3px rgba(0, 0, 0, 0.08),
    0 20px 25px -5px rgba(0, 0, 0, 0.05);
  position: relative;
}

.note-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  border-radius: 20px 20px 0 0;
}

/* ===== 加载/错误/空状态 ===== */
.loading, .error, .empty {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-right: 4px solid #764ba2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error h3 {
  color: #e74c3c;
  margin-bottom: 0.75rem;
  font-size: 1.3rem;
}

.empty h3 {
  color: #667eea;
  margin-bottom: 0.75rem;
  font-size: 1.3rem;
}

.retry-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* ===== 页脚 ===== */
.note-footer {
  text-align: center;
  margin-top: 3rem;
  padding: 1.5rem;
  color: #888;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.note-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.note-footer a:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* ===== Markdown 内容样式 ===== */
.markdown-body {
  color: #2d3748;
  line-height: 1.8;
}

/* 标题样式 */
.markdown-body :deep(h1) {
  font-size: 2.25rem;
  color: #1a202c;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid;
  border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.markdown-body :deep(h2) {
  font-size: 1.75rem;
  color: #2d3748;
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
  padding-left: 1rem;
  border-left: 4px solid #667eea;
  font-weight: 600;
}

.markdown-body :deep(h3) {
  font-size: 1.35rem;
  color: #4a5568;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.markdown-body :deep(h3)::before {
  content: '▸';
  color: #764ba2;
  font-size: 1rem;
}

.markdown-body :deep(h4) {
  font-size: 1.15rem;
  color: #4a5568;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

/* 段落 */
.markdown-body :deep(p) {
  line-height: 1.9;
  margin-bottom: 1.25rem;
  color: #4a5568;
}

/* 列表 */
.markdown-body :deep(ul), .markdown-body :deep(ol) {
  margin-bottom: 1.25rem;
  padding-left: 1.75rem;
}

.markdown-body :deep(ul) {
  list-style: none;
}

.markdown-body :deep(ul li) {
  position: relative;
  margin-bottom: 0.6rem;
  line-height: 1.7;
  padding-left: 0.5rem;
}

.markdown-body :deep(ul li::before) {
  content: '•';
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: -1.25rem;
  font-size: 1.2rem;
}

.markdown-body :deep(ol li) {
  margin-bottom: 0.6rem;
  line-height: 1.7;
  padding-left: 0.5rem;
}

.markdown-body :deep(ol li::marker) {
  color: #667eea;
  font-weight: 600;
}

/* 代码样式 */
.markdown-body :deep(code) {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Monaco', monospace;
  font-size: 0.88em;
  color: #764ba2;
  border: 1px solid #e2e8f0;
}

.markdown-body :deep(pre) {
  background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
  padding: 1.25rem;
  border-radius: 12px;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.markdown-body :deep(pre::before) {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 30px;
  background: linear-gradient(90deg, #ff5f56 0%, #ff5f56 12px, #ffbd2e 12px, #ffbd2e 24px, #27c93f 24px, #27c93f 36px, transparent 36px);
  border-radius: 12px 12px 0 0;
  opacity: 0.8;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: #e2e8f0;
  border: none;
  font-size: 0.9em;
  line-height: 1.6;
  display: block;
  margin-top: 20px;
}

/* 引用块 */
.markdown-body :deep(blockquote) {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  border-left: 4px solid #667eea;
  padding: 1.25rem 1.5rem;
  margin: 1.5rem 0;
  border-radius: 0 12px 12px 0;
  color: #4a5568;
  font-style: italic;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.markdown-body :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

/* 表格样式 */
.markdown-body :deep(table) {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 1.5rem;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.markdown-body :deep(thead) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.markdown-body :deep(th) {
  color: white;
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  font-size: 0.95rem;
}

.markdown-body :deep(td) {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid #e2e8f0;
  color: #4a5568;
}

.markdown-body :deep(tr:nth-child(even)) {
  background: #f7fafc;
}

.markdown-body :deep(tr:hover) {
  background: #edf2f7;
  transition: background 0.2s;
}

.markdown-body :deep(tr:last-child td) {
  border-bottom: none;
}

/* 图片 */
.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 1.5rem 0;
  display: block;
}

/* 链接 */
.markdown-body :deep(a) {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.markdown-body :deep(a:hover) {
  color: #764ba2;
  border-bottom-color: #764ba2;
}

/* 水平线 */
.markdown-body :deep(hr) {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%);
  margin: 2.5rem 0;
}

/* 强调文本 */
.markdown-body :deep(strong) {
  color: #2d3748;
  font-weight: 600;
}

.markdown-body :deep(em) {
  color: #667eea;
}

/* 数学公式 */
.markdown-body :deep(.katex) {
  font-size: 1.1em;
}

.markdown-body :deep(.katex-display) {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
  overflow-x: auto;
}

/* ===== 响应式设计 ===== */
@media (max-width: 768px) {
  .note-container {
    padding: 1rem;
  }
  
  .note-header {
    padding: 1.25rem;
    border-radius: 12px;
  }
  
  .note-content {
    padding: 1.5rem;
    border-radius: 16px;
  }
  
  .markdown-body :deep(h1) {
    font-size: 1.75rem;
  }
  
  .markdown-body :deep(h2) {
    font-size: 1.4rem;
  }
  
  .markdown-body :deep(h3) {
    font-size: 1.15rem;
  }
  
  .breadcrumb {
    font-size: 0.8rem;
  }
  
  .breadcrumb-item {
    padding: 0.3rem 0.6rem;
  }
}

@media (max-width: 480px) {
  .note-header {
    padding: 1rem;
  }
  
  .note-content {
    padding: 1.25rem;
  }
  
  .action-btn {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
  
  .markdown-body :deep(pre) {
    padding: 1rem;
    font-size: 0.85em;
  }
  
  .markdown-body :deep(table) {
    font-size: 0.9rem;
  }
  
  .markdown-body :deep(th),
  .markdown-body :deep(td) {
    padding: 0.625rem 0.75rem;
  }
}
</style>
