<template>
  <!-- 环境列表 -->
  <div class="common-list-container">
    <!-- 搜索区域 -->
    <div class="common-header-bar">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline" label-width="auto">
          <el-form-item label="环境名称">
            <el-input v-model="searchForm.name" placeholder="请输入环境名称" clearable @input="handleInputSearch" />
          </el-form-item>
          <el-form-item label="基础URL">
            <el-input v-model="searchForm.base_url" placeholder="请输入基础URL" clearable @input="handleInputSearch" />
          </el-form-item>
          <el-form-item>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="common-action-bar">
        <el-button type="primary" @click="showEnvironmentDialog()">创建环境</el-button>
      </div>
    </div>

    <!-- 环境表格 -->
    <el-table :data="environmentStore.environments" v-loading="environmentStore.loading" style="width: 100%"
      empty-text="暂无环境数据">
      <el-table-column prop="name" label="环境名称" min-width="120" show-overflow-tooltip />
      <el-table-column prop="base_url" label="基础URL" min-width="200" show-overflow-tooltip />
      <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
      <el-table-column prop="parameter_count" label="参数数量" width="100">
        <template #default="scope">
          <el-link type="primary" @click="showParameterDialog(scope.row)">
            {{ scope.row.parameter_count }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160" :formatter="formatDate" />
      <el-table-column prop="updated_at" label="更新时间" width="160" :formatter="formatDate" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="showEnvironmentDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDeleteEnvironment(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[10, 20, 50, 100]"
        :total="environmentStore.pagination.total" :background="true" layout="total, sizes, prev, pager, next, jumper"
        @update:current-page="handlePageChange" @update:page-size="handleSizeChange" />
    </div>
  </div>

  <!-- 环境编辑对话框 -->
  <el-dialog v-model="environmentDialog.visible" :title="environmentDialog.isEdit ? '编辑环境' : '创建环境'" width="500px">
    <el-form ref="environmentFormRef" :model="environmentDialog.form" :rules="environmentRules" label-width="100px">
      <el-form-item label="环境名称" prop="name">
        <el-input v-model="environmentDialog.form.name" placeholder="请输入环境名称" />
      </el-form-item>
      <el-form-item label="基础URL" prop="base_url">
        <el-input v-model="environmentDialog.form.base_url" placeholder="请输入基础URL" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="environmentDialog.form.description" type="textarea" :rows="3" placeholder="请输入环境描述" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="environmentDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleEnvironmentSubmit">确定</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 参数管理对话框 -->
  <el-dialog v-model="parameterDialog.visible" :title="`${parameterDialog.environmentName} - 参数管理`" width="800px">
    <!-- 参数搜索 -->
    <div class="header-bar">
      <div class="search-bar">
        <el-form :inline="true" :model="parameterSearchForm" class="demo-form-inline" label-width="auto">
          <el-form-item label="参数键">
            <el-input v-model="parameterSearchForm.param_key" placeholder="请输入参数键" clearable
              @input="handleParameterInputSearch" style="width: 180px" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="parameterSearchForm.description" placeholder="请输入描述" clearable
              @input="handleParameterInputSearch" style="width: 180px" />
          </el-form-item>
          <el-form-item>
            <el-button @click="resetParameterSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="action-bar">
        <el-button type="primary" @click="showParameterEditDialog()">新增参数</el-button>
      </div>
    </div>

    <!-- 参数表格 -->
    <el-table :data="environmentStore.parameters" v-loading="environmentStore.loading" style="width: 100%"
      empty-text="暂无参数数据">
      <el-table-column prop="param_key" label="参数键" min-width="120" show-overflow-tooltip />
      <el-table-column prop="param_value" label="参数值" min-width="200" show-overflow-tooltip />
      <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="160" :formatter="formatDate" />
      <el-table-column prop="created_at" label="更新时间" width="160" :formatter="formatDate" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="showParameterEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDeleteParameter(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 参数分页 -->
    <div class="pagination">
      <el-pagination v-model:current-page="parameterCurrentPage" v-model:page-size="parameterPageSize"
        :page-sizes="[10, 20, 50, 100]" :total="environmentStore.parameterPagination.total" :background="true"
        layout="total, sizes, prev, pager, next, jumper" @update:current-page="handleParameterPageChange"
        @update:page-size="handleParameterSizeChange" />
    </div>
  </el-dialog>

  <!-- 参数编辑对话框 -->
  <el-dialog v-model="parameterEditDialog.visible" :title="parameterEditDialog.isEdit ? '编辑参数' : '新增参数'" width="500px">
    <el-form ref="parameterFormRef" :model="parameterEditDialog.form" :rules="parameterRules" label-width="100px">
      <el-form-item label="参数键" prop="param_key">
        <el-input v-model="parameterEditDialog.form.param_key" placeholder="请输入参数键" />
      </el-form-item>
      <el-form-item label="参数值" prop="param_value">
        <el-input v-model="parameterEditDialog.form.param_value" type="textarea" :rows="3" placeholder="请输入参数值" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="parameterEditDialog.form.description" placeholder="请输入参数描述" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="parameterEditDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleParameterSubmit">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useEnvironmentStore } from '@/stores/environmentStore'
