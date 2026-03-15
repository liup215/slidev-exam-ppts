import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import NoteViewer from './components/NoteViewer.vue'

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

const app = createApp({
  template: `<div>
    <div style="background: #4ecdc4; color: white; padding: 10px; text-align: center; font-weight: bold;">
      ✅ Router-view 根组件已加载
    </div>
    <router-view></router-view>
  </div>`
})
app.use(router)
app.mount('#app')
