<template>
  <div class="training-config">
    <h2>训练配置</h2>
    <form @submit.prevent="startTraining">
      <div class="form-group">
        <label for="dataset">数据集</label>
        <select id="dataset" v-model="config.dataset" required>
          <option value="mnist">MNIST</option>
          <option value="cifar10">CIFAR-10</option>
          <option value="fashion_mnist">Fashion MNIST</option>
        </select>
      </div>

      <div class="form-group">
        <label for="batchSize">批次大小</label>
        <input 
          type="number" 
          id="batchSize" 
          v-model.number="config.batch_size" 
          min="1" 
          required
        >
      </div>

      <div class="form-group">
        <label for="epochs">训练轮数</label>
        <input 
          type="number" 
          id="epochs" 
          v-model.number="config.epochs" 
          min="1" 
          required
        >
      </div>

      <div class="form-group">
        <label for="learningRate">学习率</label>
        <input 
          type="number" 
          id="learningRate" 
          v-model.number="config.learning_rate" 
          min="0.0001" 
          step="0.0001" 
          required
        >
      </div>

      <button type="submit" :disabled="isTraining">开始训练</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'TrainingConfigForm',
  props: {
    modelId: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const config = ref({
      model_id: props.modelId,
      dataset: 'mnist',
      batch_size: 32,
      epochs: 10,
      learning_rate: 0.001
    })
    const isTraining = ref(false)

    const startTraining = async () => {
      try {
        isTraining.value = true
        await axios.post('/api/train', config.value)
        emit('training-started', config.value.epochs)
      } catch (error) {
        console.error('Error starting training:', error)
        alert('启动训练失败：' + error.message)
      } finally {
        isTraining.value = false
      }
    }

    return {
      config,
      isTraining,
      startTraining
    }
  }
}
</script>

<style scoped>
.training-config {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin: 20px 0;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}
</style> 