import { formatDateTime } from '@/utils/date'

const loading = ref(false)

const environmentStore = useEnvironmentStore()

// 搜索表单
const searchForm = ref({
  name: '',
  base_url: '',
  description: ''
})

const parameterSearchForm = ref({
  param_key: '',
  description: ''
})

// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)
const parameterCurrentPage = ref(1)
const parameterPageSize = ref(10)

// 防抖计时器
let searchTimer = null
let parameterSearchTimer = null


// 环境对话框
const environmentDialog = reactive({
  visible: false,
  isEdit: false,
  form: {
    name: '',
    base_url: '',
    description: ''
  }
})

// 参数对话框
const parameterDialog = reactive({
  visible: false,
  environmentName: ''
})

const parameterEditDialog = reactive({
  visible: false,
  isEdit: false,
  form: {
    param_key: '',
    param_value: '',
    description: ''
  }
})

// 表单引用
const environmentFormRef = ref()
const parameterFormRef = ref()

// 表单验证规则
const environmentRules = {
  name: [{ required: true, message: '请输入环境名称', trigger: 'blur' }],
  base_url: [{ required: true, message: '请输入基础URL', trigger: 'blur' }]
}

const parameterRules = {
  param_key: [{ required: true, message: '请输入参数键', trigger: 'blur' }],
  param_value: [{ required: true, message: '请输入参数值', trigger: 'blur' }]
}

// 统一的数据获取方法
const fetchEnvironments = async () => {
  loading.value = true

  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      search: searchForm.value.name || searchForm.value.base_url || searchForm.value.description 
        ? `${searchForm.value.name} ${searchForm.value.base_url} ${searchForm.value.description}`.trim()
        : ''
    }
    
    await environmentStore.fetchEnvironments(params)
  } catch (error) {
    console.error('Error fetching environments:', error)
    ElMessage.error('获取环境数据失败')
  }
}

const fetchParameters = async () => {
  if (!environmentStore.currentEnvironment) return
  
  try {
    const params = {
      page: parameterCurrentPage.value,
      pageSize: parameterPageSize.value,
      search: parameterSearchForm.value.param_key || parameterSearchForm.value.description
        ? `${parameterSearchForm.value.param_key} ${parameterSearchForm.value.description}`.trim()
        : ''
    }
    
    await environmentStore.fetchEnvironmentParameters(environmentStore.currentEnvironment.id, params)
  } catch (error) {
    console.error('Error fetching parameters:', error)
    ElMessage.error('获取参数数据失败')
  }
}

// 输入搜索处理（防抖）
const handleInputSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    fetchEnvironments()
  }, 500)
}

const handleParameterInputSearch = () => {
  clearTimeout(parameterSearchTimer)
  parameterSearchTimer = setTimeout(() => {
    parameterCurrentPage.value = 1
    fetchParameters()
  }, 500)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    base_url: '',
    description: ''
  }
  currentPage.value = 1
  fetchEnvironments()
}

const resetParameterSearch = () => {
  parameterSearchForm.value = {
    param_key: '',
    description: ''
  }
  parameterCurrentPage.value = 1
  fetchParameters()
}

// 分页处理
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchEnvironments()
}

const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchEnvironments()
}

const handleParameterPageChange = (newPage) => {
  parameterCurrentPage.value = newPage
  fetchParameters()
}

