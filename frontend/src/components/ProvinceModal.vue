<template>
  <el-dialog
    :model-value="visible"
    title="省份详情"
    width="600px"
    top="5vh"
    destroy-on-close
    class="province-modal"
    @close="handleClose"
    @update:model-value="$emit('update:visible', $event)"
  >
    <!-- 加载态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton animated :loading="loading" :count="3" />
    </div>

    <!-- 错误态 -->
    <div v-else-if="error" class="error-state">
      <p>😵 加载失败，请稍后重试</p>
      <el-button type="primary" size="small" @click="fetchDetail">重新加载</el-button>
    </div>

    <!-- 省份详情 -->
    <template v-else-if="detail">
      <div class="modal-body">
        <div class="detail-emoji">{{ detail.emoji || '🏛️' }}</div>
        <h2 class="detail-name">{{ detail.name }}</h2>
        <el-tag class="detail-region-tag" size="small" type="info">
          {{ detail.region_name || detail.region || '' }}
        </el-tag>

        <!-- 省份图片 -->
        <div class="detail-image-wrapper" v-if="detail.image">
          <el-image
            :src="imageUrl(detail.image)"
            fit="cover"
            class="detail-image"
          >
            <template #error>
              <div class="image-fallback">
                <span>🖼️</span>
                <span>图片加载失败</span>
              </div>
            </template>
          </el-image>
        </div>

        <!-- 基本信息 -->
        <el-descriptions :column="2" border class="detail-info">
          <el-descriptions-item label="简称">
            {{ detail.abbr || '—' }}
          </el-descriptions-item>
          <el-descriptions-item label="省会">
            {{ detail.capital || '—' }}
          </el-descriptions-item>
          <el-descriptions-item label="特色" :span="2">
            <template v-if="detail.feature?.length">
              <el-tag
                v-for="(feat, idx) in detail.feature"
                :key="idx"
                size="small"
                class="feature-tag"
                :type="tagType(idx)"
              >
                {{ feat }}
              </el-tag>
            </template>
            <span v-else>—</span>
          </el-descriptions-item>
        </el-descriptions>

        <!-- 趣味小知识 -->
        <div class="fun-fact-section" v-if="detail.fun_fact">
          <h3 class="fun-fact-title">🎉 趣味小知识</h3>
          <p class="fun-fact-text">{{ detail.fun_fact }}</p>
        </div>

        <!-- 操作按钮 -->
        <div class="modal-actions">
          <el-button
            v-if="!gameStore.isVisited(detail.id)"
            type="success"
            size="large"
            round
            :loading="visiting"
            @click="markVisited"
          >
            ✅ 标记为已打卡
          </el-button>
          <el-button
            v-else
            type="success"
            size="large"
            round
            disabled
          >
            ✅ 已打卡
          </el-button>

          <el-button
            size="large"
            round
            @click="handleClose"
          >
            关闭
          </el-button>
        </div>
      </div>
    </template>

    <!-- 空数据态 -->
    <div v-else-if="!loading && !detail" class="empty-state">
      <p>暂无省份数据</p>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import {
  ElDialog,
  ElButton,
  ElSkeleton,
  ElImage,
  ElTag,
  ElDescriptions,
  ElDescriptionsItem,
  ElNotification,
} from 'element-plus'
import { getProvinceDetail } from '@/api'
import { useGameStore } from '@/stores/game'

const props = defineProps({
  provinceId: {
    type: [Number, String],
    default: null,
  },
  visible: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'update:visible', 'visited'])

const gameStore = useGameStore()

// 图片基路径（数据库已包含 images/ 前缀，只需拼接 /media/）
const MEDIA_BASE = '/media/'
const imageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  // 移除可能的重复前缀
  const cleanPath = path.replace(/^\/?media\//, '')
  return `${MEDIA_BASE}${cleanPath}`
}

// 状态
const detail = ref(null)
const loading = ref(false)
const error = ref(false)
const visiting = ref(false)

// 特色标签颜色轮换
const TAG_COLORS = ['', 'success', 'warning', 'info', 'danger']
const tagType = (index) => TAG_COLORS[index % TAG_COLORS.length]

// 获取省份详情
const fetchDetail = async () => {
  if (!props.provinceId) return

  loading.value = true
  error.value = false

  try {
    const data = await getProvinceDetail(props.provinceId)
    detail.value = data
  } catch (err) {
    console.error('Failed to fetch province detail:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

// 标记已打卡
const markVisited = async () => {
  if (!detail.value?.id) return

  visiting.value = true
  try {
    await gameStore.visitProvince(detail.value.id)
    ElNotification({
      title: '打卡成功 🎉',
      message: `你已成功打卡 ${detail.value.name}！`,
      type: 'success',
      duration: 3000,
    })
    emit('visited', detail.value.id)
  } catch (err) {
    ElNotification({
      title: '打卡失败',
      message: '请稍后重试',
      type: 'error',
      duration: 3000,
    })
    console.error('Failed to mark visited:', err)
  } finally {
    visiting.value = false
  }
}

// 关闭弹窗
const handleClose = () => {
  emit('close')
  emit('update:visible', false)
}

// 监听 provinceId 变化重新加载
watch(
  () => props.provinceId,
  (newId) => {
    if (newId) {
      detail.value = null
      fetchDetail()
    }
  }
)

onMounted(() => {
  if (props.provinceId) {
    fetchDetail()
  }
})
</script>

<style scoped>
.loading-state {
  padding: 40px 20px;
}

.error-state {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.error-state p {
  font-size: 18px;
  margin-bottom: 16px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
  font-size: 16px;
}

.modal-body {
  text-align: center;
}

.detail-emoji {
  font-size: 64px;
  line-height: 1;
  margin-bottom: 8px;
}

.detail-name {
  font-size: 28px;
  font-weight: 700;
  color: #1a3a5c;
  margin: 0 0 6px;
}

.detail-region-tag {
  margin-bottom: 20px;
}

.detail-image-wrapper {
  margin: 16px 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.detail-image {
  width: 100%;
  height: 260px;
  display: block;
}

.image-fallback {
  width: 100%;
  height: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #f5f7fa;
  color: #909399;
  font-size: 16px;
}

.detail-info {
  text-align: left;
  margin-top: 16px;
}

.feature-tag {
  margin: 2px 4px 2px 0;
  cursor: default;
}

.fun-fact-section {
  margin-top: 20px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #ecf5ff 0%, #f0f9eb 100%);
  border-radius: 12px;
  text-align: left;
}

.fun-fact-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a3a5c;
  margin: 0 0 8px;
}

.fun-fact-text {
  font-size: 15px;
  color: #303133;
  line-height: 1.8;
  margin: 0;
}

.modal-actions {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  gap: 12px;
}
</style>
