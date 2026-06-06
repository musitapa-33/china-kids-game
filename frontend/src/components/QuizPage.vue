<template>
  <div class="quiz-page">
    <div class="qz-wrap">
      <div class="qz-head">
        <div class="qz-badge">第 {{ currentIndex + 1 }} 关</div>
        <div style="font-size:.9em;color:#666">⭐ {{ quizScore }} 分</div>
      </div>
      
      <div v-if="!showResult" id="qzBody">
        <div class="qz-q">{{ currentQuestion?.q }}</div>
        <div class="qz-opts">
          <div 
            v-for="(choice, index) in currentQuestion?.choices" 
            :key="index"
            :class="['qz-opt', { ok: showAnswer && index === currentQuestion?.answer, no: showAnswer && selectedAnswer === index && index !== currentQuestion?.answer }]"
            @click="answer(index)"
            :style="{ pointerEvents: showAnswer ? 'none' : 'auto' }"
          >
            {{ String.fromCharCode(65 + index) }}. {{ choice }}
          </div>
        </div>
        <div :class="['qz-fb', { show: showAnswer, 'ok-fb': isCorrect, 'no-fb': !isCorrect }]">
          {{ feedbackText }}
        </div>
        <el-button 
          v-if="showAnswer" 
          class="qz-next" 
          @click="nextQuestion"
        >
          {{ currentIndex >= questions.length - 1 ? '查看结果 🎉' : '下一题 ➡️' }}
        </el-button>
      </div>
      
      <div v-else class="qz-result">
        <span class="r-emoji">🎉</span>
        <div style="font-size:1.1em;color:#555;margin:6px 0">闯关完成！</div>
        <div class="r-score">{{ quizScore }} ⭐</div>
        <div style="color:#999;font-size:.85em;margin:4px 0">总分</div>
        <div class="r-stars">{{ starsDisplay }}</div>
        <el-button @click="restartQuiz">再玩一次 🔄</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { PROVINCE_DATA, REGIONS } from '../api/provinceApi'
import { useScoreStore } from '../stores/scoreStore'

const scoreStore = useScoreStore()
const questions = ref([])
const currentIndex = ref(0)
const quizScore = ref(0)
const showAnswer = ref(false)
const selectedAnswer = ref(-1)
const showResult = ref(false)

const currentQuestion = computed(() => questions.value[currentIndex.value])

const isCorrect = computed(() => {
  return selectedAnswer.value === currentQuestion.value?.answer
})

const feedbackText = computed(() => {
  if (!showAnswer.value) return ''
  if (isCorrect.value) return '🎉 回答正确！ +10⭐'
  return `😅 答错了，正确答案是：${currentQuestion.value?.choices[currentQuestion.value?.answer]}`
})

const starsDisplay = computed(() => {
  const stars = Math.min(5, Math.max(1, Math.ceil(quizScore.value / 20)))
  return '⭐'.repeat(stars) + '☆'.repeat(5 - stars)
})

const shuffleArray = (array) => {
  const newArray = [...array]
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[newArray[i], newArray[j]] = [newArray[j], newArray[i]]
  }
  return newArray
}

const generateQuiz = () => {
  const qs = []
  const used = {}
  const pool = shuffleArray(PROVINCE_DATA)
  
  let pi = 0
  while (qs.length < 10 && pi < pool.length) {
    const p = pool[pi++]
    if (used[p.name]) continue
    used[p.name] = true
    
    const types = ['capital', 'abbr', 'region', 'emoji']
    const type = types[Math.floor(Math.random() * types.length)]
    
    let q, choices, answer
    
    if (type === 'capital') {
      q = `"${p.name}"的省会是？`
      choices = [p.capital]
      while (choices.length < 4) {
        const c = PROVINCE_DATA[Math.floor(Math.random() * PROVINCE_DATA.length)].capital
        if (!choices.includes(c)) choices.push(c)
      }
      answer = choices.indexOf(p.capital)
    } else if (type === 'abbr') {
      q = `"${p.name}"的简称是？`
      choices = [p.abbr]
      while (choices.length < 4) {
        const c = PROVINCE_DATA[Math.floor(Math.random() * PROVINCE_DATA.length)].abbr
        if (!choices.includes(c)) choices.push(c)
      }
      answer = choices.indexOf(p.abbr)
    } else if (type === 'region') {
      q = `"${p.name}"属于哪个地区？`
      choices = [p.region]
      const others = REGIONS.filter(r => r !== '全部' && r !== p.region)
      while (choices.length < 4 && others.length > 0) {
        const ri = Math.floor(Math.random() * others.length)
        choices.push(others[ri])
        others.splice(ri, 1)
      }
      answer = choices.indexOf(p.region)
    } else {
      q = `这个 emoji 代表哪个省？${p.emoji}`
      choices = [p.name]
      while (choices.length < 4) {
        const c = PROVINCE_DATA[Math.floor(Math.random() * PROVINCE_DATA.length)].name
        if (!choices.includes(c)) choices.push(c)
      }
      answer = choices.indexOf(p.name)
    }
    
    const zipped = choices.map((choice, idx) => [choice, idx === answer])
    const shuffledZipped = shuffleArray(zipped)
    
    const newChoices = []
    let newAnswer = -1
    shuffledZipped.forEach(([choice, isAnswer], idx) => {
      newChoices.push(choice)
      if (isAnswer) newAnswer = idx
    })
    
    qs.push({ q, choices: newChoices, answer: newAnswer })
  }
  
  return qs
}

