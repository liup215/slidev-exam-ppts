<template>
  <div class="container">
    <header>
      <h1>📚 考纲幻灯片</h1>
      <p class="subtitle">在线考试考纲幻灯片展示</p>
    </header>

    <main>
      <div class="board-grid">
        <button
          v-for="board in examBoards"
          :key="board.id"
          class="board-card"
          @click="selectBoard(board)"
        >
          <span class="board-icon">{{ board.icon }}</span>
          <div class="board-info">
            <h2>{{ board.name }}</h2>
            <p v-if="board.description">{{ board.description }}</p>
            <span class="board-meta">{{ board.groups.length }} 个板块</span>
          </div>
          <span class="board-arrow">›</span>
        </button>
      </div>
    </main>

    <footer>
      <p>基于 <a href="https://sli.dev/" target="_blank">Slidev</a> 构建</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const base = '/slidev-exam-ppts/'

const examBoards = [
  {
    id: 'bio-competition',
    name: '生物竞赛',
    icon: '🏆',
    description: '全国及国际生物学竞赛备考',
    groups: []
  },
  {
    id: 'cie-9700',
    name: 'A-Level Biology (9700)',
    icon: '🧬',
    description: 'Cambridge International AS & A Level Biology',
    groups: []
  }
]

function selectBoard(board: any) {
  router.push(`/board/${board.id}`)
}
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
  margin-bottom: 2rem;
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

.board-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.board-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  background: white;
  border: none;
  border-radius: 16px;
  padding: 1.5rem 1.75rem;
  cursor: pointer;
  text-align: left;
  width: 100%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.board-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.board-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.board-info {
  flex: 1;
}

.board-info h2 {
  font-size: 1.3rem;
  color: #1a73e8;
  margin-bottom: 0.3rem;
}

.board-info p {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.4rem;
}

.board-meta {
  font-size: 0.8rem;
  color: #888;
  background: #f0f0f0;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
}

.board-arrow {
  font-size: 1.5rem;
  color: #bbb;
  flex-shrink: 0;
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
