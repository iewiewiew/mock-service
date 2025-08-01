<template>
  <div class="app-container">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">Test<span class="logo-highlight">Platform</span></div>
        <div class="logo-subtitle">测试平台</div>
      </div>

      <el-menu :default-active="activeMenu" router class="sidebar-menu" background-color="#001529" text-color="#b7bdc3"
        active-text-color="#ffffff">
        <!-- 我的工作台 -->
        <el-menu-item index="/dashboard" route="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <span>我的工作台</span>
        </el-menu-item>

        <!-- 示例模块子菜单 -->
        <el-sub-menu index="example-management">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>示例模块</span>
          </template>
          <el-menu-item index="/example-list" route="/example-list">
            <span>示例列表</span>
          </el-menu-item>
          <el-menu-item index="/example-list2" route="/example-list2">
            <span>示例分类</span>
          </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/mock-list" route="/mock-list">
          <el-icon><icon-menu /></el-icon>
          <span>接口列表</span>
        </el-menu-item>
        <el-menu-item index="/project-list" route="/project-list">
          <el-icon>
            <FolderOpened />
          </el-icon>
          <span>项目列表</span>
        </el-menu-item>
        <el-menu-item index="/environment-list" route="/environment-list">
          <el-icon>
            <Setting />
          </el-icon>
          <span>环境管理</span>
        </el-menu-item>
        <el-menu-item index="/mock-data" route="/mock-data">
          <el-icon>
            <Tools />
          </el-icon>
          <span>造数管理</span>
        </el-menu-item>
        <el-menu-item index="/api-tree" route="/api-tree">
          <el-icon>
            <Connection />
          </el-icon>
          <span>API接口</span>
        </el-menu-item>
        <el-menu-item index="/linux-info" route="/linux-info">
          <el-icon>
            <Monitor />
          </el-icon>
          <span>Linux服务器</span>
        </el-menu-item>
        <el-menu-item index="/sql-tool-box" route="/sql-tool-box">
          <el-icon>
            <SetUp />
          </el-icon>
          <span>SQL工具箱</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 右侧内容区 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="top-navbar">
        <div class="navbar-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ pageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="navbar-right">
          <el-dropdown @command="handleCommand" class="user-dropdown">
            <span class="user-info">
              <el-avatar :size="32" :src="userAvatar" class="user-avatar">
                {{ username.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="user-name">{{ username }}</span>
              <el-icon class="dropdown-icon"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 页面内容 -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Document,
  DataBoard,
  Menu as IconMenu, 
  FolderOpened, 
  Setting, 
  Connection, 
  Tools, 
  Monitor,
  SetUp,
  User,
  ArrowDown,
  SwitchButton
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 用户信息
const username = ref('')
const userAvatar = ref('')

// 检查登录状态
const checkAuth = () => {
  const isLoggedIn = localStorage.getItem('isLoggedIn')
  const savedUsername = localStorage.getItem('username')
  
  if (!isLoggedIn || isLoggedIn !== 'true') {
    router.push('/login')
  } else {
    username.value = savedUsername || '管理员'
    // 生成默认头像（可以根据用户名生成不同的颜色）
    generateDefaultAvatar()
  }
}

// 生成默认头像
const generateDefaultAvatar = () => {
  // 这里可以使用第三方头像服务，或者生成基于用户名的彩色头像
  const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']
  const colorIndex = username.value.length % colors.length
  // 实际项目中可以使用彩色背景+首字母的方式
  userAvatar.value = '' // 设置为空，使用el-avatar的默认样式
}

// 页面标题映射 - 更新以包含新的路由
const pageTitles = {
  '/dashboard': '我的工作台',
  '/example-list': '示例列表',
  '/example-list2': '示例分类',
  '/mock-list': '接口列表',
  '/project-list': '项目列表',
  '/environment-list': '环境管理',
  '/mock-data': '造数管理',
  '/api-tree': 'API接口',
  '/linux-info': 'Linux服务器'
}

const pageTitle = computed(() => pageTitles[route.path] || 'Mock 系统')
const activeMenu = computed(() => route.path)

// 处理下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中...')
      break
    case 'logout':
      await handleLogout()
      break
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    // 清除登录状态
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('username')
    
    ElMessage.success('退出登录成功')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    // 用户取消退出
    console.log('取消退出登录')
  }
}