const handleParameterSizeChange = (newSize) => {
  parameterPageSize.value = newSize
  parameterCurrentPage.value = 1
  fetchParameters()
}

// 日期格式化
const formatDate = (row, column, cellValue) => {
  return cellValue ? formatDateTime(cellValue) : '-'
}

// 生命周期
onMounted(() => {
  fetchEnvironments()
})

// 环境管理方法
const showEnvironmentDialog = (environment = null) => {
  environmentDialog.isEdit = !!environment
  environmentDialog.form = environment
    ? { ...environment }
    : { name: '', base_url: '', description: '' }
  environmentDialog.visible = true
}

const handleEnvironmentSubmit = async () => {
  if (!environmentFormRef.value) return

  await environmentFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (environmentDialog.isEdit) {
          await environmentStore.updateEnvironment(environmentDialog.form.id, environmentDialog.form)
          ElMessage.success('环境更新成功')
        } else {
          await environmentStore.createEnvironment(environmentDialog.form)
          ElMessage.success('环境创建成功')
        }
        environmentDialog.visible = false
        fetchEnvironments()
      } catch (error) {
        console.error('环境操作失败:', error)
        ElMessage.error(`操作失败: ${environmentStore.error || error.message || '未知错误'}`)
      }
    }
  })
}

const handleDeleteEnvironment = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个环境吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await environmentStore.deleteEnvironment(id)
    ElMessage.success('删除成功')
    fetchEnvironments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 参数管理方法
const showParameterDialog = async (environment) => {
  try {
    environmentStore.setCurrentEnvironment(environment)
    parameterDialog.environmentName = environment.name
    parameterDialog.visible = true
    
    // 重置参数搜索和分页
    resetParameterSearch()
    await fetchParameters()
  } catch (error) {
    console.error('打开参数对话框失败:', error)
    ElMessage.error('加载参数失败')
  }
}

const showParameterEditDialog = (parameter = null) => {
  // 确保当前环境已设置
  if (!environmentStore.currentEnvironment) {
    ElMessage.error('请先选择环境')
    return
  }
  
  parameterEditDialog.isEdit = !!parameter
  parameterEditDialog.form = parameter
    ? { ...parameter }
    : { param_key: '', param_value: '', description: '' }
  parameterEditDialog.visible = true
}

const handleParameterSubmit = async () => {
  if (!parameterFormRef.value) return

  await parameterFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (parameterEditDialog.isEdit) {
          await environmentStore.updateEnvironmentParameter(
            parameterEditDialog.form.id, 
            parameterEditDialog.form
          )
          ElMessage.success('参数更新成功')
        } else {
          await environmentStore.createEnvironmentParameter(
            environmentStore.currentEnvironment.id,
            parameterEditDialog.form
          )
          ElMessage.success('参数创建成功')
        }
        parameterEditDialog.visible = false
        await fetchParameters()
      } catch (error) {
        console.error('参数操作失败:', error)
        ElMessage.error(`操作失败: ${environmentStore.error || error.message || '未知错误'}`)
      }
    }
  })
}

const handleDeleteParameter = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个参数吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await environmentStore.deleteEnvironmentParameter(id)
    ElMessage.success('删除成功')
    await fetchParameters()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.pagination {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #ebeef5;
}

/* 表单样式优化 */
:deep(.el-form--inline .el-form-item) {
  margin-right: 16px;
  margin-bottom: 0;
}

:deep(.el-form--inline .el-form-item__label) {
  width: auto !important;
}

:deep(.el-table .el-link) {
  font-weight: 500;
}

:deep(.el-table .el-button) {
  margin: 2px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-bar {
    width: 100%;
  }
  
  .action-bar {
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .header-bar {
    margin: 0 10px 10px 10px;
    padding: 12px;
  }
  
  :deep(.el-form--inline .el-form-item) {
    margin-right: 0;
    margin-bottom: 10px;
    width: 100%;
  }
  
  :deep(.el-form--inline .el-form-item__content) {
    width: 100%;
  }
  
  :deep(.el-input) {
    width: 100%;
  }
  
  .card-header {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .card-header .el-button {
    align-self: flex-end;
  }
}

/* 对话框样式优化 */
:deep(.el-dialog__body) {
  padding: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-textarea .el-textarea__inner) {
  resize: vertical;
  min-height: 80px;
}
</style>