import axios from 'axios'

const API_BASE = '/api/v1'

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Workflows
export const workflowApi = {
  list: (params?: { limit?: number; offset?: number }) =>
    api.get('/workflows', { params }),
  get: (id: string) => api.get(`/workflows/${id}`),
  create: (data: any) => api.post('/workflows', data),
  update: (id: string, data: any) => api.patch(`/workflows/${id}`, data),
  delete: (id: string) => api.delete(`/workflows/${id}`),
}

// Models
export const modelApi = {
  list: (params?: { limit?: number; offset?: number; type?: string }) =>
    api.get('/models', { params }),
  get: (id: string) => api.get(`/models/${id}`),
  create: (data: any) => api.post('/models', data),
  load: (data: any) => api.post('/models/load', data),
  unload: (id: string) => api.post(`/models/${id}/unload`),
  listLoaded: () => api.get('/models/loaded/list'),
}

// Inference
export const inferenceApi = {
  queue: (data: any) => api.post('/inference', data),
  getStatus: (id: string) => api.get(`/inference/${id}`),
  list: (params?: { limit?: number; offset?: number }) =>
    api.get('/inference', { params }),
  cancel: (id: string) => api.post(`/inference/${id}/cancel`),
}

// Health
export const healthApi = {
  check: () => api.get('/health'),
}

export default api