<template>
  <div class="model-detail">
    <h1>模型详情</h1>
    
    <div v-if="model" class="model-info">
      <h2>{{ model.name }}</h2>
      <p>创建时间：{{ new Date(model.created_at).toLocaleString() }}</p>
      
      <div class="model-layers">
        <h3>模型结构</h3>
        <div v-for="(layer, index) in model.layers" :key="index" class="layer">
          <p>层 {{ index + 1 }}: {{ layer.type }}</p>
          <p>单元数：{{ layer.units }}</p>
          <p v-if="layer.activation">激活函数：{{ layer.activation }}</p>
        </div>
      </div>

      <div class="training-section">
        <TrainingConfigForm 
          :model-id="model.id" 
          @training-started="handleTrainingStarted"
        />
        
        <TrainingProgress 
          v-if="isTraining" 
          :model-id="model.id" 
          :total-epochs="totalEpochs"
        />

        <SavedModels :model-id="model.id" />
        <TrainingHistory :model-id="model.id" />
      </div>
    </div>
    
    <div v-else class="loading">
      <p>加载中...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import TrainingConfigForm from '@/components/TrainingConfigForm.vue'
import TrainingProgress from '@/components/TrainingProgress.vue'
import SavedModels from '@/components/SavedModels.vue'
import TrainingHistory from '@/components/TrainingHistory.vue'

export default {
  name: 'ModelDetail',
  components: {
    TrainingConfigForm,
    TrainingProgress,
    SavedModels,
    TrainingHistory
  },
  setup() {
    const route = useRoute()
    const model = ref(null)
    const isTraining = ref(false)
    const totalEpochs = ref(0)

    const fetchModel = async () => {
      try {
        const response = await axios.get(`/api/models/${route.params.id}`)
        model.value = response.data
      } catch (error) {
        console.error('Error fetching model:', error)
      }
    }

    const handleTrainingStarted = (epochs) => {
      isTraining.value = true
      totalEpochs.value = epochs
    }

    onMounted(fetchModel)

    return {
      model,
      isTraining,
      totalEpochs,
      handleTrainingStarted
    }
  }
}
</script>

<style scoped>
.model-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.model-info {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.model-layers {
  margin: 20px 0;
}

.layer {
  background-color: #f5f5f5;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
}

.training-section {
  margin-top: 30px;
}

.loading {
  text-align: center;
  padding: 20px;
}
</style> 