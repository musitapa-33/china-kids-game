<template>
  <div class="courseware-container">
    <!-- 顶部工具栏 -->
    <div class="top-bar">
      <div class="title-section">
        <span class="app-title">🌏 环游中国</span>
        <el-tag type="warning" effect="dark" size="small" class="course-tag">地理小课堂</el-tag>
      </div>
      <div class="controls-section">
        <div class="autoplay-control">
          <span class="autoplay-label">自动播放</span>
          <el-switch
            v-model="autoPlayEnabled"
            size="small"
            active-color="#67c23a"
            inactive-color="#dcdfe6"
            @change="onAutoPlayToggle"
          />
        </div>
        <el-tag type="success" effect="plain" size="small" class="page-indicator">
          🎯 {{ currentSlideLabel }}
        </el-tag>
      </div>
    </div>

    <!-- 顶部进度条 -->
    <div class="progress-bar-wrapper">
      <el-progress
        :percentage="progressPercent"
        :stroke-width="8"
        :show-text="false"
        color="linear-gradient(90deg, #f56c6c, #e6a23c, #67c23a, #409eff, #9b59b6)"
      />
      <div class="progress-dots">
        <span
          v-for="(slide, index) in slides"
          :key="index"
          class="dot"
          :class="{ active: currentIndex === index }"
          :style="{ backgroundColor: currentIndex === index ? slide.accentColor : '#ddd' }"
          @click="goToSlide(index)"
        />
      </div>
    </div>

    <!-- 幻灯片主区域 -->
    <div class="slide-area" @click="handleAreaClick">
      <div class="prev-btn-wrapper" @click.stop="prevSlide">
        <div class="nav-btn prev-btn" :class="{ disabled: currentIndex === 0 }">
          <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </div>
      </div>

      <div class="slide-wrapper">
        <div
          class="slide-card"
          :class="[slideTransitionClass]"
          :style="{ backgroundColor: currentSlide.backgroundColor }"
        >
          <!-- 装饰图形 -->
          <div class="deco deco-1" :style="{ background: currentSlide.accentColor }" />
          <div class="deco deco-2" :style="{ background: currentSlide.accentColor }" />
          <div class="deco deco-3" :style="{ background: currentSlide.accentColor }" />

          <!-- 幻灯片编号角标 -->
          <div class="slide-badge" :style="{ background: currentSlide.accentColor }">
            {{ currentIndex + 1 }}
          </div>

          <!-- 内容区 -->
          <div class="slide-content">
            <div class="slide-icon-wrapper">
              <span class="slide-icon">{{ currentSlide.icon }}</span>
            </div>
            <h2 class="slide-title">{{ currentSlide.title }}</h2>
            <div class="slide-divider" :style="{ background: currentSlide.accentColor }" />
            <div class="slide-body" v-html="currentSlide.content" />
          </div>
        </div>
      </div>

      <div class="next-btn-wrapper" @click.stop="nextSlide">
        <div class="nav-btn next-btn" :class="{ disabled: currentIndex === slides.length - 1 }">
          <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <div class="bottom-bar">
      <el-button
        type="primary"
        :disabled="currentIndex === 0"
        @click="prevSlide"
        class="bottom-nav-btn"
      >
        ← 上一页
      </el-button>

      <div class="bottom-dots">
        <span
          v-for="(slide, index) in slides"
          :key="'dot-' + index"
          class="bottom-dot"
          :class="{ active: currentIndex === index }"
          :style="{
            backgroundColor: currentIndex === index ? slide.accentColor : '#e8e8e8',
            transform: currentIndex === index ? 'scale(1.3)' : 'scale(1)'
          }"
          @click="goToSlide(index)"
        />
      </div>

      <el-button
        type="primary"
        :disabled="currentIndex === slides.length - 1"
        @click="nextSlide"
        class="bottom-nav-btn"
      >
        下一页 →
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElButton, ElProgress, ElTag, ElSwitch } from 'element-plus'