// 页面加载时检查认证状态
onMounted(() => {
  checkAuth()
})
</script>

<!-- 样式部分保持不变 -->

<style scoped>
/* 整体布局 */
.app-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: #f0f2f5;
}

/* 左侧导航栏 */
.sidebar {
  width: 240px;
  min-width: 240px;
  max-width: 240px;
  background-color: #001529;
  color: #fff;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px 0 rgba(29, 35, 41, 0.1);
}

/* Logo区域 */
.logo-container {
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.5;
}

.logo-highlight {
  color: #1890ff;
}

.logo-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.65);
  margin-top: 4px;
}

/* 菜单样式 */
.sidebar-menu {
  border-right: none;
  width: 100%;
  flex: 1;
}

:deep(.el-menu-item) {
  height: 48px;
  line-height: 48px;
  margin: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s;
}

:deep(.el-menu-item:hover) {
  background-color: rgba(24, 144, 255, 0.1) !important;
}

:deep(.el-menu-item.is-active) {
  background-color: #1890ff !important;
  color: #fff !important;
}

:deep(.el-menu-item .el-icon) {
  font-size: 16px;
  margin-right: 8px;
}

/* 子菜单样式 */
:deep(.el-sub-menu .el-menu-item) {
  padding-left: 48px !important;
  margin: 2px 8px;
}

:deep(.el-sub-menu__title) {
  height: 48px;
  line-height: 48px;
  margin: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s;
}

:deep(.el-sub-menu__title:hover) {
  background-color: rgba(24, 144, 255, 0.1) !important;
}

:deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: #ffffff !important;
}

:deep(.el-sub-menu .el-icon) {
  font-size: 16px;
  margin-right: 8px;
}

/* 右侧内容区 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 240px;
  width: calc(100% - 240px);
  min-height: 100vh;
}

/* 顶部导航栏 */
.top-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: #fff;
  border-bottom: 1px solid #e8e8e8;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  height: 60px;
  box-sizing: border-box;
}

.navbar-left {
  flex: 1;
}

.navbar-right {
  display: flex;
  align-items: center;
}

/* 用户信息下拉菜单 */
.user-info {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  color: #333;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.user-avatar {
  margin-right: 8px;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: #fff;
  font-weight: 600;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  margin-right: 8px;
}

.dropdown-icon {
  color: #999;
  font-size: 12px;
  transition: transform 0.3s;
}

.user-dropdown:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 下拉菜单样式 */
:deep(.el-dropdown-menu) {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  font-size: 14px;
}

:deep(.el-dropdown-menu__item .el-icon) {
  margin-right: 8px;
  font-size: 16px;
}

:deep(.el-dropdown-menu__item--divided) {
  border-top: 1px solid #f0f0f0;
}

:deep(.el-dropdown-menu__item:not(.is-disabled):hover) {
  background-color: #f5f7fa;
  color: #1890ff;
}

/* 内容区域 */
.content {
  flex: 1;
  padding: 16px;
  background-color: #f0f2f5;
  overflow: auto;
}

/* 滚动条美化 */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-track {
  background-color: transparent;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .sidebar {
    width: 200px;
    min-width: 200px;
    max-width: 200px;
  }

  .main-container {
    margin-left: 200px;
    width: calc(100% - 200px);
  }
  
  .user-name {
    display: none;
  }
  
  .top-navbar {
    padding: 12px 16px;
  }
}

/* 面包屑样式调整 */
:deep(.el-breadcrumb) {
  line-height: 1.5;
  font-size: 14px;
}
</style>