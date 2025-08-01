import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import LoginView from '@/views/LoginView.vue'
import Dashboard from '@/views/Dashboard.vue'
import ExampleView from '@/views/ExampleView.vue'
import ExampleView2 from '@/views/ExampleView2.vue'
import MockListView from '@/views/MockListView.vue'
import ProjectListView from '@/views/ProjectListView.vue'
import ApiDocumentation from '@/views/ApiDocView.vue'
import EnvironmentView from '@/views/EnvironmentView.vue'
import MockDataView from '@/views/MockDataView.vue'
import LinuxInfoView from '@/views/LinuxInfoView.vue'
import SQLToolbox from '@/views/SQLToolbox.vue'


const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/',
    component: AppLayout,
    redirect: '/mock-list',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'example-list',
        name: 'ExampleView',
        component: ExampleView
      },
      {
        path: 'example-list2',
        name: 'ExampleView2',
        component: ExampleView2
      },
      {
        path: 'mock-list',
        name: 'MockList',
        component: MockListView
      },
      {
        path: 'project-list',
        name: 'ProjectList',
        component: ProjectListView
      },
      {
        path: 'environment-list',
        name: 'EnvironmentView',
        component: EnvironmentView
      },
      {
        path: 'mock-data',
        name: 'MockDataView',
        component: MockDataView
      },
      {
        path: 'api-tree',
        name: 'ApiTree',
        component: ApiDocumentation
      },
      {
        path: 'linux-info',
        name: 'LinuxInfo',
        component: LinuxInfoView
      },
      {
        path: 'sql-tool-box',
        name: 'SQLToolbox',
        component: SQLToolbox
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router