// ---------- 幻灯片数据 ----------
const slides = ref([
  {
    title: '中国概况',
    icon: '🇨🇳',
    backgroundColor: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
    accentColor: '#e74c3c',
    content: `
      <div class="fact-grid">
        <div class="fact-card">
          <span class="fact-emoji">📍</span>
          <span class="fact-text">位于亚洲东部</span>
        </div>
        <div class="fact-card">
          <span class="fact-emoji">🗺️</span>
          <span class="fact-text">面积约 <strong>960万</strong> 平方公里</span>
        </div>
        <div class="fact-card">
          <span class="fact-emoji">🥉</span>
          <span class="fact-text">世界第三大国家</span>
        </div>
        <div class="fact-card">
          <span class="fact-emoji">🏛️</span>
          <span class="fact-text"><strong>34</strong> 个省级行政区</span>
        </div>
      </div>
      <p class="slide-summary">中国是一个地大物博、历史悠久的美丽国家！</p>
    `
  },
  {
    title: '四大地理区域',
    icon: '🗾',
    backgroundColor: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    accentColor: '#1abc9c',
    content: `
      <div class="region-grid">
        <div class="region-card" style="border-left-color: #e74c3c;">
          <span class="region-icon">❄️</span>
          <span class="region-name">北方地区</span>
          <span class="region-desc">四季分明，冬天会下雪</span>
        </div>
        <div class="region-card" style="border-left-color: #f39c12;">
          <span class="region-icon">🌴</span>
          <span class="region-name">南方地区</span>
          <span class="region-desc">温暖湿润，四季常青</span>
        </div>
        <div class="region-card" style="border-left-color: #e67e22;">
          <span class="region-icon">🏜️</span>
          <span class="region-name">西北地区</span>
          <span class="region-desc">干旱少雨，有大沙漠</span>
        </div>
        <div class="region-card" style="border-left-color: #9b59b6;">
          <span class="region-icon">🏔️</span>
          <span class="region-name">青藏地区</span>
          <span class="region-desc">世界屋脊，高寒缺氧</span>
        </div>
      </div>
    `
  },
  {
    title: '首都北京',
    icon: '🏯',
    backgroundColor: 'linear-gradient(135deg, #f5af19 0%, #f12711 100%)',
    accentColor: '#e67e22',
    content: `
      <div class="spot-grid">
        <div class="spot-item">
          <span class="spot-emoji">🏛️</span>
          <strong>故宫</strong> — 有600多年历史的皇家宫殿
        </div>
        <div class="spot-item">
          <span class="spot-emoji">🏛️</span>
          <strong>天安门</strong> — 世界上最大的城市广场
        </div>
        <div class="spot-item">
          <span class="spot-emoji">🧱</span>
          <strong>长城</strong> — 万里长城，人类奇迹！
        </div>
        <div class="spot-item">
          <span class="spot-emoji">🥟</span>
          <strong>北京烤鸭</strong> — 全世界都知道的美食！
        </div>
      </div>
      <p class="slide-summary">北京是中国的政治、文化中心，也是我们国家的首都！</p>
    `
  },
  {
    title: '56个民族',
    icon: '👨‍👩‍👧‍👦',
    backgroundColor: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    accentColor: '#e84393',
    content: `
      <div class="ethnic-info">
        <div class="ethnic-main">
          <span class="ethnic-circle" style="background:#e74c3c;">👨</span>
          <span class="ethnic-circle" style="background:#f39c12;">👩</span>
          <span class="ethnic-circle" style="background:#27ae60;">👦</span>
          <span class="ethnic-circle" style="background:#2980b9;">👧</span>
          <span class="ethnic-circle" style="background:#8e44ad;">👳</span>
        </div>
        <div class="ethnic-detail">
          <p>中国有 <strong>56个民族</strong>，像 <span class="highlight-text">56朵花</span> 一样美丽！</p>
          <p>其中 <el-tag size="small" type="danger" effect="dark">汉族</el-tag> 人口最多，</p>
          <p>其他 <el-tag size="small" type="warning" effect="dark">55个</el-tag> 是少数民族。</p>
          <p class="ethnic-quote">"五十六个民族，五十六枝花，五十六个兄弟姐妹是一家！"</p>
        </div>
      </div>
    `
  },
  {
    title: '美食地图',
    icon: '🍜',
    backgroundColor: 'linear-gradient(135deg, #ffecd2 0%, #ff9a9e 100%)',
    accentColor: '#e74c3c',
    content: `
      <div class="food-grid">
        <div class="food-card" style="background:#fff5f5;">
          <span class="food-emoji">🌶️</span>
          <strong>川菜</strong>
          <span class="food-tag">麻辣</span>
        </div>
        <div class="food-card" style="background:#f0fff4;">
          <span class="food-emoji">🦐</span>
          <strong>粤菜</strong>
          <span class="food-tag">鲜美</span>
        </div>
        <div class="food-card" style="background:#fffbea;">
          <span class="food-emoji">🥟</span>
          <strong>鲁菜</strong>
          <span class="food-tag">醇厚</span>
        </div>
        <div class="food-card" style="background:#f0f0ff;">
          <span class="food-emoji">🦆</span>
          <strong>北京</strong>
          <span class="food-tag">烤鸭</span>
        </div>
        <div class="food-card" style="background:#fff0f5;">
          <span class="food-emoji">🥟</span>
          <strong>上海</strong>
          <span class="food-tag">小笼包</span>
        </div>
        <div class="food-card" style="background:#f5fff0;">
          <span class="food-emoji">🥘</span>
          <strong>重庆</strong>
          <span class="food-tag">火锅</span>
        </div>
      </div>
      <p class="slide-summary">每个地方都有特色美食，你想先吃哪一个？🤤</p>
    `
  },
  {
    title: '世界遗产',
    icon: '🏛️',
    backgroundColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    accentColor: '#8e44ad',
    content: `
      <div class="heritage-grid">
        <div class="heritage-card">
          <span class="heritage-icon">🧱</span>
          <div>
            <strong>长城</strong>
            <span class="heritage-stat">全长21,196公里</span>
          </div>
        </div>
        <div class="heritage-card">
          <span class="heritage-icon">🏯</span>
          <div>
            <strong>故宫</strong>
            <span class="heritage-stat">明清两代皇宫</span>
          </div>
        </div>
        <div class="heritage-card">
          <span class="heritage-icon">🗿</span>
          <div>
            <strong>兵马俑</strong>
            <span class="heritage-stat">秦始皇的守卫</span>
          </div>
        </div>
        <div class="heritage-card">
          <span class="heritage-icon">🏔️</span>
          <div>
            <strong>泰山</strong>
            <span class="heritage-stat">五岳之首</span>
          </div>
        </div>
      </div>
      <p class="slide-summary">中国有 <strong>57项</strong> 世界遗产，数量居世界前列！🌟</p>
    `
  },
  {
    title: '交通网络',
    icon: '🚄',
    backgroundColor: 'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)',
    accentColor: '#2980b9',
    content: `
      <div class="transport-showcase">
        <div class="transport-highlight">
          <span class="transport-icon">🚄</span>
          <div class="transport-stat">
            <span class="stat-number">世界第一</span>
            <span class="stat-label">高铁总里程</span>
          </div>
        </div>
        <div class="transport-details">
          <div class="transport-item">
            <span>🚄</span>
            <span>北京 → 上海：<strong>4.5小时</strong></span>
          </div>
          <div class="transport-item">
            <span>🚄</span>
            <span>北京 → 广州：<strong>8小时</strong></span>
          </div>
          <div class="transport-item">
            <span>✈️</span>
            <span>全国有 <strong>200+</strong> 个机场</span>
          </div>
          <div class="transport-item">
            <span>🚌</span>
            <span>高速公路 <strong>17万公里</strong></span>
          </div>
        </div>
      </div>
    `
  },
  {
    title: '名山大川',
    icon: '⛰️',
    backgroundColor: 'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)',
    accentColor: '#27ae60',
    content: `
      <div class="mountain-grid">
        <div class="mountain-card">
          <span class="mountain-emoji">⛰️</span>
          <strong>东岳泰山</strong>
          <span>山东 · 五岳独尊</span>
        </div>
        <div class="mountain-card">
          <span class="mountain-emoji">⛰️</span>
          <strong>西岳华山</strong>
          <span>陕西 · 奇险天下</span>
        </div>
        <div class="mountain-card">
          <span class="mountain-emoji">⛰️</span>
          <strong>南岳衡山</strong>
          <span>湖南 · 独秀</span>
        </div>
        <div class="mountain-card">
          <span class="mountain-emoji">⛰️</span>
          <strong>北岳恒山</strong>
          <span>山西 · 壮观</span>
        </div>
        <div class="mountain-card">
          <span class="mountain-emoji">⛰️</span>
          <strong>中岳嵩山</strong>
          <span>河南 · 少林寺</span>
        </div>
        <div class="mountain-card">
          <span class="mountain-emoji">🌄</span>
          <strong>黄山</strong>
          <span>"归来不看岳"</span>
        </div>
      </div>
      <p class="slide-summary">五岳归来不看山，黄山归来不看岳！🏔️</p>
    `
  },
  {
    title: '河流湖泊',
    icon: '🌊',
    backgroundColor: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)',
    accentColor: '#3498db',
    content: `
      <div class="water-showcase">
        <div class="water-card" style="border-left-color: #2980b9;">
          <span class="water-emoji">🏞️</span>
          <div>
            <strong>长江</strong>
            <span class="water-desc">中国第一大河，全长6300公里</span>
          </div>
        </div>
        <div class="water-card" style="border-left-color: #f1c40f;">
          <span class="water-emoji">🌊</span>
          <div>
            <strong>黄河</strong>
            <span class="water-desc">中华民族的母亲河</span>
          </div>
        </div>
        <div class="water-card" style="border-left-color: #1abc9c;">
          <span class="water-emoji">💧</span>
          <div>
            <strong>青海湖</strong>
            <span class="water-desc">中国最大的湖泊</span>
          </div>
        </div>
        <div class="water-card" style="border-left-color: #9b59b6;">
          <span class="water-emoji">🏊</span>
          <div>
            <strong>鄱阳湖</strong>
            <span class="water-desc">中国最大的淡水湖</span>
          </div>
        </div>
      </div>
    `
  },
  {
    title: '动物王国',
    icon: '🐼',
    backgroundColor: 'linear-gradient(135deg, #a8e6cf 0%, #ffd3b6 100%)',
    accentColor: '#2ecc71',
    content: `
      <div class="animal-grid">
        <div class="animal-card animal-panda">
          <span class="animal-emoji">🐼</span>
          <div>
            <strong>大熊猫</strong>
            <span class="animal-desc">国宝，可爱极了！</span>
          </div>
        </div>
        <div class="animal-card animal-monkey">
          <span class="animal-emoji">🐒</span>
          <div>
            <strong>金丝猴</strong>
            <span class="animal-desc">金色毛发，珍稀动物</span>
          </div>
        </div>
        <div class="animal-card animal-antelope">
          <span class="animal-emoji">🦌</span>
          <div>
            <strong>藏羚羊</strong>
            <span class="animal-desc">青藏高原的精灵</span>
          </div>
        </div>
        <div class="animal-card animal-crane">
          <span class="animal-emoji">🦩</span>
          <div>
            <strong>丹顶鹤</strong>
            <span class="animal-desc">仙鹤，象征长寿</span>
          </div>
        </div>
        <div class="animal-card animal-tiger">
          <span class="animal-emoji">🐯</span>
          <div>
            <strong>东北虎</strong>
            <span class="animal-desc">森林之王</span>
          </div>
        </div>
        <div class="animal-card animal-elephant">
          <span class="animal-emoji">🐘</span>
          <div>
            <strong>亚洲象</strong>
            <span class="animal-desc">云南热带雨林</span>
          </div>
        </div>
      </div>
    `
  },
  {
    title: '知识总结',
    icon: '🎓',
    backgroundColor: 'linear-gradient(135deg, #ffecd2 0%, #a8edea 100%)',
    accentColor: '#f39c12',
    content: `
      <div class="summary-cards">
        <div class="summary-item">
          <span class="summary-icon" style="background:#e74c3c;">🇨🇳</span>
          <span>中国是世界第三大国家</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon" style="background:#1abc9c;">🗾</span>
          <span>四大地理区域各具特色</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon" style="background:#e67e22;">🏯</span>
          <span>北京有故宫、长城等奇迹</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon" style="background:#e84393;">👨‍👩‍👧‍👦</span>
          <span>56个民族是一家</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon" style="background:#8e44ad;">🏛️</span>
          <span>57项世界遗产举世瞩目</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon" style="background:#27ae60;">🐼</span>
          <span>大熊猫是我们的国宝</span>
        </div>
      </div>
      <div class="summary-final">
        🎉 太棒了！你已经学完了中国地理小知识！
        <br>
        继续探索我们美丽的祖国吧！🌏❤️
      </div>
    `
  }
])

