<template>
  <div class="quiz-container">
    <!-- 顶部栏 -->
    <div class="quiz-header">
      <el-button text @click="goBack" class="back-btn">← 返回</el-button>
      <div class="score-display">⭐ {{ gameStore.score }} 分</div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-view">
      <div class="loading-icon">🧠</div>
      <p class="loading-text">正在准备题目...</p>
    </div>

    <!-- 游戏进行中 -->
    <template v-else-if="!gameOver">
      <!-- 进度条 -->
      <div class="progress-section">
        <div class="progress-label">
          第 <strong>{{ currentIndex + 1 }}</strong> / {{ totalQuestions }} 题
        </div>
        <el-progress
          :percentage="progressPercent"
          :stroke-width="14"
          :color="progressColors"
          :show-text="false"
        />
      </div>

      <!-- 题目卡片 -->
      <transition name="slide-fade" mode="out-in">
        <el-card v-if="currentQuestion" :key="currentQuestion.id" class="question-card" shadow="always">
          <!-- 题目标签 + 省份 -->
          <div class="question-meta">
            <el-tag :type="tagType" effect="dark" round size="small">
              {{ questionTypeLabel }}
            </el-tag>
            <span class="province-tag">📍 {{ currentQuestion.province_name }}</span>
          </div>

          <!-- 题目文本 -->
          <h3 class="question-text">{{ currentQuestion.question_text }}</h3>

          <!-- 选项按钮 -->
          <div class="options-grid">
            <button
              v-for="(opt, idx) in options"
              :key="opt.key"
              class="option-btn"
              :class="getOptionClass(opt.key)"
              @click="selectOption(opt.key)"
              :disabled="answered"
            >
              <span class="option-letter">{{ optionLetters[idx] }}</span>
              <span class="option-text">{{ opt.text }}</span>
            </button>
          </div>

          <!-- 答题反馈 -->
          <transition name="fade">
            <div v-if="answered" class="feedback-area">
              <div class="feedback-header">
                <span :class="['feedback-icon', isCorrect ? 'icon-correct' : 'icon-wrong']">
                  {{ isCorrect ? '✅' : '❌' }}
                </span>
                <span class="feedback-title">
                  {{ isCorrect ? '回答正确！' : '回答错误' }}
                </span>
                <span v-if="isCorrect && streak >= 3" class="streak-bonus">
                  🔥 连击 ×{{ streak }} 额外 +5！
                </span>
              </div>
              <div v-if="!isCorrect" class="correct-answer-text">
                正确答案：<strong>{{ correctAnswerText }}</strong>
              </div>
              <div class="feedback-points">
                {{ isCorrect ? '+10 分' : '+0 分' }}{{ isCorrect && streak >= 3 ? ' + 5 奖励分' : '' }}
              </div>
              <el-button
                type="primary"
                round
                size="large"
                class="next-btn"
                @click="nextQuestion"
              >
                {{ currentIndex < totalQuestions - 1 ? '下一题 →' : '查看结果 🏆' }}
              </el-button>
            </div>
          </transition>
        </el-card>
      </transition>
    </template>

    <!-- 结果界面 -->
    <template v-else>
      <div class="result-section">
        <el-card class="result-card" shadow="always">
          <div class="result-emoji">{{ resultEmoji }}</div>
          <h2 class="result-title">答题完成！</h2>

          <!-- 星星评级 -->
          <div class="stars-row">
            <span
              v-for="i in 5"
              :key="i"
              :class="['star', i <= starRating ? 'star-active' : 'star-inactive']"
            >★</span>
          </div>
          <div class="star-label">{{ starLabel }}</div>

          <!-- 统计数据 -->
          <div class="result-stats">
            <div class="stat-item">
              <div class="stat-value stat-correct">{{ correctCount }}</div>
              <div class="stat-label">正确</div>
            </div>
            <div class="stat-divider" />
            <div class="stat-item">
              <div class="stat-value stat-wrong">{{ totalQuestions - correctCount }}</div>
              <div class="stat-label">错误</div>
            </div>
            <div class="stat-divider" />
            <div class="stat-item">
              <div class="stat-value stat-streak">{{ bestStreak }}</div>
              <div class="stat-label">最高连击</div>
            </div>
            <div class="stat-divider" />
            <div class="stat-item">
              <div class="stat-value stat-rate">{{ accuracyPercent }}%</div>
              <div class="stat-label">正确率</div>
            </div>
          </div>

          <!-- 本局得分 -->
          <div class="result-score-section">
            <span class="result-score-label">本局得分</span>
            <span class="result-score-value">+{{ roundScore }}</span>
          </div>

          <!-- 累计总分 -->
          <div class="result-total">
            ⭐ 累计总分：{{ gameStore.score }}
          </div>

          <!-- 操作按钮 -->
          <div class="result-actions">
            <el-button type="primary" size="large" round class="retry-btn" @click="restartGame">
              🔄 再来一次
            </el-button>
            <el-button text round class="home-btn" @click="goBack">
              🏠 返回首页
            </el-button>
          </div>
        </el-card>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElTag, ElProgress, ElCard, ElMessage } from 'element-plus'
