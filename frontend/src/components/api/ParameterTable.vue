<template>
  <el-table :data="parameters" size="small" class="parameter-table" empty-text="无参数">
    <el-table-column prop="name" label="参数名" min-width="150">
      <template #default="{ row }">
        <span class="param-name">{{ row.name }}</span>
        <el-tag v-if="row.required" size="small" type="danger" class="required-tag">必填</el-tag>
      </template>
    </el-table-column>
    
    <el-table-column label="参数值" width="180">
      <template #default="{ row }">
        <el-input
          :value="getExample(row)"
          @input="updateExample(row, $event)"
          size="small"
          placeholder="请输入值"
        />
      </template>
    </el-table-column>

    <el-table-column prop="type" label="类型" width="80">
      <template #default="{ row }">
        <el-tag size="small" effect="plain">{{ row.type || getTypeFromSchema(row.schema) }}</el-tag>
      </template>
    </el-table-column>

    <el-table-column prop="description" label="说明" min-width="200">
      <template #default="{ row }">
        <div class="param-description">
          {{ row.description || '无说明' }}
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  parameters: {
    type: Array,
    default: () => []
  }
})

const getTypeFromSchema = (schema) => {
  if (!schema) return 'string'
  if (schema.type) return schema.type
  if (schema.$ref) return schema.$ref.split('/').pop()
  return 'object'
}

const getExample = (row) => {
  if (row.example) return row.example
  if (row.schema && row.schema.example) return row.schema.example
  if (row.schema && row.schema.type === 'integer') return '123'
  if (row.schema && row.schema.type === 'boolean') return 'true'
  return null
}

const updateExample = (row, value) => {
  row.example = value;
}
</script>

<style scoped>
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
}

.param-example {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 12px;
  color: #e74c3c;
}

:deep(.el-table__header) {
  background: #f8f9fa;
}

:deep(.el-table th) {
  background: #f8f9fa;
  font-weight: 600;
}
</style>