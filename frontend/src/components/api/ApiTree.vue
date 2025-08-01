<template>
  <div class="api-tree">
    <div class="tree-header">
      <el-input v-model="searchKeyword" placeholder="搜索接口..." clearable size="default" @clear="handleSearchClear"
        @input="handleSearchInput">
        <template #prefix>
          <el-icon>
            <Search />
          </el-icon>
        </template>
      </el-input>
      <el-button-group class="tree-actions">
        <el-tooltip content="刷新文档" placement="top">
          <el-button @click="handleRefresh" :loading="loading" size="default">
            <el-icon>
              <Refresh />
            </el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="展开全部" placement="top">
          <el-button @click="expandAll" size="default" :disabled="treeData.length === 0">
            <el-icon>
              <Expand />
            </el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="折叠全部" placement="top">
          <el-button @click="collapseAll" size="default" :disabled="treeData.length === 0">
            <el-icon>
              <Fold />
            </el-icon>
          </el-button>
        </el-tooltip>
      </el-button-group>
    </div>

    <el-alert v-if="error" :title="error" type="error" show-icon closable @close="clearError" class="error-alert" />

    <div class="tree-container" v-loading="loading">
      <div v-if="!loading && treeData.length === 0" class="empty-state">
        <el-empty description="暂无接口数据" :image-size="80" />
        <el-button @click="handleRefresh" type="primary" size="small">刷新数据</el-button>
      </div>

      <el-tree v-else ref="treeRef" :data="filteredTreeData" :props="defaultProps" node-key="id"
        :default-expanded-keys="defaultExpandedKeys" :highlight-current="true" :expand-on-click-node="false"
        @node-click="handleNodeClick" class="api-tree-content">
        <template #default="{ node, data }">
          <span class="tree-node">
            <span v-if="data.type === 'category'" class="category-node">
              <el-icon>
                <component :is="node.expanded ? 'FolderOpened' : 'Folder'" />
              </el-icon>
              <span class="category-label">{{ data.label }}</span>
              <el-tag size="small" type="info" class="count-tag">
                {{ data.children?.length || 0 }}
              </el-tag>
            </span>
            <span v-else class="api-item">
              <el-tag :type="getMethodType(data.method)" size="small" class="method-tag" effect="dark">
                {{ data.method }}
              </el-tag>
              <div class="api-info">
                <div class="api-name">{{ getApiName(data) }}</div>
              </div>
            </span>
          </span>
        </template>
      </el-tree>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useEndpointStore } from '@/stores/endpointStore'
import {
  ElTree,
  ElInput,
  ElButton,
  ElButtonGroup,
  ElTag,
  ElAlert,
  ElIcon,
  ElTooltip,
  ElMessage,
  ElEmpty
} from 'element-plus'
import {
  Refresh,
  Search,
  Folder,
  FolderOpened,
  Expand,
  Fold
} from '@element-plus/icons-vue'

// 使用 store
const endpointStore = useEndpointStore()
const {
  treeData,
  filteredTreeData,
  loading,
  error,
  searchKeyword
} = storeToRefs(endpointStore)

// 定义 emits
const emit = defineEmits(['endpoint-selected'])

// 响应式数据
const treeRef = ref()
const defaultExpandedKeys = ref([])

// 计算属性
const defaultProps = computed(() => ({
  children: 'children',
  label: 'label'
}))

// 方法
const getMethodType = (method) => {
  const types = {
    'GET': 'success',
    'POST': 'warning',
    'PUT': 'primary',
    'DELETE': 'danger',
    'PATCH': 'info',
    'HEAD': 'info',
    'OPTIONS': 'info'
  }
  return types[method?.toUpperCase()] || 'info'
}

// 在 ApiTree.vue 的 getApiName 方法中，使用相同的逻辑
const getApiName = (data) => {
  if (!data) return '未知接口'

  // 1. 检查 operation 对象
  if (data.operation) {
    if (data.operation.summary) return data.operation.summary
    if (data.operation.operationId) return data.operation.operationId
    if (data.operation.description) return data.operation.description
  }

  // 2. 检查直接字段
  if (data.summary) return data.summary
  if (data.name) return data.name
  if (data.label) return data.label
  if (data.operationId) return data.operationId
  if (data.description) return data.description
  if (data.title) return data.title

  // 3. 使用路径生成名称
  if (data.path) {
    const pathParts = data.path.split('/').filter(part => part && !part.includes('{'))
    return pathParts[pathParts.length - 1] || data.path
  }

  return '未命名接口'
}

