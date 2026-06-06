import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getProvinceList, getProvinceDetail } from '@/api'

export const useGameStore = defineStore('game', () => {
  const score = ref(parseInt(localStorage.getItem('quizScore') || '0'))
  const visitedProvinces = ref(JSON.parse(localStorage.getItem('visitedProvinces') || '[]'))
  const provinces = ref([])
  const loading = ref(false)

  const visitedCount = computed(() => visitedProvinces.value.length)
  const totalProvinces = computed(() => provinces.value.length)

  function addScore(points) {
    score.value += points
    localStorage.setItem('quizScore', score.value.toString())
  }

  function visitProvince(id) {
    if (!visitedProvinces.value.includes(id)) {
      visitedProvinces.value.push(id)
      localStorage.setItem('visitedProvinces', JSON.stringify(visitedProvinces.value))
    }
  }

  function isVisited(id) {
    return visitedProvinces.value.includes(id)
  }

  async function loadProvinces(region) {
    loading.value = true
    try {
      provinces.value = await getProvinceList(region)
    } finally {
      loading.value = false
    }
  }

  function resetScore() {
    score.value = 0
    localStorage.setItem('quizScore', '0')
  }

  return {
    score, visitedProvinces, provinces, loading,
    visitedCount, totalProvinces,
    addScore, visitProvince, isVisited, loadProvinces, resetScore,
  }
})
