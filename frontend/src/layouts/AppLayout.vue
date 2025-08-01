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
        <!-- 工作台 -->
        <el-menu-item index="/dashboard" route="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <span>我的工作台</span>
        </el-menu-item>

        <el-menu-divider />

        <!-- 开发工具 -->
        <el-sub-menu index="dev-tools">
          <template #title>
            <el-icon><Connection /></el-icon>
            <span>测试工具</span>
          </template>
          <el-menu-item index="/api-tree" route="/api-tree">
            <el-icon><Connection /></el-icon>
            <span>HTTP接口</span>
          </el-menu-item>
          <el-menu-item index="/mock-list" route="/mock-list">
            <el-icon><icon-menu /></el-icon>
            <span>Mock列表</span>
          </el-menu-item>
          <el-menu-item index="/mock-data" route="/mock-data">
            <el-icon><Tools /></el-icon>
            <span>造数管理</span>
          </el-menu-item>
          <el-menu-item index="/script-management" route="/script-management">
            <el-icon><Document /></el-icon>
            <span>脚本管理</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 环境管理 -->
        <el-sub-menu index="environment-management">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span>环境管理</span>
          </template>
          <el-menu-item index="/environment-list" route="/environment-list">
            <el-icon><Monitor /></el-icon>
            <span>环境列表</span>
          </el-menu-item>
          <el-menu-item index="/linux-info" route="/linux-info">
            <el-icon><Monitor /></el-icon>
            <span>服务器信息</span>
          </el-menu-item>
          <el-menu-item index="/environment-dashboard" route="/environment-dashboard">
            <el-icon><DataBoard /></el-icon>
            <span>环境资源</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 数据管理 -->
        <el-sub-menu index="sql-management">
          <template #title>
            <el-icon><SetUp /></el-icon>
            <span>数据管理</span>
          </template>
          <el-menu-item index="/sql-tool-box/database-conn" route="/sql-tool-box/database-conn">
            <span>数据库连接</span>
          </el-menu-item>
          <el-menu-item index="/sql-tool-box/database-info" route="/sql-tool-box/database-info">
            <span>数据库信息</span>
          </el-menu-item>
          <el-menu-item index="/sql-tool-box" route="/sql-tool-box">
            <span>SQL模板库</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 系统管理 -->
        <el-sub-menu index="system-management">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/project-list" route="/project-list">
            <span>项目列表</span>
          </el-menu-item>
          <el-menu-item index="/users" route="/users">
            <span>用户列表</span>
          </el-menu-item>
          <el-menu-item index="/roles" route="/roles">
            <span>角色列表</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 示例模块 -->
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
              <el-avatar :size="32" class="user-avatar">
                {{ avatarAbbreviation }}
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
import { useAuthStore } from '@/stores/authStore'
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
  SwitchButton,
  
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()


// 用户信息
const username = computed(() => {
  return authStore.user?.username || authStore.user?.name || '用户'
})

// 生成头像缩写（仅首字母）
const getAvatarAbbreviation = (name) => {
  if (!name) return 'U'
  
  // 去除首尾空格后取首字母
  const trimmedName = name.trim()
  if (trimmedName.length === 0) return 'U'
  
  // 判断是否为中文（包含中文字符）
  const hasChinese = /[\u4e00-\u9fa5]/.test(trimmedName)
  
  if (hasChinese) {
    // 中文：取第一个字符
    return trimmedName.charAt(0)
  } else {
    // 英文：取首字母（大写）
    return trimmedName.charAt(0).toUpperCase()
  }
}

const avatarAbbreviation = computed(() => {
  return getAvatarAbbreviation(username.value)
})

// 检查登录状态
const checkAuth = () => {
  // 从 authStore 检查登录状态
  if (!authStore.isAuthenticated || !authStore.user) {
    router.push('/login')
  }
}

// 页面标题映射 - 更新以包含新的路由
const pageTitles = {
  '/dashboard': '我的工作台',
  '/example-list': '示例列表',
  '/example-list2': '示例分类',
  '/users': '用户列表',
  '/roles': '角色列表',
  '/mock-list': 'Mock列表',
  '/project-list': '项目列表',
  '/environment-list': '环境列表',
  '/mock-data': '造数管理',
  '/api-tree': 'HTTP接口',
  '/linux-info': '服务器信息',
  '/sql-tool-box': 'SQL工具箱',
  '/sql-tool-box/database-info': '数据库信息',
  '/sql-tool-box/database-conn': '数据库连接',
  '/script-management': '脚本管理',
  '/environment-dashboard': '环境资源'
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
    authStore.logout()
    
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

<style scoped>
/* 整体布局 */
.app-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: #f0f2f5;
  overflow: hidden;
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
  vertical-align: middle;
}

/* 子菜单项图标 */
:deep(.el-sub-menu .el-menu-item .el-icon) {
  font-size: 14px;
  margin-right: 6px;
}

/* 子菜单样式 */
:deep(.el-sub-menu .el-menu-item) {
  padding-left: 48px !important;
  margin: 2px 8px;
  min-height: 44px;
  line-height: 44px;
}

:deep(.el-sub-menu__title) {
  height: 48px;
  line-height: 48px;
  margin: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s;
  font-weight: 500;
}

:deep(.el-sub-menu__title:hover) {
  background-color: rgba(24, 144, 255, 0.1) !important;
}

:deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: #ffffff !important;
}

:deep(.el-sub-menu.is-opened .el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.9) !important;
}

:deep(.el-sub-menu .el-icon) {
  font-size: 16px;
  margin-right: 8px;
}

/* 菜单分隔线样式 */
:deep(.el-menu-divider) {
  margin: 8px 16px;
  background-color: rgba(255, 255, 255, 0.1);
  height: 1px;
}

/* 右侧内容区 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 240px;
  width: calc(100% - 240px);
  min-height: 100vh;
  overflow: hidden; 
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
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: #333;
  gap: 4px;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.user-avatar {
  margin-right: 10px;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: #fff;
  font-weight: 600;
  flex-shrink: 0;
}

.user-name {
  font-size: 15px;
  font-weight: normal;
  margin-right: 10px;
  color: #262626;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  overflow: hidden;
  min-height: 0; /* 确保flex子元素可以正确收缩 */
  max-height: 100%; /* 限制最大高度 */
  display: flex;
  flex-direction: column;
}

/* 确保router-view正确继承高度 */
.content > * {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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
    max-width: 80px;
    font-size: 14px;
  }
  
  .top-navbar {
    padding: 12px 16px;
  }
}

@media (max-width: 480px) {
  .user-name {
    display: none;
  }
  
  .user-avatar {
    margin-right: 4px;
  }
}

/* 面包屑样式调整 */
:deep(.el-breadcrumb) {
  line-height: 1.5;
  font-size: 14px;
}
</style>