import { getQuizQuestions } from '@/api'
import { useGameStore } from '@/stores/game'

const router = useRouter()
const gameStore = useGameStore()

const optionLetters = ['A', 'B', 'C', 'D']

// 题目状态
const questions = ref([])
const loading = ref(true)
const currentIndex = ref(0)
const answered = ref(false)
const selectedOption = ref(null)
const gameOver = ref(false)

// 统计
const correctCount = ref(0)
const streak = ref(0)
const bestStreak = ref(0)
const roundScore = ref(0)

const totalQuestions = computed(() => questions.value.length)

const currentQuestion = computed(() => {
  if (currentIndex.value < questions.value.length) {
    return questions.value[currentIndex.value]
  }
  return null
})

const progressPercent = computed(() => {
  if (totalQuestions.value === 0) return 0
  return ((currentIndex.value) / totalQuestions.value) * 100
})

const progressColors = [
  { color: '#409eff', percentage: 30 },
  { color: '#67c23a', percentage: 60 },
  { color: '#e6a23c', percentage: 80 },
  { color: '#f56c6c', percentage: 100 },
]

// 选项列表
const options = computed(() => {
  const q = currentQuestion.value
  if (!q) return []
  return [
    { key: 'A', text: q.option_a },
    { key: 'B', text: q.option_b },
    { key: 'C', text: q.option_c },
    { key: 'D', text: q.option_d },
  ]
})

// 题目类型映射
const questionTypeLabel = computed(() => {
  const t = (currentQuestion.value?.question_type || '').toLowerCase()
  if (t.includes('capital') || t.includes('省会')) return '🏛️ 省会'
  if (t.includes('abbreviation') || t.includes('简称') || t.includes('short')) return '📝 简称'
  return '🎯 特色'
})

const tagType = computed(() => {
  const t = (currentQuestion.value?.question_type || '').toLowerCase()
  if (t.includes('capital') || t.includes('省会')) return 'primary'
  if (t.includes('abbreviation') || t.includes('简称') || t.includes('short')) return 'success'
  return 'warning'
})

// 判断是否正确
const isCorrect = computed(() => {
  if (!selectedOption.value) return false
  return selectedOption.value === currentQuestion.value?.correct_answer
})

// 选项样式
function getOptionClass(key) {
  if (!answered.value) return ''
  const correct = currentQuestion.value?.correct_answer
  if (key === correct) return 'option-correct'
  if (key === selectedOption.value && key !== correct) return 'option-wrong'
  return 'option-dimmed'
}

// 正确答案文本
const correctAnswerText = computed(() => {
  const q = currentQuestion.value
  if (!q) return ''
  const map = { A: q.option_a, B: q.option_b, C: q.option_c, D: q.option_d }
  return map[q.correct_answer] || ''
})

// 选择选项
function selectOption(key) {
  if (answered.value) return
  answered.value = true
  selectedOption.value = key

  if (key === currentQuestion.value?.correct_answer) {
    correctCount.value++
    streak.value++
    if (streak.value > bestStreak.value) {
      bestStreak.value = streak.value
    }
    // 基础得分
    gameStore.addScore(10)
    roundScore.value += 10
    // 连击奖励
    if (streak.value >= 3) {
      gameStore.addScore(5)
      roundScore.value += 5
    }
  } else {
    streak.value = 0
  }
}

