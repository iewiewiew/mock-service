<template>
  <div class="login-container">
    <div class="login-background">
      <div class="login-box">
        <!-- Logo区域 -->
        <div class="login-header">
          <div class="login-logo">Test<span class="logo-highlight">Platform</span></div>
          <div class="login-subtitle">测试平台</div>
        </div>

        <!-- 登录表单 -->
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" class="login-form" @submit.prevent="handleLogin">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" size="large" :prefix-icon="User"/>
          </el-form-item>

          <el-form-item prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" size="large" :prefix-icon="Lock" show-password @keyup.enter="handleLogin"/>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" size="large" class="login-button" :loading="loading" @click="handleLogin"> {{ loading ? '登录中...' : '登录' }} </el-button>
          </el-form-item>
        </el-form>

        <!-- 底部信息 -->
        <div class="login-footer">
          <div class="footer-text">欢迎使用测试平台</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)

// 登录表单数据 - 设置默认值
const loginForm = reactive({
  username: 'admin',
  password: '123456'
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const loginFormRef = ref()

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  const valid = await loginFormRef.value.validate()
  if (!valid) return

  loading.value = true

  try {
    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 验证用户名和密码
    if (loginForm.username === 'admin' && loginForm.password === '123456') {
      ElMessage.success('登录成功')
      // 存储登录状态
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('username', loginForm.username)
      
      // 跳转到首页
      router.push('/')
    } else {
      ElMessage.error('用户名或密码错误')
    }
  } catch (error) {
    ElMessage.error('登录失败，请重试')
  } finally {
    loading.value = false
  }
}

// 组件挂载时自动填充默认值
onMounted(() => {
  // 如果表单引用存在，清除验证状态
  if (loginFormRef.value) {
    loginFormRef.value.clearValidate()
  }
})
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.login-background {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-box {
  width: 400px;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-logo {
  font-size: 32px;
  font-weight: 700;
  color: #001529;
  line-height: 1.2;
}

.logo-highlight {
  color: #1890ff;
}

.login-subtitle {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

.login-form {
  margin-bottom: 20px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-input__inner) {
  border-radius: 8px;
}

.login-button {
  width: 100%;
  border-radius: 8px;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  border: none;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.demo-title {
  font-size: 14px;
  font-weight: 600;
  color: #8b7355;
  margin-bottom: 8px;
}

.account-info {
  display: flex;
  justify-content: space-around;
  font-size: 13px;
  color: #666;
}

.account-info strong {
  color: #1890ff;
  font-weight: 600;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.footer-text {
  color: #999;
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-box {
    width: 100%;
    margin: 20px;
    padding: 30px 20px;
  }
  
  .login-logo {
    font-size: 28px;
  }
  
  .account-info {
    flex-direction: column;
    gap: 4px;
  }
}

/* 输入框获得焦点时的样式 */
:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #1890ff inset;
}

/* 加载按钮样式 */
:deep(.el-button--primary.is-loading) {
  opacity: 0.8;
}
</style>