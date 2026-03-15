import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NoteViewer from '../views/NoteViewer.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/notes/:boardId/:groupId/:chapterId',
      name: 'note',
      component: NoteViewer,
    },
  ],
})

export default router
