<template>
    <div class="common-list-container">
      <div class="common-header-bar">
        <div class="common-search-bar">
          <el-form :inline="true" :model="searchForm" class="demo-form-inline">
            <el-form-item label="名称">
              <el-input v-model="searchForm.name" placeholder="请输入名称" clearable @input="handleInputSearch"/>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="请选择状态" clearable @change="handleSearch">
                <el-option label="激活" value="active" />
                <el-option label="禁用" value="inactive" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
  
        <div class="common-action-bar">
          <el-button type="primary" @click="showCreateDialog = true">创建示例</el-button>
        </div>
      </div>
  
      <!-- 关键修复：使用计算属性确保数据是数组 -->
      <el-table 
        :data="tableData" 
        style="width: 100%" 
        v-loading="store.loading"
        empty-text="暂无数据"
        :key="tableKey"
      >
        <el-table-column prop="name" label="名称" width="200" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" sortable :formatter="formatDate"/>
        <el-table-column prop="updated_at" label="更新时间" width="160" sortable :formatter="formatDate"/>
  
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="editExample(scope.row.id)">编辑</el-button>
            <el-button size="small" type="danger" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <el-pagination
        v-model:current-page="store.pagination.currentPage"
        v-model:page-size="store.pagination.pageSize"
        :total="store.pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        :background="true"
        layout="total, sizes, prev, pager, next, jumper"
        @update:current-page="handlePageChange"
        @update:page-size="handleSizeChange"
      />
  
      <el-dialog v-model="showCreateDialog" title="创建示例" :before-close="handleDialogClose">
        <ExampleDialog
          :editing-item="null"
          :loading="dialogLoading"
          @submit="handleCreate"
          @cancel="showCreateDialog = false"
        />
      </el-dialog>
  
      <el-dialog v-model="showEditDialog" title="编辑示例" :before-close="handleDialogClose">
        <ExampleDialog
          :editing-item="store.currentExample"
          :loading="dialogLoading"
          @submit="handleUpdate"
          @cancel="showEditDialog = false"
        />
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed, nextTick } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { useExampleStore } from '@/stores/exampleStore'
  import ExampleDialog from '@/components/example/ExampleDialog.vue'
  import { formatDateTime } from '@/utils/date'

  // Store
  const store = useExampleStore()
  
  // 状态
  const dialogLoading = ref(false)
  const showCreateDialog = ref(false)
  const showEditDialog = ref(false)
  const tableKey = ref(0) // 用于强制表格重新渲染
  
  // 搜索表单
  const searchForm = ref({
    name: '',
    status: ''
  })
  
  // 防抖计时器
  let searchTimer = null
  
  // 计算属性确保表格数据是数组
  const tableData = computed(() => {
    // 确保返回的是数组，如果不是则返回空数组
    return Array.isArray(store.examples) ? store.examples : []
  })
  
  // 状态文本映射
  const statusMap = {
    active: '激活',
    inactive: '禁用'
  }
  
  // 获取状态文本
  const getStatusText = (status) => {
    return statusMap[status] || status
  }
  
  // 格式化日期
  const formatDate = (row, column, cellValue) => {
  return cellValue ? formatDateTime(cellValue) : '-'
}
  
  // 强制刷新表格
  const refreshTable = () => {
    tableKey.value += 1
  }
  
  // 对话框关闭处理
  const handleDialogClose = (done) => {
    if (!dialogLoading.value) {
      done()
    }
  }
  
  // 输入搜索处理（防抖）
  const handleInputSearch = () => {
    clearTimeout(searchTimer)
    searchTimer = setTimeout(() => {
      handleSearch()
    }, 500)
  }
  
  // 搜索处理
  const handleSearch = async () => {
    try {
      await store.fetchExamples({
        page: 1,
        name: searchForm.value.name.trim(),
        status: searchForm.value.status
      })
      // 数据更新后刷新表格
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    }
  }
  
  // 重置搜索
  const resetSearch = async () => {
    searchForm.value = { 
      name: '', 
      status: '' 
    }
    try {
      await store.fetchExamples({ page: 1 })
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    }
  }
  
  // 创建示例
  const handleCreate = async (exampleData) => {
    try {
      dialogLoading.value = true
      await store.createExample(exampleData)
      showCreateDialog.value = false
      ElMessage.success('示例创建成功')
      // 创建成功后刷新表格
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    } finally {
      dialogLoading.value = false
    }
  }
  
  // 获取示例详情
  const editExample = async (id) => {
    try {
      await store.fetchExample(id)
      showEditDialog.value = true
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    }
  }
  
  // 更新示例
  const handleUpdate = async (exampleData) => {
    try {
      dialogLoading.value = true
      await store.updateExample(store.currentExample.id, exampleData)
      showEditDialog.value = false
      ElMessage.success('示例更新成功')
      // 更新成功后刷新表格
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    } finally {
      dialogLoading.value = false
    }
  }
  
  // 确认删除
  const confirmDelete = (example) => {
    ElMessageBox.confirm(
      `确定要删除示例 "${example.name}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
      .then(async () => {
        await deleteExample(example)
      })
      .catch(() => {
        ElMessage.info('已取消删除')
      })
  }
  
  // 删除示例
  const deleteExample = async (example) => {
    try {
      await store.deleteExample(example.id)
      ElMessage.success('示例删除成功')
      // 删除成功后刷新表格
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    }
  }
  
  // 分页处理
  const handlePageChange = async (newPage) => {
    try {
      await store.fetchExamples({
        page: newPage,
        name: searchForm.value.name.trim(),
        status: searchForm.value.status
      })
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    }
  }
  
  const handleSizeChange = async (newSize) => {
    try {
      await store.fetchExamples({
        page: 1,
        pageSize: newSize,
        name: searchForm.value.name.trim(),
        status: searchForm.value.status
      })
      nextTick(() => {
        refreshTable()
      })
    } catch (error) {
      if (store.error) {
        ElMessage.error(store.error)
      }
    }
  }
  
  // 组件挂载时获取数据
  onMounted(() => {
    store.fetchExamples().then(() => {
      // 数据加载完成后刷新表格
      nextTick(() => {
        refreshTable()
      })
    }).catch(error => {
      if (store.error) {
        ElMessage.error(store.error)
      }
    })
  })
  </script>
  
  <style scoped>
  .common-list-container {
    padding: 20px;
  }
  
  .common-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
  }
  
  .common-search-bar {
    flex: 1;
  }
  
  .common-action-bar {
    margin-left: 20px;
  }
  
  .el-table {
    margin-bottom: 20px;
  }
  
  .el-pagination {
    display: flex;
    justify-content: flex-end;
  }
  
  :deep(.el-form--inline .el-form-item) {
    margin-right: 16px;
    margin-bottom: 0;
  }
  
  :deep(.el-select) {
    width: 180px;
  }
  
  @media (max-width: 1200px) {
    .common-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      padding: 16px;
      background-color: #f8f9fa;
      border-radius: 4px;
      margin-bottom: 0;
      flex-wrap: wrap;
      gap: 20px;
    }
  
    .common-search-bar {
      width: 100%;
    }
  
    .common-action-bar {
      width: 100%;
      display: flex;
      justify-content: flex-end;
      margin-left: 0;
    }
  }
  
  @media (max-width: 768px) {
    :deep(.el-form--inline .el-form-item) {
      margin-right: 0;
      margin-bottom: 10px;
      width: 100%;
    }
  
    :deep(.el-form--inline .el-form-item__content) {
      width: 100%;
    }
  
    :deep(.el-select) {
      width: 100%;
    }
  }
  </style>