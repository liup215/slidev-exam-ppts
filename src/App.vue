<template>
  <div class="container">
    <!-- 调试提示：确认 App.vue 已加载 -->
    <div style="background: #ff6b6b; color: white; padding: 10px; text-align: center; font-weight: bold;">
      ✅ App.vue 组件已加载
    </div>
    <header>
      <h1>📚 考纲幻灯片</h1>
      <p class="subtitle">在线考试考纲幻灯片展示</p>
    </header>

    <!-- Breadcrumb -->
    <nav class="breadcrumb" aria-label="当前位置">
      <button class="breadcrumb-item" @click="goHome">首页</button>
      <template v-if="currentBoard">
        <span class="breadcrumb-sep">›</span>
        <button
          class="breadcrumb-item"
          :class="{ active: !currentGroup }"
          @click="goToBoard"
        >{{ currentBoard.name }}</button>
      </template>
      <template v-if="currentGroup">
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item active">{{ currentGroup.name }}</span>
      </template>
    </nav>

    <main>
      <!-- Level 1: Exam board cards -->
      <Transition name="fade" mode="out-in">
        <div v-if="!currentBoard" key="boards" class="board-grid">
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

        <!-- Level 2: Group cards (module / level) -->
        <div v-else-if="!currentGroup" key="groups" class="group-grid">
          <button
            v-for="group in currentBoard.groups"
            :key="group.id"
            class="group-card"
            @click="selectGroup(group)"
          >
            <span class="group-icon">{{ group.icon }}</span>
            <div class="group-info">
              <h3>{{ group.name }}</h3>
              <p v-if="group.description">{{ group.description }}</p>
              <span class="group-meta">{{ group.chapters.length }} 章节</span>
            </div>
            <span class="group-arrow">›</span>
          </button>
        </div>

        <!-- Level 3: Chapter list -->
        <div v-else key="chapters">
          <div class="chapters-grid">
            <div
              v-for="chapter in currentGroup.chapters"
              :key="chapter.id"
              class="chapter-card-wrapper"
            >
              <a
                :href="chapter.url"
                class="chapter-card"
                :class="{ 'has-ppt': chapter.url && chapter.url !== '#' }"
              >
                <div class="chapter-number">Ch.{{ chapter.number }}</div>
                <div class="chapter-content">
                  <h4>{{ chapter.title }}</h4>
                  <p>{{ chapter.subtitle }}</p>
                </div>
              </a>
              <button
                v-if="chapterHasNote(chapter)"
                class="note-btn"
                @click="openNote(chapter)"
                title="查看笔记"
              >
                📄 笔记
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </main>

    <footer>
      <p>基于 <a href="https://sli.dev/" target="_blank">Slidev</a> 构建</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface Chapter {
  id: string
  number: number
  title: string
  subtitle: string
  url: string
}

interface Group {
  id: string
  name: string
  icon: string
  description?: string
  chapters: Chapter[]
}

interface ExamBoard {
  id: string
  name: string
  icon: string
  description?: string
  groups: Group[]
}

const base = import.meta.env.BASE_URL

