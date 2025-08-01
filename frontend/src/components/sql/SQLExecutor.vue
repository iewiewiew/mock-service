<template>
  <div class="sql-executor">
    <el-card class="query-card">
      <template #header>
        <div class="card-header">
          <span>SQL查询编辑器</span>
          <el-button 
            type="primary" 
            :loading="loading" 
            @click="executeQuery"
            :disabled="!sqlQuery.trim()"
          >
            执行查询
          </el-button>
        </div>
      </template>

      <!-- SQL编辑器 -->
      <el-input
        v-model="sqlQuery"
        type="textarea"
        :rows="8"
        placeholder="请输入SQL查询语句..."
        resize="none"
      />

      <!-- 当前模板显示 -->
      <div v-if="currentTemplate" class="current-template">
        <el-tag type="info">{{ currentTemplate.category }}</el-tag>
        <span class="template-name">{{ currentTemplate.name }}</span>
        <el-button link @click="clearTemplate">清除</el-button>
      </div>

      <!-- 查询结果 - 直接展示原始数据 -->
      <div v-if="queryResult" class="query-result">
        <div class="result-header">
          <span>查询结果 ({{ queryResult.row_count }} 行)</span>
          <span class="execution-time">执行时间: {{ executionTime.toFixed(3) }}s</span>
        </div>
        
        <!-- 直接展示数据 -->
        <div class="raw-data-container" v-loading="loading">
          <pre class="raw-data">{{ formattedData }}</pre>
        </div>
      </div>

      <!-- 错误信息 -->
      <div v-if="errorMessage" class="error-message">
        <el-alert
          :title="errorMessage"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useSQLStore } from '@/stores/sqlStore'

const sqlStore = useSQLStore()

// 响应式数据
const sqlQuery = ref('')
const errorMessage = ref('')

// 计算属性
const loading = computed(() => sqlStore.loading)
const queryResult = computed(() => sqlStore.queryResult)
const executionTime = computed(() => sqlStore.executionTime)
const currentTemplate = computed(() => sqlStore.currentTemplate)

// 格式化数据用于显示
const formattedData = computed(() => {
  if (!queryResult.value || !queryResult.value.data) {
    return '暂无数据'
  }
  
  try {
    return JSON.stringify(queryResult.value.data, null, 2)
  } catch (error) {
    return queryResult.value.data.toString()
  }
})

// 方法
const executeQuery = async () => {
  errorMessage.value = ''
  
  try {
    await sqlStore.executeQuery(sqlQuery.value)
    ElMessage.success('查询执行成功')
  } catch (error) {
    errorMessage.value = error.message || '执行查询时发生错误'
    ElMessage.error('查询执行失败')
  }
}

const clearTemplate = () => {
  sqlStore.setCurrentTemplate(null)
}

// 监听当前模板变化
watch(currentTemplate, (newTemplate) => {
  if (newTemplate) {
    sqlQuery.value = newTemplate.sql_content
  }
})
</script>

<style scoped>
.sql-executor {
  padding: 20px;
}

.query-card {
  min-height: 600px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.current-template {
  margin-top: 10px;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.template-name {
  flex: 1;
  font-weight: 500;
}

.query-result {
  margin-top: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #e4e7ed;
}

.execution-time {
  color: #909399;
  font-size: 12px;
}

.error-message {
  margin-top: 20px;
}

.raw-data-container {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background: #f8f9fa;
  max-height: 400px;
  overflow: auto;
}

.raw-data {
  margin: 0;
  padding: 12px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>