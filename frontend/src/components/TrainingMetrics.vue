<template>
  <div class="training-metrics">
    <div class="metrics-grid">
      <div class="metric-chart">
        <h3>准确率趋势</h3>
        <canvas ref="accuracyChart"></canvas>
      </div>
      <div class="metric-chart">
        <h3>损失趋势</h3>
        <canvas ref="lossChart"></canvas>
      </div>
      <div class="metric-chart">
        <h3>学习率变化</h3>
        <canvas ref="lrChart"></canvas>
      </div>
      <div class="metric-chart">
        <h3>批次大小分布</h3>
        <canvas ref="batchChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'TrainingMetrics',
  props: {
    metrics: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const accuracyChart = ref(null)
    const lossChart = ref(null)
    const lrChart = ref(null)
    const batchChart = ref(null)
    let charts = {}

    const createCharts = () => {
      // 准备数据
      const labels = props.metrics.map(m => `Epoch ${m.epoch} Batch ${m.batch}`)
      
      // 准确率图表
      if (charts.accuracy) charts.accuracy.destroy()
      const accuracyCtx = accuracyChart.value.getContext('2d')
      charts.accuracy = new Chart(accuracyCtx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '准确率 (%)',
            data: props.metrics.map(m => m.accuracy),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      })

      // 损失图表
      if (charts.loss) charts.loss.destroy()
      const lossCtx = lossChart.value.getContext('2d')
      charts.loss = new Chart(lossCtx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '损失',
            data: props.metrics.map(m => m.loss),
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1
          }]
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

      // 学习率图表
      if (charts.lr) charts.lr.destroy()
      const lrCtx = lrChart.value.getContext('2d')
      charts.lr = new Chart(lrCtx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '学习率',
            data: props.metrics.map(m => m.learning_rate),
            borderColor: 'rgb(153, 102, 255)',
            tension: 0.1
          }]
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

      // 批次大小分布图表
      if (charts.batch) charts.batch.destroy()
      const batchCtx = batchChart.value.getContext('2d')
      const batchSizes = props.metrics.map(m => m.batch_size)
      const batchCounts = {}
      batchSizes.forEach(size => {
        batchCounts[size] = (batchCounts[size] || 0) + 1
      })
      
      charts.batch = new Chart(batchCtx, {
        type: 'bar',
        data: {
          labels: Object.keys(batchCounts),
          datasets: [{
            label: '批次数量',
            data: Object.values(batchCounts),
            backgroundColor: 'rgba(54, 162, 235, 0.5)'
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    }

    watch(() => props.metrics, () => {
      createCharts()
    })

    onMounted(() => {
      createCharts()
    })

    return {
      accuracyChart,
      lossChart,
      lrChart,
      batchChart
    }
  }
}
</script>

<style scoped>
.training-metrics {
  margin-top: 20px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.metric-chart {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-chart h3 {
  margin-bottom: 10px;
  color: #333;
}

canvas {
  width: 100% !important;
  height: 300px !important;
}
</style> 