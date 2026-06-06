<template>
  <div class="explore-page">
    <div class="page-header">
      <h1 class="title">🗺️ 环游中国</h1>
      <p class="subtitle">浏览省份美景，打卡收集，了解祖国的大好河山！</p>
    </div>

    <!-- 游玩进度 -->
    <div class="progress-bar-wrapper" v-if="!loading">
      <el-progress
        :percentage="visitProgress"
        :stroke-width="16"
        :text-inside="true"
        :format="progressFormat"
        color="#409eff"
      />
    </div>

    <!-- 区域筛选标签 -->
    <div class="region-tabs">
      <el-button
        v-for="region in regions"
        :key="region.id"
        :type="selectedRegion === region.id ? 'primary' : 'default'"
        :plain="selectedRegion !== region.id"
        round
        size="large"
        @click="filterByRegion(region.id)"
      >
        {{ region.emoji || '' }} {{ region.name }}
      </el-button>
    </div>

    <!-- 加载骨架屏 -->
    <div v-if="loading" class="card-grid">
      <div v-for="n in 12" :key="n" class="skeleton-card">
        <el-skeleton animated>
          <template #template>
            <el-skeleton-item variant="image" class="skeleton-img" />
            <div class="skeleton-body">
              <el-skeleton-item variant="h3" class="skeleton-title" />
              <el-skeleton-item variant="text" class="skeleton-tag" />
            </div>
          </template>
        </el-skeleton>
      </div>
    </div>

    <!-- 省份卡片网格 -->
    <div v-else-if="filteredProvinces.length > 0" class="card-grid">
      <div
        v-for="(province, index) in filteredProvinces"
        :key="province.id"
        class="card-wrapper"
        :style="{ animationDelay: `${index * 0.04}s` }"
      >
        <el-card
          :class="['province-card', { 'is-visited': gameStore.isVisited(province.id) }]"
          shadow="hover"
          @click="openDetail(province, index)"
        >
          <div class="card-image-wrap">
            <el-image
              :src="imageUrl(province.image)"
              fit="cover"
              lazy
              class="card-image"
            >
              <template #error>
                <div class="image-fallback">
                  <span class="fallback-emoji">{{ province.emoji || '🏛️' }}</span>
                </div>
              </template>
            </el-image>
          </div>
          <div class="card-body">
            <div class="card-title-row">
              <span class="card-emoji">{{ province.emoji }}</span>
              <span class="card-name">{{ province.name }}</span>
              <span v-if="gameStore.isVisited(province.id)" class="visited-badge">✅</span>
            </div>
            <div class="card-meta">
              <span class="card-abbr">{{ province.abbr }}</span>
              <span class="card-divider">|</span>
              <span class="card-capital">🏙️ {{ province.capital }}</span>
            </div>
            <div class="card-tags">
              <el-tag :type="tagType(province.region_name)" size="small" effect="light" round>
                {{ province.region_name }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 空状态 -->
    <el-empty v-else description="该区域没有省份数据" />

    <!-- 统一详情/预览弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentProvince ? `${currentProvince.emoji} ${currentProvince.name}` : ''"
      class="detail-dialog"
      width="800px"
      top="5vh"
      destroy-on-close
      :close-on-click-modal="true"
      @close="dialogVisible = false"
    >
      <template v-if="currentProvince">
        <div class="detail-layout">
          <!-- 左侧：大图 -->
          <div class="detail-image-area">
            <el-image
              :src="imageUrl(currentProvince.image)"
              fit="contain"
              class="detail-image"
            >
              <template #placeholder>
                <div class="detail-placeholder">🖼️ 加载中...</div>
              </template>
              <template #error>
                <div class="detail-placeholder large">{{ currentProvince.emoji || '🏛️' }}</div>
              </template>
            </el-image>
          </div>

          <!-- 右侧：信息 -->
          <div class="detail-info-panel">
            <div class="info-header">
              <h2 class="info-name">{{ currentProvince.name }}</h2>
              <el-tag :type="tagType(currentProvince.region_name)" size="small" round>
                {{ currentProvince.region_name }}
              </el-tag>
            </div>

            <el-descriptions :column="1" border class="info-details">
              <el-descriptions-item label="简称">{{ currentProvince.abbr || '—' }}</el-descriptions-item>
              <el-descriptions-item label="省会">{{ currentProvince.capital || '—' }}</el-descriptions-item>
              <el-descriptions-item label="特色">
                <template v-if="currentProvince.feature">
                  <el-tag
                    v-for="(feat, idx) in currentProvince.feature.split('、')"
                    :key="idx"
                    size="small"
                    class="feature-tag"
                    :type="['', 'success', 'warning', 'info'][idx % 4]"
                  >
                    {{ feat }}
                  </el-tag>
                </template>
                <span v-else>—</span>
              </el-descriptions-item>
            </el-descriptions>

            <div class="fun-fact-section" v-if="currentProvince.fun_fact">
              <h4 class="fun-fact-title">🎉 趣味小知识</h4>
              <p class="fun-fact-text">{{ currentProvince.fun_fact }}</p>
            </div>

            <!-- 打卡按钮 -->
            <div class="detail-actions">
              <el-button
                v-if="!gameStore.isVisited(currentProvince.id)"
                type="success"
                size="large"
                round
                @click="handleVisit(currentProvince.id)"
              >
                ✅ 标记已打卡
              </el-button>
              <el-button v-else type="success" size="large" round disabled>
                ✅ 已打卡
              </el-button>
            </div>

            <!-- 计数器 -->
            <div class="detail-counter">
              {{ currentIndex + 1 }} / {{ filteredProvinces.length }}
            </div>
          </div>
        </div>

        <!-- 左右导航 -->
        <div class="detail-nav">
          <el-button
            :disabled="currentIndex <= 0"
            circle
            size="large"
            @click="navigatePrev"
          >
            <el-icon><ArrowLeft /></el-icon>
          </el-button>
          <el-button
            :disabled="currentIndex >= filteredProvinces.length - 1"
            circle
            size="large"
            @click="navigateNext"
          >
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  ElButton, ElCard, ElSkeleton, ElSkeletonItem,
  ElDialog, ElImage, ElTag, ElDescriptions, ElDescriptionsItem,
  ElProgress, ElNotification, ElEmpty, ElIcon,
} from 'element-plus'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { getProvinceList, getRegionList } from '@/api'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()

