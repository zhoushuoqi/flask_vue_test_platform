import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
  withCredentials: true  // 支持跨域cookies
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    console.log('发送请求:', config.url)
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    console.log('响应成功:', response.config.url, response.status)
    return response
  },
  error => {
    console.log('响应错误:', error.response?.status, error.response?.data, error.config?.url)
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        console.log('收到401错误，跳转登录页')
        window.location.href = '/login'
      }
      ElMessage.error(data.message || '请求失败')
    } else {
      ElMessage.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default request