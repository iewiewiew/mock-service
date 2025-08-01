import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import LoginView2 from '@/views/LoginView.vue'
import UserView from '@/views/UserView.vue'
import RoleView from '@/views/RoleView.vue'
import Dashboard from '@/views/Dashboard.vue'
import ExampleView from '@/views/ExampleView.vue'
import ExampleView2 from '@/views/ExampleView2.vue'
import MockListView from '@/views/MockListView.vue'
import ProjectListView from '@/views/ProjectListView.vue'
import ApiDocumentation from '@/views/ApiDocView.vue'
import EnvironmentView from '@/views/EnvironmentView.vue'
import MockDataView from '@/views/MockDataView.vue'
import LinuxInfoView from '@/views/LinuxInfoView.vue'
import EnvironmentDashboardView from '@/views/EnvironmentDashboardView.vue'
import SQLToolbox from '@/views/SQLToolbox.vue'
import DatabaseConnView from '@/views/DatabaseConnView.vue'
import DatabaseInfoView from '@/views/DatabaseInfoView.vue'
import ScriptManagementView from '@/views/ScriptManagementView.vue'
import { useAuthStore } from '@/stores/authStore';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView2,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: AppLayout,
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: '/users',
        name: 'Users',
        component: UserView
      },
      {
        path: '/roles',
        name: 'Roles',
        component: RoleView
      },
      {
        path: '/example-list',
        name: 'ExampleView',
        component: ExampleView
      },
      {
        path: '/example-list2',
        name: 'ExampleView2',
        component: ExampleView2
      },
      {
        path: '/mock-list',
        name: 'MockList',
        component: MockListView
      },
      {
        path: '/project-list',
        name: 'ProjectList',
        component: ProjectListView
      },
      {
        path: '/environment-list',
        name: 'EnvironmentView',
        component: EnvironmentView
      },
      {
        path: '/mock-data',
        name: 'MockDataView',
        component: MockDataView
      },
      {
        path: '/api-tree',
        name: 'ApiTree',
        component: ApiDocumentation
      },
      {
        path: '/linux-info',
        name: 'LinuxInfo',
        component: LinuxInfoView
      },
      {
        path: '/environment-dashboard',
        name: 'EnvironmentDashboard',
        component: EnvironmentDashboardView
      },
      {
        path: '/sql-tool-box',
        name: 'SQLToolbox',
        component: SQLToolbox
      },
      {
        path: '/sql-tool-box/database-conn',
        name: 'DatabaseConn',
        component: DatabaseConnView
      },
      {
        path: '/sql-tool-box/database-info',
        name: 'DatabaseInfo',
        component: DatabaseInfoView
      },
      {
        path: '/script-management',
        name: 'ScriptManagement',
        component: ScriptManagementView
      }
    ]
  },
  // 404 页面处理
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  console.log('🛡️ 路由守卫 - 导航:', from.path, '->', to.path);
  console.log('🔑 路由守卫 - 认证状态:', authStore.isAuthenticated);
  console.log('📝 路由守卫 - 目标路由元信息:', to.meta);

  // 如果需要认证的页面
  if (to.meta.requiresAuth) {
    if (authStore.isAuthenticated) {
      // 已认证，检查 token 是否有效
      try {
        const isValid = await authStore.checkAuth();
        if (isValid) {
          console.log('✅ 路由守卫 - Token 有效，允许访问');
          next();
        } else {
          console.log('❌ 路由守卫 - Token 无效，跳转到登录页');
          // 关键修复：记录当前要访问的页面，而不是跳转到 dashboard
          const returnUrl = encodeURIComponent(to.fullPath);
          next(`/login?returnUrl=${returnUrl}`);
        }
      } catch (error) {
        console.error('🚨 路由守卫 - 认证检查错误:', error);
        // 关键修复：记录当前要访问的页面
        const returnUrl = encodeURIComponent(to.fullPath);
        next(`/login?returnUrl=${returnUrl}`);
      }
    } else {
      console.log('❌ 路由守卫 - 未认证，跳转到登录页');
      // 关键修复：记录当前要访问的页面，而不是跳转到 dashboard
      const returnUrl = encodeURIComponent(to.fullPath);
      next(`/login?returnUrl=${returnUrl}`);
    }
  }
  // 如果要求未登录的页面（如登录页）
  else if (to.meta.requiresGuest) {
    if (authStore.isAuthenticated) {
      console.log('✅ 路由守卫 - 已登录，检查返回URL');
      
      // 关键修复：优先使用返回URL，没有则保持当前页面逻辑
      const returnUrl = to.query.returnUrl;
      if (returnUrl) {
        // 解码并跳转到原页面
        const targetPath = decodeURIComponent(returnUrl);
        console.log('🔀 路由守卫 - 跳转到返回URL:', targetPath);
        
        // 确保目标路径是有效的应用内路径
        if (targetPath.startsWith('/') && targetPath !== '/login') {
          next(targetPath);
        } else {
          next('/dashboard');
        }
      } else {
        // 没有返回URL，检查是否从其他页面跳转过来
        if (from.path !== '/' && from.path !== '/login' && from.meta.requiresAuth) {
          console.log('🔀 路由守卫 - 跳转回来源页面:', from.path);
          next(from.path);
        } else {
          console.log('🔀 路由守卫 - 跳转到默认页面');
          next('/dashboard');
        }
      }
    } else {
      console.log('✅ 路由守卫 - 未登录，允许访问登录页');
      next();
    }
  }
  // 其他页面（没有元信息的页面）
  else {
    console.log('✅ 路由守卫 - 公共页面，允许访问');
    next();
  }
})

// 路由错误处理
router.onError((error) => {
  console.error('❌ 路由错误:', error);
})

export default router;