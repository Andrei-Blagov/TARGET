import axios from 'axios'

// Пустой baseURL в production: запросы идут на тот же origin (Nginx → backend)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  timeout: 300000,
})


export async function analyzeSite(url) {
  const { data } = await api.post('/llm/analyze-site', { url })
  return data
}

export function getErrorMessage(error) {
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail
    return typeof detail === 'string' ? detail : JSON.stringify(detail)
  }
  if (error.message) return error.message
  return 'Неизвестная ошибка'
}
