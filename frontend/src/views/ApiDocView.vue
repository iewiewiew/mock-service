<template>
  <div class="common-list-container">
    <div class="layout-container">
      <!-- 左侧目录树 -->
      <div class="tree-panel">
        <ApiTree @endpoint-selected="handleEndpointSelected" />
      </div>

      <!-- 右侧接口详情 -->
      <div class="detail-panel">
        <ApiDetail :endpoint="selectedEndpoint" :loading="detailLoading" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEndpointStore } from '@/stores/endpointStore'
import ApiTree from '@/components/api/ApiTree.vue'
import ApiDetail from '@/components/api/ApiDetail.vue'

const endpointStore = useEndpointStore()
const selectedEndpoint = ref(null)
const detailLoading = ref(false)

const handleEndpointSelected = async (endpointData) => {
  detailLoading.value = true
  try {
    // 直接从点击的数据中获取接口信息，不需要额外请求
    selectedEndpoint.value = endpointData
  } catch (error) {
    console.error('加载接口详情失败:', error)
  } finally {
    detailLoading.value = false
  }
}

// 初始化加载分类数据
onMounted(() => {
  endpointStore.fetchEndpointsByCategories()
})

</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tree-panel {
  width: 350px;
  min-width: 300px;
  border-right: 1px solid #e4e7ed;
  background: #fff;
}

.detail-panel {
  flex: 1;
  min-width: 0;
  background: #fff;
  overflow: auto;
}

@media (max-width: 768px) {
  .common-list-container {
    padding: 8px;
  }

  .layout-container {
    flex-direction: column;
  }

  .tree-panel {
    width: 100%;
    height: 40%;
    border-right: none;
    border-bottom: 1px solid #e4e7ed;
  }

  .detail-panel {
    height: 60%;
  }
}
</style>