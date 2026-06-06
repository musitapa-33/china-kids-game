<template>
  <div class="nav-bar">
    <div class="nav-inner">
      <router-link to="/" class="nav-logo">
        <span style="font-size: 1.3em">🗺️</span>
        <span class="logo-text">环游中国</span>
        <small class="logo-sub">— 儿童地理</small>
      </router-link>

      <div class="nav-links">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          {{ item.icon }} {{ item.label }}
        </router-link>
      </div>

      <div class="nav-score">
        <el-tag type="warning" effect="dark" round>
          ⭐ {{ gameStore.score }} 分
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useGameStore } from '@/stores/game'

const route = useRoute()
const gameStore = useGameStore()

const navItems = [
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/map', label: '探索', icon: '🗺️' },
  { path: '/puzzle', label: '拼图', icon: '🧩' },
  { path: '/quiz', label: '答题', icon: '📝' },
  { path: '/matching', label: '匹配', icon: '🎴' },
  { path: '/courseware', label: '课件', icon: '📚' },
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<style scoped>
.nav-bar {
  background: linear-gradient(135deg, #1565c0, #0288d1, #00acc1);
  color: #fff;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 8px 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
  color: #fff;
  white-space: nowrap;
}

.logo-text {
  font-size: 1.1em;
  font-weight: 700;
}

.logo-sub {
  font-size: 0.55em;
  opacity: 0.8;
  font-weight: 400;
}

.nav-links {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  flex: 1;
  justify-content: center;
}

.nav-link {
  padding: 5px 10px;
  border: 2px solid rgba(255, 255, 255, 0.45);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  text-decoration: none;
  font-size: 0.78em;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-link:hover,
.nav-link.active {
  background: #fff;
  color: #1565c0;
  border-color: #fff;
  font-weight: 700;
}

.nav-score {
  flex-shrink: 0;
}
</style>