const handleNodeClick = async (data, node) => {
  if (data.type === 'endpoint') {
    try {
      // 直接传递整个接口数据
      emit('endpoint-selected', data)
    } catch (error) {
      ElMessage.error('选择接口失败: ' + error.message)
    }
  } else if (data.type === 'category') {
    node.expanded ? node.collapse() : node.expand()
  }
}

const handleRefresh = async () => {
  try {
    await endpointStore.refreshApiDocs()
    ElMessage.success('文档刷新成功')
    collapseAll()
  } catch (error) {
    ElMessage.error('刷新文档失败: ' + error.message)
  }
}

const handleSearchClear = () => {
  endpointStore.setSearchKeyword('')
}

const handleSearchInput = (value) => {
  endpointStore.setSearchKeyword(value)

  if (value.trim()) {
    nextTick(() => {
      expandAll()
    })
  } else {
    collapseAll()
  }
}

const clearError = () => {
  endpointStore.clearError()
}

// 展开所有节点
const expandAll = () => {
  if (treeRef.value) {
    const nodes = treeRef.value.store._getAllNodes()
    nodes.forEach(node => {
      node.expanded = true
    })
  }
}

// 折叠所有节点
const collapseAll = () => {
  if (treeRef.value) {
    const nodes = treeRef.value.store._getAllNodes()
    nodes.forEach(node => {
      node.expanded = false
    })
  }
}

// 生命周期
onMounted(() => {
  endpointStore.fetchEndpointsByCategories().catch(error => {
    ElMessage.error('加载接口数据失败: ' + error.message)
  })
})
</script>

<style scoped>
.api-tree {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.tree-header {
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  gap: 8px;
  align-items: center;
  background: #f8f9fa;
  flex-shrink: 0;
}

.tree-header .el-input {
  flex: 1;
}

.tree-actions {
  display: flex;
  gap: 4px;
}

.error-alert {
  margin: 8px 16px 0;
  flex-shrink: 0;
}

.tree-container {
  flex: 1;
  overflow: auto;
  padding: 8px 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  gap: 16px;
  color: #909399;
  padding: 0 20px;
}

:deep(.api-tree-content) {
  padding: 0 8px;
}

:deep(.api-tree-content .el-tree-node__content) {
  height: auto;
  min-height: 36px;
  margin: 2px 0;
  border-radius: 6px;
  transition: all 0.2s ease;
  padding: 4px 8px;
}

:deep(.api-tree-content .el-tree-node__content:hover) {
  background-color: #f5f7fa;
}

:deep(.api-tree-content .el-tree-node.is-current > .el-tree-node__content) {
  background-color: #f0f7ff;
  border: 1px solid #409eff;
}

:deep(.api-tree-content .el-tree-node__expand-icon) {
  color: #909399;
  transition: transform 0.2s ease;
}

:deep(.api-tree-content .el-tree-node__expand-icon.is-leaf) {
  color: transparent;
  cursor: default;
}

.tree-node {
  display: flex;
  align-items: center;
  width: 100%;
  font-size: 14px;
}

.category-node {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: #409eff;
  flex: 1;
  padding: 4px 0;
}

.category-node .el-icon {
  color: #e6a23c;
  font-size: 16px;
}

.category-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
}

.count-tag {
  min-width: 20px;
  height: 18px;
  justify-content: center;
  flex-shrink: 0;
  font-size: 11px;
}

.api-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  width: 100%;
  padding: 6px 0;
}

.method-tag {
  min-width: 48px;
  text-align: center;
  font-weight: 600;
  font-size: 10px;
  flex-shrink: 0;
  margin-top: 1px;
}

.api-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.api-name {
  font-size: 13px;
  font-weight: 500;
  color: #303133;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.api-path {
  font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 11px;
  color: #909399;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tree-container::-webkit-scrollbar {
  width: 6px;
}

.tree-container::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 3px;
}

.tree-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.tree-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>