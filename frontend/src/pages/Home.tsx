import { Box, Typography, Card, CardContent, Grid } from '@mui/material';

export default function Home() {
  const features = [
    {
      title: '可视化模型构建',
      description: '通过直观的图形界面构建神经网络模型，无需编写代码。'
    },
    {
      title: '实时训练监控',
      description: '实时查看模型训练过程，包括损失函数、准确率等指标的变化。'
    },
    {
      title: '网络结构可视化',
      description: '以3D方式展示神经网络结构，帮助理解网络架构。'
    },
    {
      title: '训练结果分析',
      description: '详细分析模型性能，包括混淆矩阵、ROC曲线等评估指标。'
    }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        欢迎使用神经网络实验室
      </Typography>
      <Typography variant="subtitle1" paragraph>
        这是一个用于学习和实验神经网络的交互式平台。您可以在这里构建、训练和可视化神经网络模型。
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} key={index}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
} 