const examBoards: ExamBoard[] = [
  {
    id: 'bio-competition',
    name: '生物竞赛',
    icon: '🏆',
    description: '全国及国际生物学竞赛备考',
    groups: [
      {
        id: 'bio-comp-cell',
        name: '细胞生物学',
        icon: '🔬',
        description: '细胞结构、细胞分裂与细胞信号',
        chapters: [
          { id: 'bc-cell-1', number: 1, title: '细胞结构与功能', subtitle: 'Cell Structure & Function', url: '#' },
          { id: 'bc-cell-2', number: 2, title: '细胞分裂', subtitle: 'Cell Division', url: '#' },
          { id: 'bc-cell-3', number: 3, title: '细胞信号传导', subtitle: 'Cell Signaling', url: '#' },
          { id: 'bc-cell-7', number: 7, title: '基因表达调控', subtitle: 'Gene Expression Control', url: `${base}slides/bio-competition/molecular-biology-of-the-cell/chapter7/` },
        ],
      },
      {
        id: 'bio-comp-biochem',
        name: '生物化学',
        icon: '⚗️',
        description: '生物大分子、代谢与酶学',
        chapters: [
          { id: 'bc-bc-1', number: 1, title: '生物分子概论', subtitle: 'Biomolecules Overview', url: '#' },
          { id: 'bc-bc-2', number: 2, title: '酶学', subtitle: 'Enzymology', url: '#' },
          { id: 'bc-bc-3', number: 3, title: '细胞呼吸与代谢', subtitle: 'Cellular Respiration & Metabolism', url: '#' },
        ],
      },
      {
        id: 'bio-comp-genetics',
        name: '遗传学',
        icon: '🧬',
        description: '孟德尔遗传、分子遗传学与基因组学',
        chapters: [
          { id: 'bc-gen-1', number: 1, title: '孟德尔遗传', subtitle: 'Mendelian Genetics', url: '#' },
          { id: 'bc-gen-2', number: 2, title: '分子遗传学', subtitle: 'Molecular Genetics', url: '#' },
          { id: 'bc-gen-3', number: 3, title: '基因工程', subtitle: 'Genetic Engineering', url: '#' },
        ],
      },
      {
        id: 'bio-comp-ecology',
        name: '生态学',
        icon: '🌿',
        description: '种群、群落与生态系统',
        chapters: [
          { id: 'bc-eco-1', number: 1, title: '种群生态学', subtitle: 'Population Ecology', url: '#' },
          { id: 'bc-eco-2', number: 2, title: '群落与生态系统', subtitle: 'Communities & Ecosystems', url: '#' },
        ],
      },
      {
        id: 'bio-comp-animal',
        name: '动物生理学',
        icon: '🐾',
        description: '动物各系统生理机制',
        chapters: [
          { id: 'bc-ap-1', number: 1, title: '神经与感官', subtitle: 'Nervous System & Senses', url: '#' },
          { id: 'bc-ap-2', number: 2, title: '循环与免疫', subtitle: 'Circulation & Immunity', url: '#' },
          { id: 'bc-ap-3', number: 3, title: '内分泌系统', subtitle: 'Endocrine System', url: '#' },
        ],
      },
      {
        id: 'bio-comp-plant',
        name: '植物生理学',
        icon: '🌱',
        description: '植物生长、光合与激素调节',
        chapters: [
          { id: 'bc-pp-1', number: 1, title: '光合作用', subtitle: 'Photosynthesis', url: '#' },
          { id: 'bc-pp-2', number: 2, title: '植物激素', subtitle: 'Plant Hormones', url: '#' },
        ],
      },
      {
        id: 'bio-comp-micro',
        name: '微生物学',
        icon: '🦠',
        description: '细菌、病毒与微生物代谢',
        chapters: [
          { id: 'bc-micro-1', number: 1, title: '微生物多样性', subtitle: 'Microbial Diversity', url: '#' },
          { id: 'bc-micro-2', number: 2, title: '病毒学', subtitle: 'Virology', url: '#' },
        ],
      },
      {
        id: 'bio-comp-biotech',
        name: '生物技术',
        icon: '🔧',
        description: 'DNA 技术、克隆与生物信息学',
        chapters: [
          { id: 'bc-bt-1', number: 1, title: 'DNA 技术', subtitle: 'DNA Technology', url: '#' },
          { id: 'bc-bt-2', number: 2, title: '克隆与干细胞', subtitle: 'Cloning & Stem Cells', url: '#' },
        ],
      },
    ],
  },
  {
    id: 'cie-9700',
    name: 'A-Level Biology (9700)',
    icon: '🧬',
    description: 'Cambridge International AS & A Level Biology',
    groups: [
      {
        id: 'cie-9700-as',
        name: 'AS Level',
        icon: '📘',
        description: 'Chapters 1 – 10',
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
          { id: 'cie-9700-ch3', number: 3, title: '酶', subtitle: 'Enzymes', url: '#' },
          { id: 'cie-9700-ch4', number: 4, title: '细胞膜与运输', subtitle: 'Cell Membranes & Transport', url: '#' },
          { id: 'cie-9700-ch5', number: 5, title: '有丝分裂', subtitle: 'The Mitotic Cell Cycle', url: '#' },
          { id: 'cie-9700-ch6', number: 6, title: '核酸与蛋白质合成', subtitle: 'Nucleic Acids & Protein Synthesis', url: '#' },
          { id: 'cie-9700-ch7', number: 7, title: '运输', subtitle: 'Transport in Plants & Animals', url: '#' },
          { id: 'cie-9700-ch8', number: 8, title: '气体交换与呼吸', subtitle: 'Gas Exchange & Respiration', url: '#' },
          { id: 'cie-9700-ch9', number: 9, title: '感染与免疫', subtitle: 'Infectious Disease & Immunity', url: '#' },
          { id: 'cie-9700-ch10', number: 10, title: '遗传', subtitle: 'Inheritance', url: '#' },
        ],
      },
      {
        id: 'cie-9700-a2',
        name: 'A2 Level',
        icon: '📗',
        description: 'Chapters 11 – 19',
        chapters: [
          { id: 'cie-9700-ch11', number: 11, title: '光合作用', subtitle: 'Photosynthesis', url: '#' },
          { id: 'cie-9700-ch12', number: 12, title: '有氧呼吸与无氧呼吸', subtitle: 'Respiration', url: '#' },
          { id: 'cie-9700-ch13', number: 13, title: '调控与稳态', subtitle: 'Homeostasis', url: '#' },
          { id: 'cie-9700-ch14', number: 14, title: '协调', subtitle: 'Coordination', url: '#' },
          { id: 'cie-9700-ch15', number: 15, title: '自然选择与进化', subtitle: 'Inheritance & Evolution', url: '#' },
          { id: 'cie-9700-ch16', number: 16, title: '分类与多样性', subtitle: 'Classification & Biodiversity', url: '#' },
          { id: 'cie-9700-ch17', number: 17, title: '生态系统与人类活动', subtitle: 'Ecosystems & Human Impact', url: '#' },
          { id: 'cie-9700-ch18', number: 18, title: '遗传技术', subtitle: 'Genetic Technology', url: '#' },
        ],
      },
    ],
  },
]

