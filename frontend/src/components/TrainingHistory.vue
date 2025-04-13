<template>
  <div class="training-history">
    <h2>训练历史</h2>
    <div v-if="histories.length > 0" class="history-list">
      <div v-for="history in histories" :key="history.id" class="history-item">
        <div class="history-info">
          <p class="time">
            开始时间：{{ formatDateTime(history.start_time) }}
            <br>
            结束时间：{{ formatDateTime(history.end_time) }}
          </p>
          <p>数据集：{{ history.dataset }}</p>
          <p>批次大小：{{ history.batch_size }}</p>
          <p>训练轮数：{{ history.epochs }}</p>
          <p>学习率：{{ history.learning_rate }}</p>
          <p>最终准确率：{{ history.final_accuracy.toFixed(2) }}%</p>
          <p>最终损失：{{ history.final_loss.toFixed(4) }}</p>
        </div>
        <div class="history-actions">
          <button @click="showMetrics(history)">查看指标</button>
          <button @click="deleteHistory(history)">删除</button>
        </div>
      </div>
    </div>
    <div v-else class="no-history">
      <p>暂无训练历史</p>
    </div>

    <!-- 指标图表对话框 -->
    <div v-if="selectedHistory" class="metrics-dialog">
      <h3>训练指标</h3>
      <div class="metrics-chart">
        <canvas ref="metricsChart"></canvas>
      </div>
      <button @click="closeMetrics">关闭</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'TrainingHistory',
  props: {
    modelId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const histories = ref([])
    const selectedHistory = ref(null)
    const metricsChart = ref(null)
    let chart = null

    const fetchHistories = async () => {
      try {
        const response = await axios.get(`/api/training/history/${props.modelId}`)
        histories.value = response.data
      } catch (error) {
        console.error('Error fetching training history:', error)
      }
    }

    const formatDateTime = (datetimeStr) => {
      return new Date(datetimeStr).toLocaleString()
    }

    const showMetrics = (history) => {
      selectedHistory.value = history
      nextTick(() => {
        createMetricsChart(history.metrics)
      })
    }

    const createMetricsChart = (metrics) => {
      if (chart) {
        chart.destroy()
      }

      const ctx = metricsChart.value.getContext('2d')
      const labels = metrics.map(m => `Epoch ${m.epoch} Batch ${m.batch}`)
      const accuracyData = metrics.map(m => m.accuracy)
      const lossData = metrics.map(m => m.loss)

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: '准确率 (%)',
              data: accuracyData,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            },
            {
              label: '损失',
              data: lossData,
              borderColor: 'rgb(255, 99, 132)',
              tension: 0.1
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    const closeMetrics = () => {
      selectedHistory.value = null
      if (chart) {
        chart.destroy()
        chart = null
      }
    }

    const deleteHistory = async (history) => {
      try {
        await axios.delete(`/api/training/history/${props.modelId}/${history.id}`)
        await fetchHistories()
      } catch (error) {
        console.error('Error deleting training history:', error)
        alert('删除训练历史失败：' + error.message)
      }
    }

    onMounted(fetchHistories)

    return {
      histories,
      selectedHistory,
      metricsChart,
      formatDateTime,
      showMetrics,
      closeMetrics,
      deleteHistory
    }
  }
}
</script>

<style scoped>
.training-history {
  margin-top: 30px;
}

.history-list {
  display: grid;
  gap: 15px;
}

.history-item {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.history-info {
  flex: 1;
}

.time {
  font-weight: bold;
  margin-bottom: 10px;
}

.history-actions {
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
  background-color: #2196F3;
  color: white;
}

button:last-child {
  background-color: #f44336;
  color: white;
}

button:hover {
  opacity: 0.9;
}

.no-history {
  text-align: center;
  padding: 20px;
  color: #666;
}

.metrics-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.metrics-chart {
  width: 600px;
  height: 400px;
  margin: 20px 0;
}
</style> 