// 下一题
function nextQuestion() {
  if (currentIndex.value < totalQuestions.value - 1) {
    currentIndex.value++
    answered.value = false
    selectedOption.value = null
  } else {
    gameOver.value = true
  }
}

// 结果数据
const accuracyPercent = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round((correctCount.value / totalQuestions.value) * 100)
})

const starRating = computed(() => {
  const pct = accuracyPercent.value
  if (pct === 0) return 0
  if (pct <= 20) return 1
  if (pct <= 40) return 2
  if (pct <= 60) return 3
  if (pct <= 80) return 4
  return 5
})

const starLabel = computed(() => {
  const map = ['', '继续加油 💪', '还需努力 📖', '不错哦 👍', '很棒！🌟', '完美通关！🎉']
  return map[starRating.value] || ''
})

const resultEmoji = computed(() => {
  const r = starRating.value
  if (r <= 1) return '😅'
  if (r <= 2) return '🙂'
  if (r <= 3) return '😊'
  if (r <= 4) return '🥳'
  return '🏆'
})

// 重新开始
function restartGame() {
  questions.value = []
  currentIndex.value = 0
  answered.value = false
  selectedOption.value = null
  gameOver.value = false
  correctCount.value = 0
  streak.value = 0
  bestStreak.value = 0
  roundScore.value = 0
  loading.value = true
  fetchQuestions()
}

function goBack() {
  router.push('/')
}

// 获取题目
async function fetchQuestions() {
  loading.value = true
  try {
    const data = await getQuizQuestions(10)
    // 确保至少得到 1 题
    if (data && data.length > 0) {
      questions.value = data
    } else {
      ElMessage.warning('暂未获取到题目，请稍后再试')
    }
  } catch (e) {
    ElMessage.error('加载题目失败，请检查网络')
    console.error('获取题目失败:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchQuestions()
})
</script>

<style scoped>
.quiz-container {
  min-height: 100vh;
  padding: 16px;
  background: linear-gradient(135deg, #e3f2fd 0%, #e0f7fa 50%, #f1f8e9 100%);
}

/* 顶部栏 */
.quiz-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 600px;
  margin: 0 auto 16px;
}

.back-btn {
  font-size: 15px;
  color: #1565c0;
  font-weight: 600;
}

.score-display {
  font-size: 16px;
  font-weight: 700;
  color: #ff8f00;
  background: rgba(255, 143, 0, 0.1);
  padding: 6px 16px;
  border-radius: 20px;
}

/* 加载状态 */
.loading-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
}

.loading-icon {
  font-size: 64px;
  animation: bounce 1.2s infinite;
}

.loading-text {
  margin-top: 16px;
  font-size: 18px;
  color: #1565c0;
  font-weight: 600;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-16px); }
}

/* 进度条区域 */
.progress-section {
  max-width: 600px;
  margin: 0 auto 20px;
}

.progress-label {
  text-align: center;
  font-size: 14px;
  color: #555;
  margin-bottom: 6px;
}

.progress-label strong {
  color: #1565c0;
  font-size: 16px;
}

/* 题目卡片 */
.question-card {
  max-width: 600px;
  margin: 0 auto;
  border-radius: 20px;
  border: none;
  padding: 8px;
  background: #fff;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.province-tag {
  font-size: 13px;
  color: #888;
}

.question-text {
  font-size: 20px;
  color: #263238;
  line-height: 1.5;
  margin: 0 0 24px;
  font-weight: 700;
}

/* 选项网格 */
.options-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 14px;
  background: #fafafa;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 16px;
  text-align: left;
  color: #333;
}

.option-btn:not(:disabled):hover {
  border-color: #42a5f5;
  background: #e3f2fd;
  transform: translateX(4px);
}

.option-btn:not(:disabled):active {
  transform: scale(0.98);
}

.option-btn:disabled {
  cursor: default;
}

.option-letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #1565c0;
  color: #fff;
  font-weight: 700;
  font-size: 15px;
  flex-shrink: 0;
  transition: background 0.25s;
}

