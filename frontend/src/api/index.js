import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// 省份相关
export const getProvinceList = (region) =>
  api.get('/provinces/', { params: { region } }).then(r => r.data.data)

export const getProvinceDetail = (id) =>
  api.get(`/provinces/${id}/`).then(r => r.data.data)

export const getRegionList = () =>
  api.get('/regions/').then(r => r.data.data)

export const getQuizQuestions = (count = 10) =>
  api.get('/quiz/', { params: { count } }).then(r => r.data.data)

export const getMatchingData = (mode = 'capital') =>
  api.get('/matching/', { params: { mode } }).then(r => r.data)

export const getPuzzleData = () =>
  api.get('/puzzle/').then(r => r.data.data)

export const getGalleryData = () =>
  api.get('/gallery/').then(r => r.data.data)

export const healthCheck = () =>
  api.get('/health/').then(r => r.data)

export default api
