<template>
  <div class="container">
    <header>
      <h1>📚 考纲幻灯片</h1>
      <p class="subtitle">在线考试考纲幻灯片展示</p>
    </header>

    <main>
      <div v-for="board in examBoards" :key="board.id" class="board-section">
        <h2>{{ board.name }}</h2>
        <div class="syllabi-grid">
          <a
            v-for="syllabus in board.syllabi"
            :key="syllabus.id"
            :href="syllabus.url"
            class="syllabus-card"
          >
            <div class="card-icon">{{ syllabus.icon }}</div>
            <div class="card-content">
              <h3>{{ syllabus.code }}</h3>
              <p>{{ syllabus.name }}</p>
              <span class="chapters">{{ syllabus.chapters }} 章节</span>
            </div>
          </a>
        </div>
      </div>
    </main>

    <footer>
      <p>基于 <a href="https://sli.dev/" target="_blank">Slidev</a> 构建</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
interface Syllabus {
  id: string
  code: string
  name: string
  icon: string
  chapters: number
  url: string
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
        chapters: 1,
        url: `${base}slides/cie-9700/`,
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

.syllabi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}

.syllabus-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.syllabus-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.card-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.card-content h3 {
  font-size: 1.1rem;
  color: #1a73e8;
  margin-bottom: 0.2rem;
}

.card-content p {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.4rem;
}

.chapters {
  font-size: 0.8rem;
  color: #888;
  background: #f0f0f0;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
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
