import { createRouter, createWebHashHistory } from 'vue-router'
import App from '../App.vue'
import NoteViewer from '../components/NoteViewer.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: App
  },
  {
    path: '/notes/:board/:group/:chapter',
    name: 'NoteViewer',
    component: NoteViewer,
    props: true
  }
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL || '/'),
  routes
})

export default router