const answer = (index) => {
  if (showAnswer.value) return
  selectedAnswer.value = index
  showAnswer.value = true
  
  if (index === currentQuestion.value?.answer) {
    quizScore.value += 10
    scoreStore.addScore(10)
  }
}

const nextQuestion = () => {
  if (currentIndex.value >= questions.value.length - 1) {
    showResult.value = true
    if (Math.floor(quizScore.value / 20) >= 3) {
      scoreStore.addScore(15)
    }
    scoreStore.checkBadges()
  } else {
    currentIndex.value++
    showAnswer.value = false
    selectedAnswer.value = -1
  }
}

const restartQuiz = () => {
  questions.value = generateQuiz()
  currentIndex.value = 0
  quizScore.value = 0
  showAnswer.value = false
  selectedAnswer.value = -1
  showResult.value = false
}

onMounted(() => {
  questions.value = generateQuiz()
})
</script>

<style scoped>
.quiz-page {
  animation: fadeIn .3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.qz-wrap {
  background: #fff;
  border-radius: 16px;
  padding: 18px 15px;
  box-shadow: 0 3px 14px rgba(0, 0, 0, .08);
  max-width: 560px;
  margin: 0 auto;
}

.qz-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 6px;
}

.qz-badge {
  background: linear-gradient(45deg, #fb8c00, #ffa726);
  color: #fff;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: .82em;
  font-weight: 700;
}

.qz-q {
  font-size: 1.05em;
  color: #333;
  margin-bottom: 14px;
  line-height: 1.6;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 10px;
}

.qz-opts {
  display: grid;
  gap: 9px;
}

.qz-opt {
  padding: 11px 14px;
  background: #fafafa;
  border-radius: 12px;
  cursor: pointer;
  transition: all .2s;
  border: 2px solid #e0e0e0;
  font-size: .92em;
  text-align: left;
}

.qz-opt:hover:not(.ok):not(.no) {
  border-color: #1e88e5;
  background: #e3f2fd;
  transform: scale(1.01);
}

.qz-opt.ok {
  border-color: #43a047;
  background: #e8f5e9;
  color: #2e7d32;
  font-weight: 700;
}

.qz-opt.no {
  border-color: #e53935;
  background: #ffebee;
  color: #c62828;
}

.qz-fb {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  font-size: .88em;
  display: none;
  line-height: 1.5;
}

.qz-fb.show {
  display: block;
}

.qz-fb.ok-fb {
  background: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}

.qz-fb.no-fb {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
}

.qz-next {
  margin-top: 12px;
  padding: 8px 22px;
  background: linear-gradient(135deg, #1e88e5, #42a5f5);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: .9em;
  font-weight: 700;
  transition: .2s;
}

.qz-next:hover {
  opacity: .9;
  transform: scale(1.03);
}

.qz-result {
  text-align: center;
  padding: 28px 10px;
}

.r-emoji {
  font-size: 3em;
  display: block;
  margin-bottom: 8px;
}

.r-score {
  font-size: 2.5em;
  font-weight: 700;
  color: #ff6f00;
}

.r-stars {
  font-size: 1.8em;
  margin: 8px 0;
}
</style>
