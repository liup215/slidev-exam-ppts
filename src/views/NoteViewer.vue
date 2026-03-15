<template>
  <div class="container">
    <header>
      <h1>📚 考纲幻灯片</h1>
      <p class="subtitle">在线考试考纲幻灯片展示</p>
    </header>

    <nav class="breadcrumb" aria-label="当前位置">
      <a class="breadcrumb-item" href="#/">首页</a>
    </nav>

    <main class="note-main">
      <div v-if="loading" class="note-loading">
        <span>正在加载笔记…</span>
      </div>

      <div v-else-if="error" class="note-error">
        <p>{{ error }}</p>
        <a href="#/" class="back-btn">← 返回首页</a>
      </div>

      <article v-else class="note-article">
        <div class="note-toolbar">
          <a href="#/" class="back-btn">← 返回首页</a>
        </div>
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div class="note-body" v-html="renderedHtml"></div>
      </article>
    </main>

    <footer>
      <p>基于 <a href="https://sli.dev/" target="_blank">Slidev</a> 构建</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import katex from 'katex'

// ── Highlight.js language auto-detect (common langs bundled via hljs.highlightAuto)
// Using highlightAuto keeps the bundle smaller than importing all languages.

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(code, { language: lang, ignoreIllegals: true }).value}</code></pre>`
      } catch {
        // fall through to default
      }
    }
    return `<pre class="hljs"><code>${hljs.highlightAuto(code).value}</code></pre>`
  },
})

// ── KaTeX rendering helper
function renderMath(tex: string, displayMode: boolean): string {
  try {
    return katex.renderToString(tex, {
      displayMode,
      throwOnError: false,
      output: 'html',
    })
  } catch {
    return `<span class="math-error">${tex}</span>`
  }
}

// ── Simple math pre-processing: replace $$...$$ and $...$ with KaTeX HTML
function renderMathInHtml(html: string): string {
  // Display math: $$...$$  (processed first so inline $ regex sees none left)
  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => renderMath(tex, true))
  // Inline math: $...$  (no $ or newline inside, since $$ already consumed above)
  html = html.replace(/\$([^$\n]+?)\$/g, (_, tex) => renderMath(tex, false))
  return html
}

// ── Load all notes at build time
const noteModules = import.meta.glob('/notes/**/*.md', { query: '?raw', import: 'default' })

const route = useRoute()
const loading = ref(true)
const error = ref<string | null>(null)
const renderedHtml = ref('')

async function loadNote() {
  loading.value = true
  error.value = null
  renderedHtml.value = ''

  const { boardId, groupId, chapterId } = route.params as Record<string, string>
  const modulePath = `/notes/${boardId}/${groupId}/${chapterId}.md`
  const loader = noteModules[modulePath]

  if (!loader) {
    error.value = '该章节暂无笔记，敬请期待。'
    loading.value = false
    return
  }

  try {
    const raw = (await loader()) as string
    const parsed = md.render(raw)
    renderedHtml.value = renderMathInHtml(parsed)
  } catch {
    error.value = '笔记加载失败，请稍后重试。'
  } finally {
    loading.value = false
  }
}

onMounted(loadNote)
watch(() => route.params, loadNote)
</script>

<style>
/* ── KaTeX stylesheet ────────────────────────────────────────────────────── */
@import 'katex/dist/katex.min.css';

/* ── highlight.js theme (GitHub) ─────────────────────────────────────────── */
@import 'highlight.js/styles/github.css';
</style>

<style scoped>
.note-main {
  min-height: 60vh;
}

.note-loading {
  text-align: center;
  padding: 4rem;
  color: #888;
  font-size: 1.1rem;
}

.note-error {
  text-align: center;
  padding: 4rem 2rem;
  color: #555;
}

.note-error p {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.back-btn {
  display: inline-block;
  color: #1a73e8;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  transition: background 0.15s;
}

.back-btn:hover {
  background: #e8f0fe;
}

.note-toolbar {
  margin-bottom: 1.5rem;
}

.note-article {
  background: white;
  border-radius: 16px;
  padding: 2rem 2.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  max-width: 860px;
  margin: 0 auto;
}

/* ── Markdown body typography ─────────────────────────────────────────────── */
.note-body {
  line-height: 1.8;
  color: #333;
  font-size: 1rem;
}

.note-body :deep(h1) {
  font-size: 1.9rem;
  color: #1a73e8;
  border-bottom: 2px solid #e8f0fe;
  padding-bottom: 0.5rem;
  margin: 0 0 1.5rem;
}

.note-body :deep(h2) {
  font-size: 1.4rem;
  color: #1558b0;
  margin: 2rem 0 0.75rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #e8f0fe;
}

.note-body :deep(h3) {
  font-size: 1.15rem;
  color: #1a73e8;
  margin: 1.5rem 0 0.5rem;
}

.note-body :deep(h4) {
  font-size: 1.05rem;
  color: #333;
  margin: 1rem 0 0.4rem;
}

.note-body :deep(p) {
  margin: 0.75rem 0;
}

.note-body :deep(ul),
.note-body :deep(ol) {
  padding-left: 1.5rem;
  margin: 0.75rem 0;
}

.note-body :deep(li) {
  margin: 0.3rem 0;
}

.note-body :deep(a) {
  color: #1a73e8;
  text-decoration: none;
}

.note-body :deep(a:hover) {
  text-decoration: underline;
}

.note-body :deep(blockquote) {
  border-left: 4px solid #1a73e8;
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  background: #f0f6ff;
  border-radius: 0 8px 8px 0;
  color: #555;
}

.note-body :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.note-body :deep(th),
.note-body :deep(td) {
  border: 1px solid #ddd;
  padding: 0.5rem 0.75rem;
  text-align: left;
}

.note-body :deep(th) {
  background: #f0f6ff;
  font-weight: 600;
  color: #1558b0;
}

.note-body :deep(tr:nth-child(even)) {
  background: #fafafa;
}

.note-body :deep(pre.hljs) {
  border-radius: 10px;
  padding: 1rem 1.25rem;
  overflow-x: auto;
  margin: 1rem 0;
  font-size: 0.88rem;
}

.note-body :deep(code) {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}

.note-body :deep(:not(pre) > code) {
  background: #f0f0f0;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.88em;
}

.note-body :deep(hr) {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 2rem 0;
}

.note-body :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

/* KaTeX display block centering */
.note-body :deep(.katex-display) {
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0.5rem 0;
}

.math-error {
  color: #c0392b;
  font-style: italic;
}

@media (max-width: 600px) {
  .note-article {
    padding: 1.25rem 1rem;
  }

  .note-body :deep(h1) {
    font-size: 1.4rem;
  }

  .note-body :deep(h2) {
    font-size: 1.15rem;
  }

  .note-body :deep(table) {
    font-size: 0.8rem;
  }
}
</style>