// ---------- 状态 ----------
const currentIndex = ref(0)
const autoPlayEnabled = ref(false)
const transitionDirection = ref('next') // 'next' | 'prev'
const slideTransitionClass = ref('')

let autoPlayTimer = null

// ---------- 计算属性 ----------
const currentSlide = computed(() => slides.value[currentIndex.value])
const totalSlides = computed(() => slides.value.length)
const progressPercent = computed(() => ((currentIndex.value + 1) / totalSlides.value) * 100)
const currentSlideLabel = computed(() => `第 ${currentIndex.value + 1} 页 / 共 ${totalSlides.value} 页`)

// ---------- 导航方法 ----------
function goToSlide(index) {
  if (index < 0 || index >= slides.value.length || index === currentIndex.value) return
  transitionDirection.value = index > currentIndex.value ? 'next' : 'prev'
  startSlideTransition()
  currentIndex.value = index
  resetAutoPlayTimer()
}

function nextSlide() {
  if (currentIndex.value < slides.value.length - 1) {
    transitionDirection.value = 'next'
    startSlideTransition()
    currentIndex.value++
    resetAutoPlayTimer()
  }
}

function prevSlide() {
  if (currentIndex.value > 0) {
    transitionDirection.value = 'prev'
    startSlideTransition()
    currentIndex.value--
    resetAutoPlayTimer()
  }
}

