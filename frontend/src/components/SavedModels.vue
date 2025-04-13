<template>
  <div class="saved-models">
    <h2>已保存的模型</h2>
    <div v-if="models.length > 0" class="models-list">
      <div v-for="model in models" :key="model.filename" class="model-item">
        <div class="model-info">
          <p class="timestamp">保存时间：{{ formatTimestamp(model.timestamp) }}</p>
          <p>训练轮数：{{ model.epoch }}</p>
          <p>准确率：{{ model.accuracy.toFixed(2) }}%</p>
        </div>
        <div class="model-actions">
          <button @click="downloadModel(model)">下载</button>
          <button @click="loadModel(model)">加载</button>
        </div>
      </div>
    </div>
    <div v-else class="no-models">
      <p>暂无保存的模型</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'SavedModels',
  props: {
    modelId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const models = ref([])

    const fetchModels = async () => {
      try {
        const response = await axios.get(`/api/models/saved/${props.modelId}`)
        models.value = response.data
      } catch (error) {
        console.error('Error fetching saved models:', error)
      }
    }

    const formatTimestamp = (timestamp) => {
      const year = timestamp.substring(0, 4)
      const month = timestamp.substring(4, 6)
      const day = timestamp.substring(6, 8)
      const hour = timestamp.substring(9, 11)
      const minute = timestamp.substring(11, 13)
      return `${year}-${month}-${day} ${hour}:${minute}`
    }

    const downloadModel = async (model) => {
      try {
        const response = await axios.get(model.path, {
          responseType: 'blob'
        })
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', model.filename)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        console.error('Error downloading model:', error)
        alert('下载模型失败：' + error.message)
      }
    }

    const loadModel = async (model) => {
      try {
        await axios.post(`/api/models/${props.modelId}/load`, {
          path: model.path
        })
        alert('模型加载成功！')
      } catch (error) {
        console.error('Error loading model:', error)
        alert('加载模型失败：' + error.message)
      }
    }

    onMounted(fetchModels)

    return {
      models,
      formatTimestamp,
      downloadModel,
      loadModel
    }
  }
}
</script>

<style scoped>
.saved-models {
  margin-top: 30px;
}

.models-list {
  display: grid;
  gap: 15px;
}

.model-item {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-info {
  flex: 1;
}

.timestamp {
  font-weight: bold;
  margin-bottom: 5px;
}

.model-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:first-child {
  background-color: #4CAF50;
  color: white;
}

button:last-child {
  background-color: #2196F3;
  color: white;
}

button:hover {
  opacity: 0.9;
}

.no-models {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style> 