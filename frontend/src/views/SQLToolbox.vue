<template>
    <div class="sql-toolbox">
      <el-container class="toolbox-container">
        <!-- 侧边栏 - SQL模板 -->
        <el-aside width="300px" class="sidebar">
          <SQLTemplates 
            @template-select="handleTemplateSelect"
            @template-edit="handleTemplateEdit"
          />
        </el-aside>
  
        <!-- 主内容区 -->
        <el-main class="main-content">
          <el-tabs v-model="activeTab" type="border-card">
            <!-- SQL执行标签页 -->
            <el-tab-pane label="SQL执行" name="execute">
              <SQLExecutor />
            </el-tab-pane>
  
            <!-- 模板管理标签页 -->
            <el-tab-pane label="模板管理" name="templates">
              <TemplateManager />
            </el-tab-pane>
  
            <!-- 查询历史标签页 -->
            <el-tab-pane label="查询历史" name="history">
              <QueryHistory />
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>
  
      <!-- 模板编辑对话框 -->
      <TemplateDialog 
        v-model="templateDialogVisible"
        :template="editingTemplate"
        @success="handleTemplateSuccess"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useSQLStore } from '@/stores/sqlStore'
  
  // 组件导入
  import SQLTemplates from '@/components/sql/SQLTemplates.vue'
  import SQLExecutor from '@/components/sql/SQLExecutor.vue'
  import TemplateManager from '@/components/sql/TemplateManager.vue'
  import QueryHistory from '@/components/sql/QueryHistory.vue'
  import TemplateDialog from '@/components/sql/TemplateDialog.vue'
  
  const sqlStore = useSQLStore()
  
  // 响应式数据
  const activeTab = ref('execute')
  const templateDialogVisible = ref(false)
  const editingTemplate = ref(null)
  
  // 方法
  const handleTemplateSelect = (template) => {
    sqlStore.setCurrentTemplate(template)
    activeTab.value = 'execute'
  }
  
  const handleTemplateEdit = (template) => {
    editingTemplate.value = template
    templateDialogVisible.value = true
  }
  
  const handleTemplateSuccess = () => {
    templateDialogVisible.value = false
    editingTemplate.value = null
    sqlStore.loadTemplates()
  }
  
  // 生命周期
  onMounted(() => {
    sqlStore.loadTemplates()
    sqlStore.loadHistory()
  })
  </script>
  
  <style scoped>
  .sql-toolbox {
    height: 100vh;
    background: #f5f7fa;
  }
  
  .toolbox-container {
    height: 100%;
  }
  
  .sidebar {
    background: white;
    border-right: 1px solid #e4e7ed;
    padding: 0;
  }
  
  .main-content {
    padding: 0;
    background: white;
  }
  
  :deep(.el-tabs__content) {
    padding: 0;
  }
  </style>