// ---- 状态 ----
const provinces = ref([])
const regions = ref([])
const selectedRegion = ref(null)
const loading = ref(true)
const dialogVisible = ref(false)
const currentProvince = ref(null)
const currentIndex = ref(0)

// ---- 图片 ----
const MEDIA_BASE = '/media/'
const imageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${MEDIA_BASE}${path.replace(/^\/?media\//, '')}`
}

// ---- 区域标签颜色 ----
const tagType = (region) => {
  const map = {
    '华北': 'primary', '东北': 'success', '华东': 'warning',
    '华中': 'danger', '华南': 'info', '西南': 'info',
    '西北': 'primary', '港澳台': 'success',
  }
  return map[region] || 'info'
}

// ---- 进度 ----
const visitProgress = computed(() => {
  if (!provinces.value.length) return 0
  return Math.round((gameStore.visitedCount / provinces.value.length) * 100)
})
const progressFormat = (percentage) =>
  `已打卡 ${gameStore.visitedCount} / ${provinces.value.length} 个省份 (${percentage}%)`

// ---- 筛选 ----
const filteredProvinces = computed(() => {
  if (!selectedRegion.value) return provinces.value
  const region = regions.value.find(r => r.id === selectedRegion.value)
  if (!region) return provinces.value
  return provinces.value.filter(p => p.region_name === region.name)
})

const filterByRegion = (regionId) => {
  selectedRegion.value = selectedRegion.value === regionId ? null : regionId
  currentIndex.value = 0
}

// ---- 打开详情 ----
const openDetail = (province, index) => {
  currentProvince.value = province
  currentIndex.value = index
  dialogVisible.value = true
}

// ---- 导航 ----
const navigatePrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    currentProvince.value = filteredProvinces.value[currentIndex.value]
  }
}
const navigateNext = () => {
  if (currentIndex.value < filteredProvinces.value.length - 1) {
    currentIndex.value++
    currentProvince.value = filteredProvinces.value[currentIndex.value]
  }
}

// ---- 键盘导航 ----
const handleKeydown = (e) => {
  if (!dialogVisible.value) return
  if (e.key === 'ArrowLeft') navigatePrev()
  if (e.key === 'ArrowRight') navigateNext()
}

// ---- 打卡 ----
const handleVisit = (id) => {
  gameStore.visitProvince(id)
  ElNotification({
    title: '打卡成功 🎉',
    message: `你已成功打卡 ${currentProvince.value.name}！`,
    type: 'success',
    duration: 3000,
  })
}