.option-text {
  flex: 1;
  line-height: 1.4;
}

/* 正确选项 */
.option-correct {
  border-color: #4caf50;
  background: #e8f5e9;
}

.option-correct .option-letter {
  background: #4caf50;
}

/* 错误选项 */
.option-wrong {
  border-color: #f44336;
  background: #ffebee;
  animation: shake 0.4s ease;
}

.option-wrong .option-letter {
  background: #f44336;
}

/* 未选中的选项（已答题后） */
.option-dimmed {
  opacity: 0.5;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}

/* 反馈区域 */
.feedback-area {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px dashed #e0e0e0;
  text-align: center;
}

.feedback-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.feedback-icon {
  font-size: 28px;
}

.feedback-title {
  font-size: 18px;
  font-weight: 700;
}

.icon-correct + .feedback-title {
  color: #2e7d32;
}

.icon-wrong + .feedback-title {
  color: #c62828;
}

.streak-bonus {
  font-size: 15px;
  color: #e65100;
  font-weight: 700;
  background: #fff3e0;
  padding: 2px 12px;
  border-radius: 12px;
}

.correct-answer-text {
  font-size: 16px;
  color: #555;
  margin-bottom: 6px;
}

.correct-answer-text strong {
  color: #2e7d32;
}

.feedback-points {
  font-size: 15px;
  color: #888;
  margin-bottom: 16px;
}

.next-btn {
  min-width: 140px;
  font-size: 16px;
  font-weight: 600;
}

/* 结果界面 */
.result-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  padding: 20px 0;
}

.result-card {
  max-width: 480px;
  width: 100%;
  border-radius: 24px;
  border: none;
  text-align: center;
  padding: 12px;
}

.result-emoji {
  font-size: 72px;
  margin-bottom: 8px;
  animation: resultPop 0.6s ease;
}

@keyframes resultPop {
  0% { transform: scale(0); opacity: 0; }
  60% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

.result-title {
  font-size: 26px;
  color: #1565c0;
  margin: 0 0 16px;
  font-weight: 800;
}

/* 星星 */
.stars-row {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 4px;
}

.star {
  font-size: 36px;
  transition: all 0.3s ease;
}

.star-active {
  color: #ffc107;
  text-shadow: 0 0 8px rgba(255, 193, 7, 0.5);
  animation: starPop 0.4s ease backwards;
}

.star-active:nth-child(1) { animation-delay: 0.1s; }
.star-active:nth-child(2) { animation-delay: 0.2s; }
.star-active:nth-child(3) { animation-delay: 0.3s; }
.star-active:nth-child(4) { animation-delay: 0.4s; }
.star-active:nth-child(5) { animation-delay: 0.5s; }

@keyframes starPop {
  0% { transform: scale(0) rotate(-30deg); }
  70% { transform: scale(1.3) rotate(5deg); }
  100% { transform: scale(1) rotate(0); }
}

.star-inactive {
  color: #e0e0e0;
}

.star-label {
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
}

/* 统计信息 */
.result-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 16px;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
}

.stat-correct { color: #4caf50; }
.stat-wrong { color: #f44336; }
.stat-streak { color: #ff6f00; }
.stat-rate { color: #1565c0; }

.stat-label {
  font-size: 13px;
  color: #888;
  margin-top: 2px;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: #e0e0e0;
}

/* 得分 */
.result-score-section {
  margin-bottom: 8px;
}

.result-score-label {
  font-size: 15px;
  color: #888;
  margin-right: 8px;
}

.result-score-value {
  font-size: 28px;
  font-weight: 800;
  color: #ff6f00;
}

.result-total {
  font-size: 15px;
  color: #666;
  margin-bottom: 24px;
}

/* 结果按钮 */
.result-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.retry-btn {
  min-width: 200px;
  font-size: 18px;
  font-weight: 700;
}

.home-btn {
  font-size: 15px;
  color: #666;
}

/* 过渡动画 */
.slide-fade-enter-active {
  transition: all 0.35s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.25s ease-in;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}

.fade-enter-active {
  transition: opacity 0.3s ease;
}
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
