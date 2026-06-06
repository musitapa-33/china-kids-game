<template>
  <div class="puzzle-game">
    <!-- 顶部标题区域 -->
    <div class="game-header">
      <div class="title-row">
        <h1 class="game-title">🧩 环游中国</h1>
        <div class="game-subtitle">拼图挑战</div>
      </div>
      <div class="timer-display">
        <span class="timer-icon">⏱️</span>
        <span class="timer-text">{{ formattedTime }}</span>
      </div>
    </div>

    <!-- 控制区域 -->
    <div class="game-controls">
      <div class="control-group">
        <label class="control-label">难度选择</label>
        <el-select
          v-model="difficulty"
          :disabled="gameStarted && !isComplete"
          size="large"
          class="difficulty-select"
        >
          <el-option label="简单 (18个省份)" value="easy" />
          <el-option label="中等 (26个省份)" value="medium" />
          <el-option label="困难 (全部34个)" value="hard" />
        </el-select>
      </div>
      <el-button
        :type="gameStarted ? 'warning' : 'primary'"
        size="large"
        @click="startGame"
      >
        {{ gameStarted ? '🔄 重新开始' : '🚀 开始游戏' }}
      </el-button>
    </div>

    <!-- 提示消息 -->
    <transition name="hint-fade">
      <div v-if="hintMessage" class="hint-banner" :class="hintType">
        <span class="hint-icon">{{ hintType === 'success' ? '✅' : '💡' }}</span>
        <span>{{ hintMessage }}</span>
      </div>
    </transition>

    <!-- 游戏状态信息 -->
    <div v-if="gameStarted && !isComplete" class="game-stats">
      <el-tag type="info" effect="plain">
        已匹配: {{ placedCount }} / {{ slots.length }}
      </el-tag>
      <el-tag type="danger" effect="plain" v-if="wrongAttempts > 0">
        错误: {{ wrongAttempts }} 次
      </el-tag>
    </div>

    <!-- 拼图插槽网格 -->
    <div v-if="gameStarted" class="slots-container">
      <div class="section-label">🗺️ 将省份名称拖到对应的位置</div>
      <div class="slots-grid">
        <div
          v-for="(slot, index) in slots"
          :key="slot.id"
          class="slot-card"
          :class="{
            filled: slot.placed,
            shaking: shakingIndex === index,
            'drag-over': dragOverIndex === index
          }"
          @dragover.prevent="onDragOver($event, index)"
          @dragleave="onDragLeave(index)"
          @drop.prevent="onDrop($event, index)"
        >
          <div class="slot-emoji">{{ slot.emoji }}</div>
          <div class="slot-divider"></div>
          <div v-if="slot.placed" class="slot-name-placed">
            <span>{{ slot.name }}</span>
            <span class="checkmark">✓</span>
          </div>
          <div v-else class="slot-placeholder">
            <span class="placeholder-text">?</span>
            <span class="placeholder-hint">拖到这里</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 待选拼块托盘 -->
    <div v-if="gameStarted && trayItems.length > 0" class="tray-container">
      <div class="section-label">🧩 可拖动的拼块</div>
      <div class="tray">
        <div
          v-for="item in trayItems"
          :key="item.id"
          class="tray-tile"
          :class="{ dragging: draggedItem?.id === item.id }"
          draggable="true"
          @dragstart="onDragStart($event, item)"
          @dragend="onDragEnd"
        >
          <span class="tile-emoji">{{ item.emoji }}</span>
          <span class="tile-name">{{ item.name }}</span>
        </div>
      </div>
    </div>

    <!-- 游戏空状态 -->
    <div v-if="gameStarted && trayItems.length === 0 && placedCount === slots.length" class="all-placed-message">
      <div class="all-placed-icon">🎉</div>
      <div>全部匹配完成！</div>
    </div>

    <!-- 开始前引导 -->
    <div v-if="!gameStarted" class="welcome-section">
      <div class="welcome-card">
        <div class="welcome-icon">🧩</div>
        <h2>欢迎来到拼图挑战！</h2>
        <p>选择难度后点击"开始游戏"，将省份名称拖到对应的插槽中。</p>
        <div class="rules">
          <div class="rule-item">
            <span class="rule-icon">🎯</span>
            <span>拖拽拼块到对应的位置</span>
          </div>
          <div class="rule-item">
            <span class="rule-icon">✅</span>
            <span>匹配正确会锁定并显示绿色标记</span>
          </div>
          <div class="rule-item">
            <span class="rule-icon">💡</span>
            <span>匹配错误会弹出提示</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 进度区域 -->
    <div v-if="gameStarted" class="progress-section">
      <div class="progress-info">
        <span class="progress-label">完成进度</span>
        <span class="progress-percent">{{ progress }}%</span>
      </div>
      <el-progress
        :percentage="progress"
        :stroke-width="16"
        :color="progressColors"
        :format="() => `${placedCount} / ${slots.length}`"
      />
    </div>

    <!-- 完成弹窗 -->
    <el-dialog
      v-model="showDialog"
      title="🎉 恭喜完成！"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="420px"
      class="congrats-dialog"
      top="15vh"
    >
      <div class="dialog-content">
        <div class="dialog-emoji">🏆</div>
        <h2 class="dialog-title">太棒了！</h2>
        <p class="dialog-subtitle">你成功完成了拼图挑战！</p>
        <div class="result-stats">
          <div class="stat-item">
            <span class="stat-icon">⏱️</span>
            <div class="stat-body">
              <span class="stat-label">用时</span>
              <span class="stat-value">{{ formattedTime }}</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">❌</span>
            <div class="stat-body">
              <span class="stat-label">错误次数</span>
              <span class="stat-value">{{ wrongAttempts }} 次</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">⭐</span>
            <div class="stat-body">
              <span class="stat-label">评价</span>
              <span class="stat-value star-rating">{{ starRating }}</span>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button type="primary" size="large" @click="startGame" class="play-again-btn">
          🔄 再玩一次
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElButton, ElSelect, ElOption, ElDialog, ElProgress, ElTag } from 'element-plus'
import { getPuzzleData } from '@/api'

