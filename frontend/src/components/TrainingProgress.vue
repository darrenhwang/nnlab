<template>
  <div class="training-progress">
    <h2>训练进度</h2>
    <div v-if="progress" class="progress-container">
      <div class="progress-info">
        <p>Epoch: {{ progress.epoch }}/{{ totalEpochs }}</p>
        <p>Batch: {{ progress.batch }}</p>
        <p>Loss: {{ progress.loss.toFixed(4) }}</p>
        <p>Accuracy: {{ progress.accuracy.toFixed(2) }}%</p>
      </div>
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: `${(progress.epoch / totalEpochs) * 100}%` }"
        ></div>
      </div>
    </div>
    <div v-else class="no-progress">
      <p>等待训练开始...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

export default {
  name: 'TrainingProgress',
  props: {
    modelId: {
      type: String,
      required: true
    },
    totalEpochs: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const progress = ref(null)
    let intervalId = null

    const fetchProgress = async () => {
      try {
        const response = await axios.get(`/api/training/progress/${props.modelId}`)
        progress.value = response.data
      } catch (error) {
        console.error('Error fetching training progress:', error)
      }
    }

    onMounted(() => {
      fetchProgress()
      intervalId = setInterval(fetchProgress, 1000)
    })

    onUnmounted(() => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    })

    return {
      progress
    }
  }
}
</script>

<style scoped>
.training-progress {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin: 20px 0;
}

.progress-container {
  margin-top: 20px;
}

.progress-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.3s ease;
}

.no-progress {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style> 