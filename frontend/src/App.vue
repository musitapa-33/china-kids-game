<template>
  <el-container style="min-height: 100vh">
    <!-- 顶部导航 -->
    <el-header style="padding: 0">
      <NavBar />
    </el-header>

    <!-- 主内容 -->
    <el-main style="padding: 0">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
  </el-container>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
