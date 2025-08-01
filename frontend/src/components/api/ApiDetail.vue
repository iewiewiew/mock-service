<template>
  <div class="api-detail">
    <div v-if="!endpoint" class="empty-detail">
      <el-empty description="请选择左侧接口查看详情" :image-size="120" />
    </div>

    <div v-else class="detail-content" v-loading="loading">

      <!-- 接口基本信息 -->
      <div class="api-basic-info">
        <h1 class="api-title">{{ getApiTitle() }}</h1>

        <div class="method-path">
          <el-tag :type="getMethodType(endpoint.method)" effect="dark" class="method-tag">
            {{ endpoint.method }}
          </el-tag>
          <span class="api-path">{{ domain + endpoint.path }}</span>
        </div>
      </div>

      <!-- 请求参数 -->
      <div class="parameters-section">
        <h2 class="section-title">
          <el-icon><Document /></el-icon>
          请求参数
        </h2>

        <!-- 路径参数 -->
        <div v-if="hasPathParameters" class="parameter-group">
          <h3 class="parameter-group-title">
            <el-tag size="small" type="danger">路径参数</el-tag>
            <span class="param-desc">包含在URL路径中的参数</span>
          </h3>
          <ParameterTable :parameters="pathParameters" />
        </div>

        <!-- Query参数 -->
        <div v-if="hasQueryParameters" class="parameter-group">
          <h3 class="parameter-group-title">
            <el-tag size="small" type="primary">Query参数</el-tag>
            <span class="param-desc">URL问号后的参数</span>
          </h3>
          <ParameterTable :parameters="queryParameters" />
        </div>

        <!-- Body参数 -->
        <div v-if="hasBodyParameters" class="parameter-group">
          <h3 class="parameter-group-title">
            <el-tag size="small" type="warning">Body参数</el-tag>
            <span class="param-desc">请求体中的表单参数</span>
          </h3>
          <div class="body-parameters-table">
            <el-table :data="bodyParameters" size="small" class="parameter-table" empty-text="无参数">
              <el-table-column prop="name" label="参数名" min-width="200">
                <template #default="{ row }">
                  <span class="param-name">{{ row.name }}</span>
                  <el-tag v-if="row.required" size="small" type="danger" class="required-tag">必填</el-tag>
                </template>
              </el-table-column>
              
              <el-table-column label="参数值" min-width="200">
                <template #default="{ row }">
                  <!-- 文本输入框 -->
                  <el-input
                    v-if="row.type === 'string' && !row.enum"
                    v-model="bodyFormData[row.name]"
                    :placeholder="getPlaceholder(row)"
                    size="small"
                    clearable
                  />

                  <!-- 数字输入框 -->
                  <el-input-number
                    v-else-if="row.type === 'integer' || row.type === 'number'"
                    v-model="bodyFormData[row.name]"
                    :placeholder="getPlaceholder(row)"
                    :min="row.minimum"
                    :max="row.maximum"
                    size="small"
                    controls-position="right"
                    style="width: 100%"
                  />

                  <!-- 下拉选择框 -->
                  <el-select
                    v-else-if="row.enum && row.enum.length > 0"
                    v-model="bodyFormData[row.name]"
                    :placeholder="getPlaceholder(row)"
                    size="small"
                    style="width: 100%"
                    clearable
                  >
                    <el-option
                      v-for="option in row.enum"
                      :key="option"
                      :label="option"
                      :value="option"
                    />
                  </el-select>

                  <!-- 布尔值选择 -->
                  <el-radio-group
                    v-else-if="row.type === 'boolean'"
                    v-model="bodyFormData[row.name]"
                    size="small"
                  >
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                  </el-radio-group>

                  <!-- 默认文本输入框 -->
                  <el-input
                    v-else
                    v-model="bodyFormData[row.name]"
                    :placeholder="getPlaceholder(row)"
                    size="small"
                    clearable
                  />
                </template>
              </el-table-column>

              <el-table-column prop="type" label="类型" width="70">
                <template #default="{ row }">
                  <el-tag size="small" effect="plain">{{ row.type || 'string' }}</el-tag>
                </template>
              </el-table-column>

              <el-table-column prop="description" label="说明" min-width="100">
                <template #default="{ row }">
                  <div class="param-description">
                    {{ row.description || '无说明' }}
                    <div v-if="row.format" class="format-hint">格式: {{ row.format }}</div>
                    <div v-if="row.minimum !== undefined || row.maximum !== undefined" class="range-hint">
                      <span v-if="row.minimum !== undefined">最小值: {{ row.minimum }}</span>
                      <span v-if="row.maximum !== undefined">最大值: {{ row.maximum }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>

            <!-- JSON预览 -->
            <div v-if="showJsonPreview" class="json-preview">
              <h4>JSON预览</h4>
              <pre class="json-code">{{ JSON.stringify(bodyFormData, null, 2) }}</pre>
            </div>
          </div>
        </div>

        <!-- Header参数 -->
        <div v-if="hasHeaderParameters" class="parameter-group">
          <h3 class="parameter-group-title">
            <el-tag size="small" type="success">Header参数</el-tag>
            <span class="param-desc">HTTP头部参数</span>
          </h3>
          <ParameterTable :parameters="headerParameters" />
        </div>

        <div v-if="!hasParameters" class="no-parameters">
          <el-empty description="此接口无需参数" :image-size="80" />
        </div>
      </div>

      <!-- 响应示例 -->
      <div v-if="hasResponses" class="response-section">
        <h2 class="section-title">
          <el-icon><CircleCheck /></el-icon>
          响应示例
        </h2>
        <div class="response-content">
          <div v-for="(response, code) in getResponses()" :key="code" class="response-item">
            <div class="response-code">
              <el-tag :type="getResponseType(code)" size="small">{{ code }}</el-tag>
              <span class="response-desc">{{ response.description }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'
import { Document, CircleCheck } from '@element-plus/icons-vue'
import ParameterTable from './ParameterTable.vue'
import { useEndpointStore } from '@/stores/endpointStore'

const props = defineProps({
  endpoint: Object,
  loading: Boolean
})

const apiStore = useEndpointStore()
const showDebug = ref(false)
const localLoading = ref(false)
const showJsonPreview = ref(true)
const bodyFormData = ref({})

const domain = 'https://gitee.com';

// 参数计算属性 - 移到前面定义
const pathParameters = computed(() => {
  const params = currentParameters.value.filter(p => p.param_type === 'path')
  console.log('📍 路径参数数量:', params.length)
  return params
})

const queryParameters = computed(() => {
  const params = currentParameters.value.filter(p => p.param_type === 'query')
  console.log('📍 查询参数数量:', params.length)
  return params
})

const bodyParameters = computed(() => {
  // 过滤出 body 参数并转换为表单可用的格式
  const bodyParams = currentParameters.value.filter(p => 
    p.param_type === 'formData' || p.param_type === 'body'
  )
  
  // 转换参数格式
  const formattedParams = bodyParams.map(param => {
    // 如果参数有 schema，提取 schema 中的信息
    if (param.schema && typeof param.schema === 'object') {
      return {
        name: param.name,
        type: param.schema.type || 'string',
        required: param.required || false,
        description: param.description || param.schema.description,
        default: param.default || param.schema.default,
        enum: param.enum || param.schema.enum,
        format: param.format || param.schema.format,
        minimum: param.minimum || param.schema.minimum,
        maximum: param.maximum || param.schema.maximum,
        minLength: param.minLength || param.schema.minLength,
        maxLength: param.maxLength || param.schema.maxLength
      }
    }
    
    return {
      name: param.name,
      type: param.type || 'string',
      required: param.required || false,
      description: param.description,
      default: param.default,
      enum: param.enum,
      format: param.format,
      minimum: param.minimum,
      maximum: param.maximum,
      minLength: param.minLength,
      maxLength: param.maxLength
    }
  })
  
  console.log('📍 Body参数:', formattedParams)
  return formattedParams
})

const headerParameters = computed(() => {
  const params = currentParameters.value.filter(p => p.param_type === 'header')
  console.log('📍 头部参数数量:', params.length)
  return params
})

// 是否有参数的计算属性
const hasPathParameters = computed(() => pathParameters.value.length > 0)
const hasQueryParameters = computed(() => queryParameters.value.length > 0)
const hasBodyParameters = computed(() => bodyParameters.value.length > 0)
const hasHeaderParameters = computed(() => headerParameters.value.length > 0)
const hasParameters = computed(() =>
  hasPathParameters.value ||
  hasQueryParameters.value ||
  hasBodyParameters.value ||
  hasHeaderParameters.value
)

// 直接从 endpoint.id 获取当前接口ID
const currentEndpointId = computed(() => {
  return props.endpoint?.id || null
})

// 修复：简化参数逻辑，直接使用 store 中的参数
const currentParameters = computed(() => {
  console.log('🔍 currentParameters 计算:')
  console.log('  - 当前接口ID:', currentEndpointId.value)
  console.log('  - store 参数数量:', apiStore.endpointParameters.length)
  
  // 如果没有当前接口ID，返回空数组
  if (!currentEndpointId.value) {
    console.log('❌ 没有当前接口ID，返回空数组')
    return []
  }
  
  // 检查 store 中的参数是否属于当前接口
  if (apiStore.endpointParameters.length > 0) {
    const firstParam = apiStore.endpointParameters[0]
    console.log('  - 第一个参数的endpoint_id:', firstParam?.endpoint_id)
    
    if (firstParam && firstParam.endpoint_id === currentEndpointId.value) {
      console.log('✅ 参数匹配，返回参数数量:', apiStore.endpointParameters.length)
      return apiStore.endpointParameters
    } else {
      console.log('❌ 参数不匹配，返回空数组')
      return []
    }
  }
  
  console.log('❌ store中没有参数，返回空数组')
  return []
})

// 监听 endpoint 变化，获取参数
watch(() => props.endpoint, async (newEndpoint, oldEndpoint) => {
  console.log('🔄 endpoint 变化监听:', { 
    oldEndpointId: oldEndpoint?.id, 
    newEndpointId: newEndpoint?.id 
  })
  
  if (newEndpoint && newEndpoint.id) {
    await fetchParameters(newEndpoint.id)
    // 重置表单数据
    resetBodyFormData()
  }
}, { immediate: true })

// 监听 bodyParameters 变化，初始化表单数据
watch(bodyParameters, (newParams) => {
  if (newParams && newParams.length > 0) {
    resetBodyFormData()
  }
}, { deep: true })

// 重置Body表单数据
const resetBodyFormData = () => {
  bodyFormData.value = {}
  if (bodyParameters.value && bodyParameters.value.length > 0) {
    bodyParameters.value.forEach(param => {
      // 设置默认值
      if (param.default !== undefined) {
        bodyFormData.value[param.name] = param.default
      } else if (param.type === 'boolean') {
        bodyFormData.value[param.name] = false
      } else if (param.type === 'integer' || param.type === 'number') {
        bodyFormData.value[param.name] = null
      } else {
        bodyFormData.value[param.name] = ''
      }
    })
  }
}

// 获取参数的方法
const fetchParameters = async (endpointId) => {
  try {
    localLoading.value = true
    console.log('🟡 开始获取参数，接口ID:', endpointId)
    
    // 清空之前的参数
    if (apiStore.endpointParameters.length > 0) {
      apiStore.endpointParameters = []
      await nextTick()
    }
    
    // 调用 store 方法获取参数
    await apiStore.fetchEndpointParameters(endpointId)
    
    console.log('🟢 参数获取完成:')
    console.log('  - 参数数量:', apiStore.endpointParameters.length)
    console.log('  - 参数详情:', apiStore.endpointParameters)
    
  } catch (error) {
    console.error('❌ 获取参数失败:', error)
    apiStore.endpointParameters = []
  } finally {
    localLoading.value = false
  }
}

// 组合 loading 状态
const loading = computed(() => props.loading || localLoading.value)

// 获取占位符文本
const getPlaceholder = (param) => {
  let placeholder = `请输入${param.name}`
  
  if (param.type === 'integer' || param.type === 'number') {
    placeholder = `请输入数字`
    if (param.minimum !== undefined && param.maximum !== undefined) {
      placeholder += ` (${param.minimum}-${param.maximum})`
    } else if (param.minimum !== undefined) {
      placeholder += ` (最小${param.minimum})`
    } else if (param.maximum !== undefined) {
      placeholder += ` (最大${param.maximum})`
    }
  } else if (param.format) {
    placeholder += ` (${param.format})`
  }
  
  return placeholder
}

const getMethodType = (method) => {
  const types = {
    'GET': 'success',
    'POST': 'warning',
    'PUT': 'primary',
    'DELETE': 'danger',
    'PATCH': 'info'
  }
  return types[method?.toUpperCase()] || 'info'
}

const getResponseType = (code) => {
  if (code.startsWith('2')) return 'success'
  if (code.startsWith('4')) return 'warning'
  if (code.startsWith('5')) return 'danger'
  return 'info'
}

const getApiTitle = () => {
  if (!props.endpoint) return '未知接口'
  
  const data = props.endpoint
  
  if (data.operation) {
    if (data.operation.summary) return data.operation.summary
    if (data.operation.operationId) return data.operation.operationId
    if (data.operation.description) return data.operation.description
  }
  
  if (data.summary) return data.summary
  if (data.name) return data.name
  if (data.label) return data.label
  if (data.operationId) return data.operationId
  if (data.description) return data.description
  if (data.title) return data.title
  
  if (data.path) {
    const pathParts = data.path.split('/').filter(part => part && !part.includes('{'))
    return pathParts[pathParts.length - 1] || data.path
  }
  
  return '未命名接口'
}

const getApiDescription = () => {
  if (!props.endpoint) return ''
  
  const data = props.endpoint
  
  if (data.operation?.description) return data.operation.description
  if (data.description) return data.description
  if (data.operation?.summary) return data.operation.summary
  if (data.summary) return data.summary
  
  return ''
}

const getResponses = () => {
  if (!props.endpoint) return {}
  
  const data = props.endpoint
  
  if (data.operation?.responses) return data.operation.responses
  if (data.responses) return data.responses
  
  return {}
}

const hasResponses = computed(() => {
  const responses = getResponses()
  return Object.keys(responses).length > 0
})
</script>

<style scoped>
.api-detail {
  height: 100%;
  overflow: auto;
  padding: 0;
}

.empty-detail {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: #fafafa;
}

.detail-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.api-basic-info {
  border-bottom: 1px solid #e4e7ed;
  padding-bottom: 20px;
  margin-bottom: 24px;
}

.method-path {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.method-tag {
  min-width: 60px;
  text-align: center;
  font-weight: bold;
  font-size: 12px;
}

.api-path {
  font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.api-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 32px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
}

.parameter-group {
  margin-bottom: 24px;
}

.parameter-group-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.param-desc {
  font-size: 12px;
  color: #909399;
  font-weight: normal;
}

/* Body参数表格样式 */
.body-parameters-table {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  height: 500px;
}

.parameter-table {
  width: 100%;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
}

.param-name {
  font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
  font-weight: 500;
}

.required-tag {
  margin-left: 6px;
}

.param-description {
  line-height: 1.4;
  font-size: 12px;
}

.format-hint {
  color: #909399;
  font-size: 11px;
  margin-top: 2px;
}

.range-hint {
  color: #e6a23c;
  font-size: 11px;
  margin-top: 2px;
}

.range-hint span {
  margin-right: 8px;
}

:deep(.parameter-table .el-table__header) {
  background: #f8f9fa;
}

:deep(.parameter-table th) {
  background: #f8f9fa;
  font-weight: 600;
}

:deep(.parameter-table .el-table__row) {
  background: white;
}

/* JSON预览样式 */
.json-preview {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px dashed #dcdfe6;
}

.json-preview h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.json-code {
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.4;
  overflow-x: auto;
  margin: 0;
}

.no-parameters {
  text-align: center;
  padding: 40px 0;
  color: #909399;
}

.response-section {
  margin-top: 32px;
}

.response-item {
  margin-bottom: 20px;
}

.response-code {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.response-desc {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .detail-content {
    padding: 16px;
  }

  .api-title {
    font-size: 20px;
  }

  .api-path {
    font-size: 14px;
  }

  .section-title {
    font-size: 18px;
  }

  .parameter-group-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .method-path {
    flex-wrap: wrap;
  }
  
  .body-parameters-table {
    padding: 12px;
  }
}
</style>