// ---------- 过渡动画 ----------
function startSlideTransition() {
  slideTransitionClass.value = ''
  // 触发浏览器重排以重新启动动画
  void document.body.offsetHeight
  slideTransitionClass.value = transitionDirection.value === 'next' ? 'slide-enter-right' : 'slide-enter-left'
}

// ---------- 自动播放 ----------
function onAutoPlayToggle(val) {
  if (val) {
    startAutoPlay()
  } else {
    stopAutoPlay()
  }
}

function startAutoPlay() {
  stopAutoPlay()
  autoPlayTimer = setInterval(() => {
    if (currentIndex.value >= slides.value.length - 1) {
      currentIndex.value = 0
      transitionDirection.value = 'next'
    } else {
      nextSlide()
    }
  }, 4000)
}

function stopAutoPlay() {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer)
    autoPlayTimer = null
  }
}

function resetAutoPlayTimer() {
  if (autoPlayEnabled.value) {
    startAutoPlay()
  }
}

// ---------- 点击区域切换（点击左右半区切换页面） ----------
function handleAreaClick(event) {
  const slideArea = event.currentTarget
  const rect = slideArea.getBoundingClientRect()
  const x = event.clientX - rect.left
  const third = rect.width / 3
  if (x > third * 2) {
    nextSlide()
  } else if (x < third) {
    prevSlide()
  }
}

