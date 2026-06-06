<template>
  <div style="text-align: center; padding: 80px 20px">
    <div style="font-size: 48px; margin-bottom: 16px">🗺️</div>
    <h2 style="color: #1a3a5c; margin-bottom: 12px">图片探索已合并到地图模块</h2>
    <p style="color: #909399; margin-bottom: 24px">
      省份卡片图片 + 大图预览 + 左右导航功能已整合到「地图探索」页面
    </p>
    <el-button type="primary" size="large" round @click="$router.push('/map')">
      前往地图探索 🗺️
    </el-button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
onMounted(() => {
  router.replace('/map')
})
</script>
