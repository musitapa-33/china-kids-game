<template>
  <div class="matching-game">
    <!-- 页面头部 -->
    <div class="game-header">
      <h1>
        <span class="header-icon">🧩</span>
        记忆配对
      </h1>
      <p class="subtitle">翻开卡片，找到省份与答案的匹配对</p>
    </div>

    <!-- 配置面板（游戏开始前） -->
    <div v-if="!gameStarted" class="config-panel">
      <div class="config-section">
        <h3 class="config-title">选择模式</h3>
        <div class="mode-buttons">
          <button
            v-for="m in modes"
            :key="m.value"
            class="config-btn"
            :class="{ active: selectedMode === m.value }"
            @click="selectedMode = m.value"
          >
            <span class="config-btn-icon">{{ m.icon }}</span>
            <span class="config-btn-label">{{ m.label }}</span>
          </button>
        </div>
      </div>

      <div class="config-section">
        <h3 class="config-title">选择难度</h3>
        <div class="difficulty-buttons">
          <button
            v-for="d in difficulties"
            :key="d.value"
            class="config-btn"
            :class="{ active: selectedDifficulty === d.value }"
            @click="selectedDifficulty = d.value"
          >
            <span class="config-btn-label">{{ d.label }}</span>
            <span class="config-btn-desc">{{ d.pairs }}对 / {{ d.pairs * 2 }}张卡片</span>
          </button>
        </div>
      </div>

      <button
        class="start-btn"
        :disabled="loading"
        @click="startGame"
      >
        <span v-if="loading" class="loading-spinner"></span>
        <span v-else>🚀</span>
        <span>{{ loading ? '加载中...' : '开始游戏' }}</span>
      </button>
    </div>

    <!-- 游戏状态栏 -->
    <div v-if="gameStarted" class="stats-bar">
      <div class="stat-item">
        <span class="stat-label">已配对</span>
        <span class="stat-value">{{ matchedPairs }} / {{ totalPairs }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">尝试</span>
        <span class="stat-value">{{ attempts }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">用时</span>
        <span class="stat-value timer-value">{{ formattedTime }}</span>
      </div>
      <button class="reset-btn" @click="resetGame">重新开始</button>
    </div>

    <!-- 进度条 -->
    <div v-if="gameStarted" class="progress-wrapper">
      <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      <span>⚠️</span>
      <span>{{ error }}</span>
      <button @click="resetGame">重试</button>
    </div>

    <!-- 卡片网格 -->
    <div v-if="gameStarted && cards.length > 0" class="card-grid" :class="'cols-' + gridCols">
      <div
        v-for="card in cards"
        :key="card.id"
        class="card-wrapper"
        :class="{
          flipped: card.isFlipped || card.isMatched,
          matched: card.isMatched,
          'no-click': isChecking
        }"
        @click="flipCard(card)"
      >
        <div class="card-inner">
          <!-- 卡背 -->
          <div class="card-back">
            <div class="card-back-pattern">
              <svg viewBox="0 0 120 160" class="card-back-svg">
                <rect x="4" y="4" width="112" height="152" rx="12" fill="#2b5a8c" />
                <rect x="8" y="8" width="104" height="144" rx="10" fill="none" stroke="#4a8fd4" stroke-width="1.5" />
                <circle cx="60" cy="70" r="28" fill="none" stroke="#6ab0f0" stroke-width="1.5" />
                <path d="M60 42 Q75 55 80 70 Q75 85 60 98 Q45 85 40 70 Q45 55 60 42Z" fill="#6ab0f0" opacity="0.3" />
                <circle cx="60" cy="70" r="8" fill="#6ab0f0" opacity="0.5" />
                <line x1="35" y1="70" x2="85" y2="70" stroke="#6ab0f0" stroke-width="1" opacity="0.5" />
                <line x1="60" y1="45" x2="60" y2="95" stroke="#6ab0f0" stroke-width="1" opacity="0.5" />
                <text x="60" y="130" text-anchor="middle" fill="#6ab0f0" font-size="14" opacity="0.8">环游中国</text>
              </svg>
            </div>
          </div>
          <!-- 卡面 -->
          <div class="card-front" :class="card.type === 'name' ? 'front-name' : 'front-match'">
            <div class="card-front-content">
              <span class="card-badge">{{ card.type === 'name' ? '省份' : '答案' }}</span>
              <span class="card-text">{{ card.text }}</span>
              <span class="card-hint">{{ card.type === 'name' ? '点击配对' : '匹配省份' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="gameStarted && cards.length === 0 && !loading && !error" class="empty-state">
      <p>暂无卡片数据，请重试</p>
      <button class="reset-btn" @click="resetGame">返回设置</button>
    </div>

    <!-- 胜利弹窗 -->
    <Teleport to="body">
      <div v-if="gameFinished" class="victory-overlay" @click.self="resetGame">
        <div class="victory-card">
          <div class="victory-fireworks">🎉</div>
          <h2 class="victory-title">恭喜通关！</h2>
          <p class="victory-subtitle">
            你成功匹配了所有 {{ totalPairs }} 对卡片！
          </p>
          <div class="victory-stars">
            <span v-for="i in starRating" :key="i" class="star">⭐</span>
          </div>
          <div class="victory-details">
            <div class="detail-item">
              <span class="detail-icon">🔄</span>
              <span class="detail-text">尝试 {{ attempts }} 次</span>
            </div>
            <div class="detail-item">
              <span class="detail-icon">⏱️</span>
              <span class="detail-text">用时 {{ formattedTime }}</span>
            </div>
          </div>
          <button class="play-again-btn" @click="resetGame">
            🎮 再来一局
          </button>
        </div>

        <!-- 庆祝粒子 -->
        <div class="confetti-container">
          <div
            v-for="i in 30"
            :key="i"
            class="confetti-piece"
            :style="{
              '--x': Math.random() * 100 + '%',
              '--delay': Math.random() * 3 + 's',
              '--color': confettiColors[i % confettiColors.length],
              '--rotation': Math.random() * 720 + 'deg',
              '--size': (Math.random() * 8 + 4) + 'px'
            }"
          ></div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getMatchingData } from '@/api'

// ---------- 常量 ----------
const modes = [
  { value: 'capital', label: '省会配对', icon: '🏙️', desc: '省份 → 省会' },
  { value: 'abbr',    label: '简称配对', icon: '📝', desc: '省份 → 简称' },
  { value: 'feature', label: '特色配对', icon: '🏔️', desc: '省份 → 特色' }
]

const difficulties = [
  { value: 'easy',   label: '简单', pairs: 6  },
  { value: 'medium', label: '中等', pairs: 8  },
  { value: 'hard',   label: '困难', pairs: 12 }
]

const confettiColors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#ff6be6', '#845ef7']

// ---------- 状态 ----------
const selectedMode = ref('capital')
const selectedDifficulty = ref('easy')
const loading = ref(false)
const error = ref('')
const gameStarted = ref(false)
const gameFinished = ref(false)

const cards = ref([])
const flippedCards = ref([])
const matchedPairs = ref(0)
const attempts = ref(0)
const isChecking = ref(false)

const timerSeconds = ref(0)
let timerInterval = null

// ---------- 计算属性 ----------
const totalPairs = computed(() => {
  const d = difficulties.find(d => d.value === selectedDifficulty.value)
  return d ? d.pairs : 6
})

const gridCols = computed(() => {
  const total = totalPairs.value * 2
  if (total <= 12) return 4
  if (total <= 16) return 4
  return 6
})

const progressPercent = computed(() => {
  if (totalPairs.value === 0) return 0
  return Math.round((matchedPairs.value / totalPairs.value) * 100)
})

const formattedTime = computed(() => {
  const m = Math.floor(timerSeconds.value / 60)
  const s = timerSeconds.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

const starRating = computed(() => {
  // 3 星: 尝试次数 <= 总对数 * 1.8
  // 2 星: 尝试次数 <= 总对数 * 3
  // 1 星: 其他
  const ratio = attempts.value / totalPairs.value
  if (ratio <= 1.8) return 3
  if (ratio <= 3) return 2
  return 1
})

// ---------- 工具函数 ----------
function shuffleArray(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

// ---------- 游戏逻辑 ----------
async function startGame() {
  loading.value = true
  error.value = ''
  gameStarted.value = false
  gameFinished.value = false
  cards.value = []
  flippedCards.value = []
  matchedPairs.value = 0
  attempts.value = 0
  isChecking.value = false
  timerSeconds.value = 0

  try {
    const response = await getMatchingData(selectedMode.value)
    const rawData = response.data || []

    if (!rawData || rawData.length === 0) {
      error.value = '未获取到配对数据，请重试'
      loading.value = false
      return
    }

    // 选择指定数量的配对
    const numPairs = totalPairs.value
    const selectedItems = shuffleArray(rawData).slice(0, numPairs)

    // 生成卡片对：每条数据生成"省份名"和"匹配值"两张卡
    let cardId = 0
    const newCards = []
    for (const item of selectedItems) {
      newCards.push({
        id: cardId++,
        pairId: item.name,
        text: item.name,
        type: 'name',
        isFlipped: false,
        isMatched: false
      })
      newCards.push({
        id: cardId++,
        pairId: item.name,
        text: item.match,
        type: 'match',
        isFlipped: false,
        isMatched: false
      })
    }

    cards.value = shuffleArray(newCards)
    gameStarted.value = true
    startTimer()
  } catch (e) {
    console.error('获取配对数据失败:', e)
    error.value = '加载失败，请检查网络后重试'
  } finally {
    loading.value = false
  }
}

function flipCard(card) {
  // 禁止点击条件：已匹配 / 已翻开 / 游戏结束 / 正在检查配对
  if (card.isMatched || card.isFlipped || gameFinished.value || isChecking.value) return

  // 禁止连续点击同一张卡
  if (flippedCards.value.length === 1 && flippedCards.value[0].id === card.id) return

  card.isFlipped = true
  flippedCards.value.push(card)

  if (flippedCards.value.length === 2) {
    attempts.value++
    isChecking.value = true

    const [card1, card2] = flippedCards.value

    // 检查是否匹配：pairId 相同
    if (card1.pairId === card2.pairId && card1.type !== card2.type) {
      // 匹配成功
      setTimeout(() => {
        card1.isMatched = true
        card2.isMatched = true
        matchedPairs.value++
        flippedCards.value = []
        isChecking.value = false

        // 检查是否全部匹配完成
        if (matchedPairs.value === totalPairs.value) {
          gameFinished.value = true
          stopTimer()
        }
      }, 400)
    } else {
      // 不匹配，翻回
      setTimeout(() => {
        card1.isFlipped = false
        card2.isFlipped = false
        flippedCards.value = []
        isChecking.value = false
      }, 900)
    }
  }
}

function resetGame() {
  stopTimer()
  gameStarted.value = false
  gameFinished.value = false
  cards.value = []
  flippedCards.value = []
  matchedPairs.value = 0
  attempts.value = 0
  isChecking.value = false
  timerSeconds.value = 0
  error.value = ''
}

// ---------- 计时器 ----------
function startTimer() {
  stopTimer()
  timerSeconds.value = 0
  timerInterval = setInterval(() => {
    timerSeconds.value++
  }, 1000)
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

// ---------- 生命周期 ----------
onUnmounted(() => {
  stopTimer()
})
</script>

<style scoped>
/* ========== 基础布局 ========== */
.matching-game {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 16px 48px;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* ========== 头部 ========== */
.game-header {
  text-align: center;
  margin-bottom: 32px;
}

.game-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1a3a5c;
  margin: 0 0 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.header-icon {
  font-size: 36px;
  line-height: 1;
}

.subtitle {
  color: #6b7b8d;
  font-size: 15px;
  margin: 0;
}

/* ========== 配置面板 ========== */
.config-panel {
  background: linear-gradient(135deg, #f8faff 0%, #eef3fb 100%);
  border-radius: 20px;
  padding: 32px 28px;
  box-shadow: 0 4px 20px rgba(43, 90, 140, 0.08);
  max-width: 600px;
  margin: 0 auto;
}

.config-section {
  margin-bottom: 24px;
}

.config-title {
  font-size: 16px;
  font-weight: 600;
  color: #2b5a8c;
  margin: 0 0 12px;
}

.mode-buttons,
.difficulty-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.config-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 20px;
  border: 2px solid #dce5f0;
  border-radius: 14px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  flex: 1;
  min-width: 100px;
}

.config-btn:hover {
  border-color: #4a8fd4;
  background: #f0f7ff;
  transform: translateY(-1px);
}

.config-btn.active {
  border-color: #2b5a8c;
  background: #e5f0ff;
  box-shadow: 0 2px 8px rgba(43, 90, 140, 0.15);
}

.config-btn-icon {
  font-size: 28px;
  line-height: 1;
}

.config-btn-label {
  font-size: 15px;
  font-weight: 600;
  color: #1a3a5c;
}

.config-btn-desc {
  font-size: 12px;
  color: #8a9aa8;
}

.difficulty-buttons .config-btn {
  flex-direction: row;
  justify-content: center;
  gap: 8px;
}

/* 开始按钮 */
.start-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 16px rgba(46, 125, 50, 0.3);
}

.start-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(46, 125, 50, 0.4);
}

.start-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 22px;
  height: 22px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========== 状态栏 ========== */
.stats-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  padding: 16px 24px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-label {
  font-size: 13px;
  color: #8a9aa8;
  font-weight: 500;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #1a3a5c;
}

.timer-value {
  font-variant-numeric: tabular-nums;
  color: #e65100;
}

.reset-btn {
  padding: 8px 20px;
  border: 2px solid #dce5f0;
  border-radius: 10px;
  background: #fff;
  color: #2b5a8c;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-btn:hover {
  border-color: #4a8fd4;
  background: #f0f7ff;
}

/* ========== 进度条 ========== */
.progress-wrapper {
  height: 10px;
  background: #e8edf4;
  border-radius: 10px;
  margin-bottom: 24px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  border-radius: 10px;
  transition: width 0.4s ease;
}

/* ========== 错误提示 ========== */
.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  background: #fff0f0;
  border-radius: 12px;
  color: #c62828;
  margin-bottom: 16px;
}

.error-message button {
  margin-left: 8px;
  padding: 4px 14px;
  border: 1px solid #c62828;
  border-radius: 8px;
  background: transparent;
  color: #c62828;
  font-family: inherit;
  cursor: pointer;
}

/* ========== 卡片网格 ========== */
.card-grid {
  display: grid;
  gap: 12px;
  max-width: 960px;
  margin: 0 auto;
}

.card-grid.cols-4 {
  grid-template-columns: repeat(4, 1fr);
}

.card-grid.cols-6 {
  grid-template-columns: repeat(6, 1fr);
}

/* ========== 卡片 3D 翻转 ========== */
.card-wrapper {
  aspect-ratio: 3 / 4;
  perspective: 1000px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.card-wrapper.no-click {
  cursor: default;
  pointer-events: none;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}

.card-wrapper.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-back,
.card-front {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 14px;
  overflow: hidden;
}

/* -- 卡背 -- */
.card-back {
  background: linear-gradient(145deg, #2b5a8c, #1a3a5c);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(26, 58, 92, 0.2);
  border: 2px solid #3a6a9c;
}

.card-back-pattern {
  width: 90%;
  height: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-back-svg {
  width: 100%;
  height: 100%;
}

/* -- 卡面 -- */
.card-front {
  transform: rotateY(180deg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.front-name {
  background: linear-gradient(145deg, #fff3e0, #ffe0b2);
}

.front-match {
  background: linear-gradient(145deg, #e3f2fd, #bbdefb);
}

.card-front-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  text-align: center;
  width: 100%;
  height: 100%;
}

.card-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: 20px;
  letter-spacing: 1px;
}

.front-name .card-badge {
  background: #ffcc80;
  color: #e65100;
}

.front-match .card-badge {
  background: #90caf9;
  color: #0d47a1;
}

.card-text {
  font-size: 20px;
  font-weight: 700;
  color: #1a3a5c;
  line-height: 1.3;
  word-break: break-word;
  max-width: 100%;
}

.card-hint {
  font-size: 11px;
  color: #8a9aa8;
  opacity: 0.7;
}

/* 匹配完成状态 */
.card-wrapper.matched .card-front {
  border-color: #4caf50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.3), 0 4px 12px rgba(76, 175, 80, 0.2);
}

.card-wrapper.matched .card-front .card-text {
  color: #2e7d32;
}

.card-wrapper.matched .card-front .card-badge {
  background: #a5d6a7;
  color: #1b5e20;
}

/* 卡片交互反馈 */
.card-wrapper:not(.flipped):not(.matched):not(.no-click):hover .card-inner {
  transform: scale(1.04);
  transition: transform 0.2s ease;
}

.card-wrapper:not(.flipped):not(.matched):not(.no-click):active .card-inner {
  transform: scale(0.97);
}

/* ========== 空状态 ========== */
.empty-state {
  text-align: center;
  padding: 48px 16px;
  color: #8a9aa8;
}

/* ========== 胜利弹窗 ========== */
.victory-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.victory-card {
  background: #fff;
  border-radius: 24px;
  padding: 40px 36px;
  text-align: center;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  animation: scaleIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  z-index: 10;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.7);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.victory-fireworks {
  font-size: 64px;
  line-height: 1;
  margin-bottom: 8px;
  animation: bounce 1s ease infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.victory-title {
  font-size: 28px;
  font-weight: 800;
  color: #1a3a5c;
  margin: 0 0 8px;
}

.victory-subtitle {
  color: #6b7b8d;
  font-size: 15px;
  margin: 0 0 16px;
}

.victory-stars {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
  gap: 4px;
}

.star {
  font-size: 32px;
  animation: popIn 0.3s ease both;
}

.star:nth-child(1) { animation-delay: 0.4s; }
.star:nth-child(2) { animation-delay: 0.6s; }
.star:nth-child(3) { animation-delay: 0.8s; }

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0) rotate(-30deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.victory-details {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4a5a6a;
  font-size: 14px;
  font-weight: 500;
}

.detail-icon {
  font-size: 20px;
  line-height: 1;
}

.play-again-btn {
  padding: 14px 36px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #2b5a8c, #1a3a5c);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(43, 90, 140, 0.3);
}

.play-again-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(43, 90, 140, 0.4);
}

/* ========== 庆祝粒子 ========== */
.confetti-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 5;
}

.confetti-piece {
  position: absolute;
  top: -10px;
  left: var(--x);
  width: var(--size);
  height: var(--size);
  background: var(--color);
  border-radius: 2px;
  animation: confettiFall 3s var(--delay) ease-in infinite;
  opacity: 0.8;
}

@keyframes confettiFall {
  0% {
    transform: translateY(-10px) rotate(0deg);
    opacity: 0.8;
  }
  100% {
    transform: translateY(100vh) rotate(var(--rotation));
    opacity: 0;
  }
}

/* ========== 响应式 ========== */
@media (max-width: 700px) {
  .card-grid.cols-6 {
    grid-template-columns: repeat(4, 1fr);
  }

  .card-grid {
    gap: 8px;
  }

  .stats-bar {
    gap: 16px;
    padding: 12px 16px;
  }

  .config-btn {
    padding: 10px 14px;
    min-width: 80px;
  }

  .card-text {
    font-size: 16px;
  }

  .victory-card {
    padding: 28px 20px;
  }
}

@media (max-width: 480px) {
  .card-grid.cols-4,
  .card-grid.cols-6 {
    grid-template-columns: repeat(3, 1fr);
  }

  .card-grid {
    gap: 6px;
  }

  .game-header h1 {
    font-size: 24px;
  }

  .card-text {
    font-size: 14px;
  }

  .card-badge {
    font-size: 9px;
    padding: 1px 8px;
  }

  .card-hint {
    display: none;
  }

  .victory-details {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
