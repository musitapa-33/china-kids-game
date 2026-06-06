<template>
  <div class="page-container">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-emoji">🗺️</div>
      <h2 class="hero-title">环游中国</h2>
      <p class="hero-desc">通过游戏认识中国的 34 个省级行政区，<br>了解各地特色风景和美食！</p>
      <div class="hero-btns">
        <el-button type="primary" size="large" round @click="$router.push('/map')">
          🗺️ 开始探索
        </el-button>
        <el-button type="success" size="large" round @click="$router.push('/quiz')">
          📝 挑战答题
        </el-button>
      </div>
    </div>

    <!-- 功能卡片 -->
    <el-row :gutter="12" style="max-width: 800px; margin: 0 auto; padding: 0 12px">
      <el-col :xs="12" :sm="6" v-for="card in featureCards" :key="card.path">
        <el-card
          shadow="hover"
          class="feature-card card-hover"
          @click="$router.push(card.path)"
        >
          <div style="text-align: center">
            <div style="font-size: 2em; margin-bottom: 4px">{{ card.icon }}</div>
            <h3 style="color: #1565c0; font-size: 0.95em">{{ card.title }}</h3>
            <p style="color: #999; font-size: 0.72em; margin-top: 4px">{{ card.desc }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 进度 -->
    <el-card shadow="never" style="max-width: 500px; margin: 24px auto; background: rgba(255,255,255,0.85)">
      <div style="text-align: center">
        <h3 style="color: #1565c0; margin-bottom: 12px">📊 学习进度</h3>
        <div style="font-size: 2em; font-weight: 700; color: #ff6f00">
          {{ gameStore.visitedCount }} / {{ gameStore.totalProvinces || 34 }}
        </div>
        <el-progress
          :percentage="progressPercent"
          :stroke-width="10"
          :color="progressColors"
          style="margin: 12px 0"
        />
        <p style="color: #888; font-size: 0.85em">
          ⭐ 累计得分：{{ gameStore.score }} 分
        </p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()

const featureCards = [
  { icon: '🗺️', title: '地图探索', desc: '点击省份了解详情', path: '/map' },
  { icon: '🧩', title: '拼图游戏', desc: '拼出完整中国', path: '/puzzle' },
  { icon: '📝', title: '知识问答', desc: '答题赚积分', path: '/quiz' },
  { icon: '🗺️', title: '探索地图', desc: '省份卡片+图片+打卡', path: '/map' },
  { icon: '🎴', title: '匹配游戏', desc: '翻牌配对吧', path: '/matching' },
  { icon: '📚', title: '互动课件', desc: '学习地理知识', path: '/courseware' },
  { icon: '🏆', title: '积分成就', desc: '查看你的收集', path: '/' },
  { icon: '🎯', title: '全部省份', desc: '34省全收录', path: '/map' },
]

const total = computed(() => gameStore.totalProvinces || 34)
const progressPercent = computed(() =>
  Math.round((gameStore.visitedCount / total.value) * 100)
)
const progressColors = [
  { color: '#f56c6c', percentage: 30 },
  { color: '#e6a23c', percentage: 60 },
  { color: '#67c23a', percentage: 80 },
  { color: '#409eff', percentage: 100 },
]

onMounted(() => {
  gameStore.loadProvinces()
})
</script>

<style scoped>
.page-container {
  padding: 20px 12px 60px;
  max-width: 900px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 32px 10px 20px;
}

.hero-emoji {
  font-size: 3.4em;
  margin-bottom: 8px;
  animation: floatY 3s ease-in-out infinite;
}

@keyframes floatY {
  0%, 100% { transform: translateY(0) rotate(-2deg); }
  50% { transform: translateY(-12px) rotate(2deg); }
}

.hero-title {
  font-size: 1.7em;
  background: linear-gradient(90deg, #1565c0, #00838f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 6px;
}

.hero-desc {
  color: #666;
  font-size: 1em;
  line-height: 1.7;
  margin-bottom: 16px;
}

.hero-btns {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.feature-card {
  margin-bottom: 12px;
  cursor: pointer;
  border-radius: 14px;
}
</style>