// ==================== 响应式状态 ====================

const allProvinces = ref([])
const slots = ref([])
const trayItems = ref([])
const difficulty = ref('easy')
const gameStarted = ref(false)
const showDialog = ref(false)

// 拖拽状态
const draggedItem = ref(null)
const dragOverIndex = ref(-1)

// 计时与统计
const timer = ref(0)
const wrongAttempts = ref(0)
let timerInterval = null

// 动画状态
const shakingIndex = ref(-1)
const hintMessage = ref('')
const hintType = ref('info')

// ==================== 计算属性 ====================

const placedCount = computed(() => {
  return slots.value.filter(s => s.placed).length
})

const progress = computed(() => {
  if (slots.value.length === 0) return 0
  return Math.round((placedCount.value / slots.value.length) * 100)
})

const isComplete = computed(() => {
  return slots.value.length > 0 && placedCount.value === slots.value.length
})

const formattedTime = computed(() => {
  const minutes = Math.floor(timer.value / 60)
  const seconds = timer.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

const starRating = computed(() => {
  const ratio = wrongAttempts.value / slots.value.length
  if (ratio <= 0.15) return '⭐⭐⭐ 完美！'
  if (ratio <= 0.4) return '⭐⭐ 不错哦！'
  return '⭐ 继续加油！'
})

const provinceCount = computed(() => {
  switch (difficulty.value) {
    case 'easy': return 18
    case 'medium': return 26
    case 'hard': return 34
    default: return 18
  }
})

const progressColors = [
  { color: '#409eff', percentage: 40 },
  { color: '#67c23a', percentage: 70 },
  { color: '#e6a23c', percentage: 90 },
  { color: '#f56c6c', percentage: 100 }
]

// ==================== 工具函数 ====================

function shuffleArray(arr) {
  const shuffled = [...arr]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

// ==================== 核心方法 ====================

async function startGame() {
  stopTimer()
  timer.value = 0
  wrongAttempts.value = 0
  showDialog.value = false
  hintMessage.value = ''
  shakingIndex.value = -1
  draggedItem.value = null
  dragOverIndex.value = -1

  // 如果还没有加载数据，则加载
  if (allProvinces.value.length === 0) {
    try {
      const data = await getPuzzleData()
      allProvinces.value = data
    } catch (e) {
      console.error('加载拼图数据失败:', e)
      hintMessage.value = '加载数据失败，请刷新页面重试'
      hintType.value = 'error'
      return
    }
  }

  const count = provinceCount.value
  const shuffledAll = shuffleArray(allProvinces.value)
  const selected = shuffledAll.slice(0, count)

  // 为每个省份创建插槽对象
  slots.value = shuffleArray(selected.map(p => ({
    id: p.id,
    name: p.name,
    emoji: p.emoji,
    placed: false
  })))

  // 创建托盘对象（不同的随机顺序）
  trayItems.value = shuffleArray(selected.map(p => ({
    id: p.id,
    name: p.name,
    emoji: p.emoji
  })))

  gameStarted.value = true
  startTimer()
}

function onDragStart(event, item) {
  draggedItem.value = item
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', item.id)
  // 设置拖拽时的光标样式
  event.target.style.opacity = '0.6'
}

function onDragEnd(event) {
  draggedItem.value = null
  dragOverIndex.value = -1
  if (event.target) {
    event.target.style.opacity = '1'
  }
}

function onDragOver(event, index) {
  event.dataTransfer.dropEffect = 'move'
  dragOverIndex.value = index
}

function onDragLeave(index) {
  if (dragOverIndex.value === index) {
    dragOverIndex.value = -1
  }
}

function onDrop(event, slotIndex) {
  dragOverIndex.value = -1

  if (!draggedItem.value) return

  const slot = slots.value[slotIndex]
  if (slot.placed) return

  const draggedId = draggedItem.value.id

  if (draggedId === slot.id) {
    // 正确匹配
    slot.placed = true
    // 从托盘中移除
    trayItems.value = trayItems.value.filter(item => item.id !== draggedId)

    showHint('🎉 正确！' + slot.name, 'success')

    // 检查是否全部完成
    if (isComplete.value) {
      stopTimer()
      setTimeout(() => {
        showDialog.value = true
      }, 600)
    }
  } else {
    // 错误匹配
    wrongAttempts.value++

    // 晃动动画
    shakingIndex.value = slotIndex
    const correctItem = slots.value.find(s => s.id === draggedId)
    const hint = correctItem ? `"${draggedItem.value.name}" 属于 ${correctItem.emoji} 哦` : '再想想这个属于哪里？'
    showHint('💡 ' + hint, 'error')

    setTimeout(() => {
      shakingIndex.value = -1
    }, 600)
  }
}

function showHint(message, type) {
  hintMessage.value = message
  hintType.value = type
  setTimeout(() => {
    hintMessage.value = ''
  }, 2500)
}

// ==================== 计时器 ====================

function startTimer() {
  stopTimer()
  timerInterval = setInterval(() => {
    timer.value++
  }, 1000)
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

// ==================== 生命周期 ====================

onMounted(async () => {
  try {
    const data = await getPuzzleData()
    allProvinces.value = data
  } catch (e) {
    console.error('加载拼图数据失败:', e)
  }
})

onUnmounted(() => {
  stopTimer()
})
</script>

<style scoped>
/* ==================== 整体布局 ==================== */

.puzzle-game {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 20px 40px;
  min-height: calc(100vh - 80px);
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* ==================== 顶部标题 ==================== */

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 3px solid #e8f5e9;
}

.title-row {
  display: flex;
  flex-direction: column;
}

.game-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a5276;
  margin: 0;
  line-height: 1.3;
}

.game-subtitle {
  font-size: 15px;
  color: #7fb3d8;
  margin-top: 2px;
}

.timer-display {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #e3f2fd, #e8f5e9);
  padding: 10px 20px;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.timer-icon {
  font-size: 20px;
}

.timer-text {
  font-size: 24px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #1565c0;
  letter-spacing: 2px;
}

/* ==================== 控制区域 ==================== */

.game-controls {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.control-label {
  font-size: 14px;
  font-weight: 600;
  color: #555;
}

.difficulty-select {
  width: 200px;
}

/* ==================== 提示横幅 ==================== */

.hint-banner {
  text-align: center;
  padding: 12px 20px;
  border-radius: 12px;
  margin-bottom: 16px;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.hint-banner.success {
  background: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #a5d6a7;
}

.hint-banner.error {
  background: #fff3e0;
  color: #e65100;
  border: 1px solid #ffcc80;
}

.hint-icon {
  font-size: 18px;
}

.hint-fade-enter-active,
.hint-fade-leave-active {
  transition: all 0.35s ease;
}

.hint-fade-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}

.hint-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ==================== 游戏状态标签 ==================== */

.game-stats {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
}

/* ==================== 部分标题 ==================== */

.section-label {
  font-size: 15px;
  font-weight: 600;
  color: #1a5276;
  margin-bottom: 12px;
  text-align: center;
}

/* ==================== 插槽网格 ==================== */

.slots-container {
  margin-bottom: 28px;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.slot-card {
  background: #f5f9fc;
  border: 2px dashed #b0d4e3;
  border-radius: 16px;
  padding: 14px 8px;
  text-align: center;
  cursor: default;
  transition: all 0.25s ease;
  min-height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.slot-card.drag-over {
  border-color: #42a5f5;
  background: #e3f2fd;
  transform: scale(1.04);
  box-shadow: 0 4px 16px rgba(66, 133, 244, 0.25);
}

.slot-card.filled {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  border: 2px solid #66bb6a;
  cursor: default;
}

.slot-card.shaking {
  animation: shake 0.5s ease-in-out;
  border-color: #ef5350;
  background: #ffebee;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  15% { transform: translateX(-8px); }
  30% { transform: translateX(8px); }
  45% { transform: translateX(-6px); }
  60% { transform: translateX(6px); }
  75% { transform: translateX(-3px); }
  90% { transform: translateX(3px); }
}

.slot-emoji {
  font-size: 30px;
  line-height: 1.2;
  margin-bottom: 6px;
}

.slot-divider {
  width: 40px;
  height: 2px;
  background: #d0e3f0;
  border-radius: 1px;
  margin: 4px auto;
}

.slot-card.filled .slot-divider {
  background: #81c784;
}

.slot-name-placed {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 700;
  color: #1b5e20;
}

.checkmark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: #4caf50;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 700;
  animation: pop-in 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes pop-in {
  0% { transform: scale(0); }
  100% { transform: scale(1); }
}

.slot-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.placeholder-text {
  font-size: 22px;
  font-weight: 700;
  color: #b0bec5;
}

.placeholder-hint {
  font-size: 11px;
  color: #b0bec5;
}

/* ==================== 托盘 ==================== */

.tray-container {
  margin-bottom: 24px;
}

.tray {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  padding: 16px;
  background: #f0f7fb;
  border-radius: 16px;
  min-height: 70px;
  border: 2px solid #dceef7;
}

.tray-tile {
  display: flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, #ffffff 0%, #f5faff 100%);
  border: 2px solid #90caf9;
  border-radius: 12px;
  padding: 8px 16px;
  cursor: grab;
  user-select: none;
  font-size: 14px;
  font-weight: 600;
  color: #1565c0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(66, 133, 244, 0.12);
}

.tray-tile:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 6px 16px rgba(66, 133, 244, 0.25);
  border-color: #42a5f5;
}

.tray-tile:active {
  cursor: grabbing;
}

.tray-tile.dragging {
  opacity: 0.4;
  transform: scale(0.95);
}

.tile-emoji {
  font-size: 18px;
}

.tile-name {
  font-size: 14px;
}

/* ==================== 全匹配消息 ==================== */

.all-placed-message {
  text-align: center;
  padding: 40px 20px;
  font-size: 20px;
  font-weight: 700;
  color: #2e7d32;
  background: #e8f5e9;
  border-radius: 16px;
  margin-bottom: 24px;
}

.all-placed-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

/* ==================== 欢迎区域 ==================== */

.welcome-section {
  margin: 20px 0 32px;
}

.welcome-card {
  text-align: center;
  background: linear-gradient(135deg, #e3f2fd 0%, #e8f5e9 100%);
  border-radius: 20px;
  padding: 40px 28px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.welcome-icon {
  font-size: 56px;
  margin-bottom: 16px;
}

.welcome-card h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a5276;
  margin: 0 0 8px;
}

.welcome-card p {
  font-size: 15px;
  color: #546e7a;
  margin: 0 0 24px;
}

.rules {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 360px;
  margin: 0 auto;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  font-size: 14px;
  color: #37474f;
}

.rule-icon {
  font-size: 20px;
  flex-shrink: 0;
}

/* ==================== 进度区域 ==================== */

.progress-section {
  margin-top: 8px;
  padding: 16px 20px;
  background: #f8fbfd;
  border-radius: 14px;
  border: 1px solid #e3eef5;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 14px;
  font-weight: 600;
  color: #546e7a;
}

.progress-percent {
  font-size: 16px;
  font-weight: 700;
  color: #1565c0;
}

/* ==================== 完成弹窗 ==================== */

.congrats-dialog :deep(.el-dialog__header) {
  text-align: center;
  font-size: 22px;
  padding-bottom: 0;
}

.congrats-dialog :deep(.el-dialog__body) {
  padding-top: 12px;
}

.dialog-content {
  text-align: center;
}

.dialog-emoji {
  font-size: 64px;
  margin-bottom: 8px;
  animation: bounce 1s ease infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.dialog-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a5276;
  margin: 0 0 4px;
}

.dialog-subtitle {
  font-size: 15px;
  color: #78909c;
  margin: 0 0 24px;
}

.result-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 280px;
  margin: 0 auto 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 18px;
  background: #f5f9fc;
  border-radius: 12px;
  text-align: left;
}

.stat-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.stat-body {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 12px;
  color: #90a4ae;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #37474f;
}

.star-rating {
  font-size: 16px;
  letter-spacing: 2px;
}

.play-again-btn {
  width: 100%;
}

/* ==================== 响应式 ==================== */

@media (max-width: 640px) {
  .puzzle-game {
    padding: 16px 12px 32px;
  }

  .game-header {
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .title-row {
    align-items: center;
  }

  .game-title {
    font-size: 22px;
  }

  .game-controls {
    flex-direction: column;
    align-items: center;
  }

  .difficulty-select {
    width: 100%;
  }

  .slots-grid {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: 8px;
  }

  .slot-card {
    min-height: 80px;
    padding: 10px 6px;
  }

  .slot-emoji {
    font-size: 24px;
  }

  .tray-tile {
    padding: 6px 12px;
    font-size: 13px;
  }

  .timer-text {
    font-size: 20px;
  }
}
</style>
