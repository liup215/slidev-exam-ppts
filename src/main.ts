import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import Home from './App.vue'
import NoteViewer from './components/NoteViewer.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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

const app = createApp({
  template: '<router-view></router-view>'
})
app.use(router)
app.mount('#app')
