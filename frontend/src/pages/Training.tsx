import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Line } from 'react-chartjs-2';

export default function Training() {
  const currentModel = useSelector((state: RootState) => state.model.currentModel);
  const [dataset, setDataset] = useState('mnist');
  const [batchSize, setBatchSize] = useState(32);
  const [epochs, setEpochs] = useState(10);
  const [learningRate, setLearningRate] = useState(0.001);
  const [isTraining, setIsTraining] = useState(false);
  const [progress, setProgress] = useState({
    currentEpoch: 0,
    loss: 0,
    accuracy: 0,
  });

  const datasets = ['mnist', 'cifar10', 'fashion_mnist'];

  const handleStartTraining = async () => {
    if (!currentModel) return;

    setIsTraining(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/training/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model_id: currentModel.id,
          dataset,
          batch_size: batchSize,
          epochs,
          learning_rate: learningRate,
        }),
      });

      if (!response.ok) {
        throw new Error('训练启动失败');
      }

      // 建立WebSocket连接以接收实时训练数据
      const ws = new WebSocket(`ws://localhost:8000/ws/training/${currentModel.id}`);
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setProgress(data);
      };

      ws.onclose = () => {
        setIsTraining(false);
      };
    } catch (error) {
      console.error('训练错误:', error);
      setIsTraining(false);
    }
  };

  const chartData = {
    labels: Array.from({ length: epochs }, (_, i) => i + 1),
    datasets: [
      {
        label: '损失',
        data: [progress.loss],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: '准确率',
        data: [progress.accuracy],
        borderColor: 'rgb(153, 102, 255)',
        tension: 0.1,
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        模型训练
      </Typography>

      <Paper sx={{ p: 2, mb: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              当前模型: {currentModel?.name || '未选择模型'}
            </Typography>
          </Grid>

          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel>数据集</InputLabel>
              <Select
                value={dataset}
                label="数据集"
                onChange={(e) => setDataset(e.target.value)}
              >
                {datasets.map((ds) => (
                  <MenuItem key={ds} value={ds}>
                    {ds}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={6}>
            <TextField
              fullWidth
              label="批次大小"
              type="number"
              value={batchSize}
              onChange={(e) => setBatchSize(parseInt(e.target.value))}
            />
          </Grid>

          <Grid item xs={6}>
            <TextField
              fullWidth
              label="训练轮数"
              type="number"
              value={epochs}
              onChange={(e) => setEpochs(parseInt(e.target.value))}
            />
          </Grid>

          <Grid item xs={6}>
            <TextField
              fullWidth
              label="学习率"
              type="number"
              value={learningRate}
              onChange={(e) => setLearningRate(parseFloat(e.target.value))}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleStartTraining}
              disabled={!currentModel || isTraining}
              fullWidth
            >
              {isTraining ? '训练中...' : '开始训练'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {isTraining && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            训练进度
          </Typography>
          <Typography>
            当前轮数: {progress.currentEpoch} / {epochs}
          </Typography>
          <Typography>
            损失: {progress.loss.toFixed(4)}
          </Typography>
          <Typography>
            准确率: {(progress.accuracy * 100).toFixed(2)}%
          </Typography>
          <Box sx={{ mt: 2, height: 300 }}>
            <Line data={chartData} options={{ maintainAspectRatio: false }} />
          </Box>
        </Paper>
      )}
    </Box>
  );
} 