// ---------- 键盘监听 ----------
function onKeyDown(event) {
  if (event.key === 'ArrowRight') {
    event.preventDefault()
    nextSlide()
  } else if (event.key === 'ArrowLeft') {
    event.preventDefault()
    prevSlide()
  }
}

// ---------- 生命周期 ----------
onMounted(() => {
  window.addEventListener('keydown', onKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown)
  stopAutoPlay()
})
</script>

<style scoped>
/* ========== 全局容器 ========== */
.courseware-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 50%, #fef3c7 100%);
  display: flex;
  flex-direction: column;
  padding: 16px 24px 20px;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  user-select: none;
}

/* ========== 顶部工具栏 ========== */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-shrink: 0;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.app-title {
  font-size: 22px;
  font-weight: 800;
  background: linear-gradient(90deg, #f56c6c, #e6a23c, #67c23a, #409eff, #9b59b6);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
}

.course-tag {
  border-radius: 12px !important;
  font-weight: 600 !important;
}

.controls-section {
  display: flex;
  align-items: center;
  gap: 14px;
}

.autoplay-control {
  display: flex;
  align-items: center;
  gap: 6px;
}

.autoplay-label {
  font-size: 13px;
  color: #555;
  font-weight: 500;
}

.page-indicator {
  font-size: 13px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
}

/* ========== 进度条 ========== */
.progress-bar-wrapper {
  margin-bottom: 16px;
  flex-shrink: 0;
}

.progress-dots {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.dot:hover {
  transform: scale(1.4);
  opacity: 0.8;
}

/* ========== 幻灯片区域 ========== */
.slide-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 0;
  cursor: pointer;
}

/* 导航按钮容器 */
.prev-btn-wrapper,
.next-btn-wrapper {
  flex-shrink: 0;
  z-index: 2;
}

.nav-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s ease;
  color: #555;
  backdrop-filter: blur(6px);
}

.nav-btn:hover:not(.disabled) {
  background: #fff;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.18);
  transform: scale(1.08);
  color: #409eff;
}

