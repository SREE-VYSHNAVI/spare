import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      return Promise.reject(new Error(error.response.data?.detail || error.response.statusText))
    } else if (error.request) {
      return Promise.reject(new Error('No response from server'))
    } else {
      return Promise.reject(new Error(error.message))
    }
  }
)