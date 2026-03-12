<template>
  <div class="container">
    <header>
      <h1>📚 考纲幻灯片</h1>
      <p class="subtitle">在线考试考纲幻灯片展示</p>
    </header>

    <main>
      <div v-for="board in examBoards" :key="board.id" class="board-section">
        <h2>{{ board.name }}</h2>
        <div v-for="syllabus in board.syllabi" :key="syllabus.id" class="syllabus-section">
          <div class="syllabus-header">
            <span class="syllabus-icon">{{ syllabus.icon }}</span>
            <div>
              <h3 class="syllabus-title">{{ syllabus.code }} — {{ syllabus.name }}</h3>
              <span class="chapters">{{ syllabus.chapters.length }} 章节</span>
            </div>
          </div>
          <div class="chapters-grid">
            <a
              v-for="chapter in syllabus.chapters"
              :key="chapter.id"
              :href="chapter.url"
              class="chapter-card"
            >
              <div class="chapter-number">Ch.{{ chapter.number }}</div>
              <div class="chapter-content">
                <h4>{{ chapter.title }}</h4>
                <p>{{ chapter.subtitle }}</p>
              </div>
            </a>
          </div>
        </div>
      </div>
    </main>

    <footer>
      <p>基于 <a href="https://sli.dev/" target="_blank">Slidev</a> 构建</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
interface Chapter {
  id: string
  number: number
  title: string
  subtitle: string
  url: string
}

interface Syllabus {
  id: string
  code: string
  name: string
  icon: string
  chapters: Chapter[]
}

interface ExamBoard {
  id: string
  name: string
  syllabi: Syllabus[]
}

const base = import.meta.env.BASE_URL

const examBoards: ExamBoard[] = [
  {
    id: 'cie',
    name: 'CIE (Cambridge International Examinations)',
    syllabi: [
      {
        id: 'cie-9700',
        code: '9700',
        name: 'AS & A Level Biology',
        icon: '🧬',
        chapters: [
          {
            id: 'cie-9700-ch1',
            number: 1,
            title: '细胞结构',
            subtitle: 'Cell Structure',
            url: `${base}slides/cie-9700/`,
          },
          {
            id: 'cie-9700-ch2',
            number: 2,
            title: '生物分子',
            subtitle: 'Biological Molecules',
            url: `${base}slides/cie-9700/chapter-2/`,
          },
        ],
      },
    ],
  },
]
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  color: #333;
  min-height: 100vh;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

header {
  text-align: center;
  margin-bottom: 3rem;
}

header h1 {
  font-size: 2.5rem;
  color: #1a73e8;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.board-section {
  margin-bottom: 2.5rem;
}

.board-section h2 {
  font-size: 1.3rem;
  color: #444;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.syllabus-section {
  margin-bottom: 2rem;
}

.syllabus-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.syllabus-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.syllabus-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.chapters {
  font-size: 0.8rem;
  color: #888;
  background: #f0f0f0;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
}

.chapters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.chapter-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border-radius: 12px;
  padding: 1.1rem 1.25rem;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.chapter-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.chapter-number {
  font-size: 1rem;
  font-weight: 700;
  color: #1a73e8;
  background: #e8f0fe;
  border-radius: 8px;
  padding: 0.4rem 0.6rem;
  flex-shrink: 0;
}

.chapter-content h4 {
  font-size: 1rem;
  color: #1a73e8;
  margin-bottom: 0.15rem;
}

.chapter-content p {
  font-size: 0.82rem;
  color: #777;
}

footer {
  text-align: center;
  margin-top: 4rem;
  color: #999;
  font-size: 0.9rem;
}

footer a {
  color: #1a73e8;
  text-decoration: none;
}
</style>