.nav-btn.disabled {
  opacity: 0.3;
  cursor: not-allowed;
  transform: none !important;
}

/* ========== 幻灯片卡片 ========== */
.slide-wrapper {
  flex: 1;
  max-width: 760px;
  perspective: 1200px;
  min-height: 0;
}

.slide-card {
  position: relative;
  border-radius: 24px;
  padding: 36px 40px;
  min-height: 380px;
  max-height: 520px;
  overflow-y: auto;
  box-shadow:
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #333;
  transition: box-shadow 0.3s ease;
}

.slide-card::-webkit-scrollbar {
  width: 5px;
}

.slide-card::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 10px;
}

/* 过渡动画 */
.slide-card.slide-enter-right {
  animation: slideInRight 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

.slide-card.slide-enter-left {
  animation: slideInLeft 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(60px) rotateY(-8deg) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateX(0) rotateY(0deg) scale(1);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-60px) rotateY(8deg) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateX(0) rotateY(0deg) scale(1);
  }
}

/* ========== 装饰元素 ========== */
.deco {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
  pointer-events: none;
}

.deco-1 {
  width: 120px;
  height: 120px;
  top: -30px;
  right: -20px;
}

.deco-2 {
  width: 80px;
  height: 80px;
  bottom: -15px;
  left: -15px;
}

.deco-3 {
  width: 50px;
  height: 50px;
  bottom: 30%;
  right: 10%;
}

/* 角标 */
.slide-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* ========== 幻灯片内容 ========== */
.slide-content {
  position: relative;
  z-index: 1;
  text-align: center;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.slide-icon-wrapper {
  animation: bounceIn 0.6s ease;
}

.slide-icon {
  font-size: 52px;
  display: inline-block;
  line-height: 1;
}

@keyframes bounceIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.slide-title {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

.slide-divider {
  width: 60px;
  height: 4px;
  border-radius: 4px;
  opacity: 0.4;
  margin: 2px 0 6px;
}

.slide-body {
  width: 100%;
  font-size: 15px;
  line-height: 1.8;
}

.slide-summary {
  margin: 10px 0 0;
  font-size: 16px;
  font-weight: 600;
  color: #555;
}

/* ========== 第1页：概况卡片 ========== */
.fact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  width: 100%;
  max-width: 420px;
  margin: 4px auto;
}

.fact-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 14px;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.fact-emoji {
  font-size: 28px;
}

.fact-text {
  font-size: 14px;
  font-weight: 500;
}

/* ========== 第2页：区域卡片 ========== */
.region-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  width: 100%;
  max-width: 460px;
  margin: 4px auto;
}

.region-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(4px);
  border-radius: 14px;
  padding: 12px 10px;
  border-left: 5px solid;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.region-icon {
  font-size: 26px;
}

.region-name {
  font-weight: 700;
  font-size: 16px;
}

.region-desc {
  font-size: 13px;
  color: #666;
}

/* ========== 第3页：景点列表 ========== */
.spot-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  max-width: 400px;
  margin: 4px auto;
}