const currentBoard = ref<ExamBoard | null>(null)
const currentGroup = ref<Group | null>(null)

// Cache for note existence checks
const noteExistenceCache = ref<Record<string, boolean>>({})

// Pre-defined list of available notes (built at build time)
const availableNotes = [
  '/notes/cie-9700/chapter-1.md',
  '/notes/cie-9700/chapter-2.md',
  '/notes/cie-9700/chapter-3.md',
  '/notes/cie-9700/chapter-4.md',
  '/notes/cie-9700/chapter-5.md',
]

function chapterHasNote(chapter: Chapter): boolean {
  if (!currentBoard.value || !currentGroup.value) return false
  
  const boardId = currentBoard.value.id
  const groupId = currentGroup.value.id
  const chapterId = chapter.id
  
  // Check if note exists at path: /notes/{board}/{group}/{chapter}.md
  const notePath = `/notes/${boardId}/${groupId}/${chapterId}.md`
  const altPath = `/notes/${boardId}/${chapterId}.md`
  
  // Also check for chapter-{number}.md pattern (e.g., chapter-1.md)
  const chapterNum = chapterId.match(/ch(\d+)$/i)?.[1]
  const chapterPath = chapterNum ? `/notes/${boardId}/chapter-${chapterNum}.md` : null
  
  return availableNotes.includes(notePath) || 
         availableNotes.includes(altPath) || 
         (chapterPath && availableNotes.includes(chapterPath))
}

function openNote(chapter: Chapter) {
  if (!currentBoard.value || !currentGroup.value) return
  
  const boardId = currentBoard.value.id
  const groupId = currentGroup.value.id
  const chapterId = chapter.id
  
  // Navigate to note viewer using Vue Router
  router.push(`/notes/${boardId}/${groupId}/${chapterId}`)
}

function selectBoard(board: ExamBoard) {
  currentBoard.value = board
  currentGroup.value = null
}

function selectGroup(group: Group) {
  currentGroup.value = group
}

function goHome() {
  currentBoard.value = null
  currentGroup.value = null
}

function goToBoard() {
  currentGroup.value = null
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
  margin-bottom: 1.5rem;
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

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-bottom: 2rem;
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

/* Board grid */
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

/* Group grid */
.group-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.group-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border: none;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  text-align: left;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.group-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.group-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.group-info {
  flex: 1;
}

.group-info h3 {
  font-size: 1.05rem;
  color: #1a73e8;
  margin-bottom: 0.25rem;
}

.group-info p {
  font-size: 0.82rem;
  color: #777;
  margin-bottom: 0.35rem;
}

.group-meta {
  font-size: 0.78rem;
  color: #888;
  background: #f0f0f0;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
}

.group-arrow {
  font-size: 1.2rem;
  color: #ccc;
  flex-shrink: 0;
}

/* Chapter grid */
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

/* Chapter card wrapper with note button */
.chapter-card-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.note-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  background: #f0f7ff;
  border: 1px solid #1a73e8;
  border-radius: 8px;
  color: #1a73e8;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.15s ease;
  align-self: flex-start;
}

.note-btn:hover {
  background: #1a73e8;
  color: white;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(12px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-12px);
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

@media (max-width: 600px) {
  header h1 {
    font-size: 1.8rem;
  }

  .board-card {
    padding: 1.1rem 1.25rem;
  }

  .board-icon {
    font-size: 2rem;
  }

  .board-info h2 {
    font-size: 1.1rem;
  }

  .group-grid {
    grid-template-columns: 1fr;
  }

  .chapters-grid {
    grid-template-columns: 1fr;
  }
}
</style>
