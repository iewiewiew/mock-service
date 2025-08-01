import axios from 'axios'

const baseURL = process.env.NODE_ENV === 'production' 
    ? 'http://114.67.240.27:5001/api' 
    : 'http://localhost:5001/api';

const apiClient = axios.create({
    baseURL,
    withCredentials: false,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    maxRedirects: 0, // 防止自动重定向
    timeout: 10000 // 添加超时设置
})

// 请求拦截器
apiClient.interceptors.request.use(config => {
    // 规范化URL，防止双斜杠
    config.url = config.url.replace(/([^:]\/)\/+/g, '$1')
    return config
}, error => {
    return Promise.reject(error)
})

// 响应拦截器
apiClient.interceptors.response.use(response => {
    return response
}, error => {
    // 统一错误处理
    if (error.response) {
        console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
        console.error('API Error: No response received')
    } else {
        console.error('API Error:', error.message)
    }
    return Promise.reject(error)
})

export default apiClient