.spot-item {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 12px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.spot-emoji {
  font-size: 22px;
  flex-shrink: 0;
}

/* ========== 第4页：民族 ========== */
.ethnic-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.ethnic-main {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.ethnic-circle {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.ethnic-detail {
  text-align: center;
}

.ethnic-detail p {
  margin: 3px 0;
}

.highlight-text {
  color: #e74c3c;
  font-weight: 800;
}

.ethnic-quote {
  margin-top: 6px !important;
  font-style: italic;
  color: #8e44ad;
  font-weight: 600;
  background: rgba(142, 68, 173, 0.08);
  border-radius: 10px;
  padding: 6px 12px;
}

/* ========== 第5页：美食卡片 ========== */
.food-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  width: 100%;
  max-width: 460px;
  margin: 4px auto;
}

.food-card {
  border-radius: 14px;
  padding: 12px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.food-emoji {
  font-size: 28px;
}

.food-tag {
  font-size: 12px;
  color: #888;
  background: rgba(0, 0, 0, 0.04);
  padding: 1px 8px;
  border-radius: 8px;
}

/* ========== 第6页：世界遗产 ========== */
.heritage-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  width: 100%;
  max-width: 420px;
  margin: 4px auto;
}

.heritage-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 14px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.heritage-icon {
  font-size: 30px;
  flex-shrink: 0;
}

.heritage-stat {
  display: block;
  font-size: 12px;
  color: #777;
  margin-top: 1px;
}

/* ========== 第7页：交通 ========== */
.transport-showcase {
  width: 100%;
  max-width: 420px;
  margin: 4px auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.transport-highlight {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(4px);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
}

.transport-icon {
  font-size: 40px;
}

.transport-stat {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-number {
  font-size: 22px;
  font-weight: 800;
  color: #e74c3c;
}

.stat-label {
  font-size: 13px;
  color: #666;
}

.transport-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.transport-item {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 10px;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

/* ========== 第8页：名山 ========== */
.mountain-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  width: 100%;
  max-width: 460px;
  margin: 4px auto;
}

.mountain-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 14px;
  padding: 12px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  font-size: 13px;
}

.mountain-emoji {
  font-size: 28px;
}

/* ========== 第9页：河流湖泊 ========== */
.water-showcase {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  max-width: 420px;
  margin: 4px auto;
}

.water-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 14px;
  padding: 12px 14px;
  border-left: 5px solid;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.water-emoji {
  font-size: 28px;
  flex-shrink: 0;
}

.water-desc {
  display: block;
  font-size: 13px;
  color: #666;
  margin-top: 1px;
}

/* ========== 第10页：动物 ========== */
.animal-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  width: 100%;
  max-width: 460px;
  margin: 4px auto;
}

.animal-card {
  border-radius: 14px;
  padding: 12px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.animal-emoji {
  font-size: 30px;
}

.animal-desc {
  display: block;
  font-size: 12px;
  color: #777;
  margin-top: 1px;
}

.animal-panda { background: rgba(255, 255, 255, 0.75); border: 2px solid #2ecc71; }
.animal-monkey { background: rgba(255, 255, 255, 0.75); border: 2px solid #f39c12; }
.animal-antelope { background: rgba(255, 255, 255, 0.75); border: 2px solid #8e44ad; }
.animal-crane { background: rgba(255, 255, 255, 0.75); border: 2px solid #e74c3c; }
.animal-tiger { background: rgba(255, 255, 255, 0.75); border: 2px solid #e67e22; }
.animal-elephant { background: rgba(255, 255, 255, 0.75); border: 2px solid #2980b9; }

/* ========== 第11页：总结 ========== */
.summary-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  width: 100%;
  max-width: 440px;
  margin: 4px auto;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 12px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.summary-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.summary-final {
  margin-top: 10px;
  text-align: center;
  font-size: 17px;
  font-weight: 700;
  color: #e67e22;
  line-height: 1.7;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 14px;
  padding: 10px 16px;
  width: 100%;
  max-width: 440px;
}

/* ========== 底部导航 ========== */
.bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
  flex-shrink: 0;
  gap: 12px;
}

.bottom-nav-btn {
  border-radius: 20px !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 8px 20px !important;
  flex-shrink: 0;
}

.bottom-dots {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.bottom-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
}

.bottom-dot:hover {
  transform: scale(1.4) !important;
  opacity: 0.8;
}

/* ========== 响应式 ========== */
@media (max-width: 640px) {
  .courseware-container {
    padding: 10px 12px 14px;
  }

  .slide-card {
    padding: 24px 18px;
    min-height: 300px;
    max-height: 440px;
    border-radius: 18px;
  }

  .slide-icon {
    font-size: 40px;
  }

  .slide-title {
    font-size: 20px;
  }

  .slide-body {
    font-size: 14px;
  }

  .nav-btn {
    width: 36px;
    height: 36px;
  }

  .nav-btn svg {
    width: 20px;
    height: 20px;
  }

  .fact-grid,
  .region-grid,
  .heritage-grid,
  .food-grid,
  .mountain-grid,
  .animal-grid,
  .summary-cards {
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }

  .app-title {
    font-size: 18px;
  }

  .food-grid,
  .mountain-grid,
  .animal-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .bottom-nav-btn {
    font-size: 12px !important;
    padding: 6px 12px !important;
  }
}

@media (max-width: 420px) {
  .food-grid,
  .mountain-grid,
  .animal-grid {
    grid-template-columns: 1fr 1fr;
  }

  .slide-area {
    gap: 6px;
  }

  .nav-btn {
    width: 30px;
    height: 30px;
  }

  .nav-btn svg {
    width: 16px;
    height: 16px;
  }

  .slide-card {
    padding: 18px 14px;
    min-height: 260px;
  }
}
</style>