// ---- 初始化 ----
onMounted(async () => {
  try {
    loading.value = true
    const [provinceData, regionData] = await Promise.all([
      getProvinceList(),
      getRegionList(),
    ])
    provinces.value = provinceData || []
    // 过滤掉没有关联省份的无效区域（如"特别行政区"）
    const validRegions = (regionData || []).filter(r =>
      provinces.value.some(p => p.region_name === r.name)
    )
    regions.value = [
      { id: null, name: '全部', emoji: '🗺️' },
      ...validRegions,
    ]
    gameStore.loadProvinces(provinces.value.map(p => p.id))
  } catch (err) {
    ElNotification({
      title: '加载失败',
      message: '获取省份数据失败，请检查网络后重试',
      type: 'error',
      duration: 5000,
    })
    console.error('Failed to load provinces:', err)
  } finally {
    loading.value = false
  }
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.explore-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px 60px;
  min-height: 100vh;
}
.page-header {
  text-align: center;
  margin-bottom: 24px;
}
.title {
  font-size: 36px;
  font-weight: 800;
  color: #1a3a5c;
  margin: 0 0 8px;
  letter-spacing: 2px;
}
.subtitle {
  font-size: 15px;
  color: #6b7b8d;
  margin: 0;
}

/* 进度条 */
.progress-bar-wrapper {
  margin-bottom: 24px;
  padding: 0 4px;
}

/* 区域筛选 */
.region-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 28px;
}
.region-tabs .el-button {
  font-size: 14px;
  padding: 8px 18px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.region-tabs .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(64, 158, 255, 0.25);
}

/* 卡片网格 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
@media (max-width: 768px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
}
@media (max-width: 480px) {
  .card-grid { grid-template-columns: 1fr; }
}

.card-wrapper {
  animation: fadeInUp 0.5s ease both;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 省份卡片 */
.province-card {
  border-radius: 14px;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 2px solid transparent;
}
.province-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 10px 28px rgba(64, 158, 255, 0.2);
}
.province-card.is-visited {
  border-color: #67c23a;
}
.province-card :deep(.el-card__body) { padding: 0; }

/* 卡片图片 */
.card-image-wrap {
  width: 100%;
  height: 160px;
  overflow: hidden;
  background: #f0f2f5;
}
.card-image {
  width: 100%;
  height: 100%;
  display: block;
  transition: transform 0.4s ease;
}
.province-card:hover .card-image {
  transform: scale(1.08);
}
.image-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 160px;
  background: #f7f8fa;
}
.fallback-emoji {
  font-size: 48px;
}

/* 卡片内容 */
.card-body {
  padding: 12px 14px 14px;
}
.card-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}
.card-emoji { font-size: 20px; }
.card-name {
  font-size: 17px;
  font-weight: 700;
  color: #1a3a5c;
}
.visited-badge { margin-left: auto; font-size: 14px; }
.card-meta {
  display: flex;
  gap: 6px;
  align-items: center;
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}
.card-divider { color: #ddd; }
.card-tags { display: flex; gap: 4px; flex-wrap: wrap; }

/* 骨架屏 */
.skeleton-card {
  border-radius: 14px;
  overflow: hidden;
  background: #fff;
}
.skeleton-img { width: 100%; height: 160px; }
.skeleton-body { padding: 12px 14px 14px; }
.skeleton-title { height: 18px; width: 60%; margin-bottom: 8px; }
.skeleton-tag { height: 14px; width: 40%; }

/* 详情弹窗 */
.detail-dialog { border-radius: 16px; overflow: hidden; }
.detail-dialog :deep(.el-dialog__header) {
  text-align: center;
  padding: 20px 20px 0;
  font-size: 20px;
  font-weight: 600;
}
.detail-dialog :deep(.el-dialog__body) {
  padding: 16px 24px 12px;
}
.detail-layout {
  display: flex;
  gap: 24px;
}
@media (max-width: 640px) {
  .detail-layout { flex-direction: column; }
}
.detail-image-area {
  flex: 1;
  min-width: 0;
}
.detail-image {
  width: 100%;
  max-height: 420px;
  border-radius: 12px;
  overflow: hidden;
}
.detail-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 320px;
  background: #f7f8fa;
  color: #b0b8c4;
  font-size: 20px;
  border-radius: 12px;
}
.detail-placeholder.large { font-size: 72px; }

.detail-info-panel {
  width: 260px;
  flex-shrink: 0;
}
@media (max-width: 640px) {
  .detail-info-panel { width: 100%; }
}
.info-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}
.info-name {
  font-size: 22px;
  font-weight: 700;
  color: #1a3a5c;
  margin: 0;
}
.info-details { margin-bottom: 16px; }
.feature-tag { margin: 2px 4px 2px 0; }

.fun-fact-section {
  padding: 12px 14px;
  background: linear-gradient(135deg, #ecf5ff, #f0f9eb);
  border-radius: 10px;
  margin-bottom: 16px;
}
.fun-fact-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a3a5c;
  margin: 0 0 6px;
}
.fun-fact-text {
  font-size: 13px;
  color: #303133;
  line-height: 1.7;
  margin: 0;
}

.detail-actions { text-align: center; margin-bottom: 12px; }
.detail-counter { text-align: center; font-size: 13px; color: #a0aab4; }

/* 导航按钮 */
.detail-nav {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}
</style>
