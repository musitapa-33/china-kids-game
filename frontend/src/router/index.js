import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue'), meta: { title: '首页' } },
  { path: '/map', name: 'MapExplore', component: () => import('@/views/MapExplore.vue'), meta: { title: '地图探索' } },
  { path: '/puzzle', name: 'PuzzleGame', component: () => import('@/views/PuzzleGame.vue'), meta: { title: '拼图游戏' } },
  { path: '/quiz', name: 'QuizGame', component: () => import('@/views/QuizGame.vue'), meta: { title: '知识问答' } },
  { path: '/gallery', name: 'Gallery', component: () => import('@/views/Gallery.vue'), meta: { title: '图片探索' } },
  { path: '/matching', name: 'MatchingGame', component: () => import('@/views/MatchingGame.vue'), meta: { title: '匹配游戏' } },
  { path: '/courseware', name: 'Courseware', component: () => import('@/views/Courseware.vue'), meta: { title: '互动课件' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
