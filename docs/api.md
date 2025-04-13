# NNLab API 文档

## API 概述

NNLab API 提供了一系列端点用于神经网络的创建、训练和可视化。所有API都遵循RESTful设计原则。

## 基础URL

```
http://localhost:8000/api/v1
```

## 认证

所有API请求需要在header中包含JWT token：

```
Authorization: Bearer <your_token>
```

## API 端点

### 1. 神经网络模型

#### 创建模型

```http
POST /models
```

请求体：
```json
{
  "name": "my_model",
  "layers": [
    {
      "type": "dense",
      "units": 64,
      "activation": "relu"
    },
    {
      "type": "dense",
      "units": 10,
      "activation": "softmax"
    }
  ]
}
```

响应：
```json
{
  "id": "model_123",
  "status": "created",
  "created_at": "2024-03-20T10:00:00Z"
}
```

#### 获取模型列表

```http
GET /models
```

响应：
```json
{
  "models": [
    {
      "id": "model_123",
      "name": "my_model",
      "status": "trained",
      "created_at": "2024-03-20T10:00:00Z"
    }
  ]
}
```

### 2. 训练

#### 开始训练

```http
POST /models/{model_id}/train
```

请求体：
```json
{
  "dataset": "mnist",
  "batch_size": 32,
  "epochs": 10,
  "learning_rate": 0.001
}
```

响应：
```json
{
  "training_id": "train_456",
  "status": "started"
}
```

#### 获取训练状态

```http
GET /models/{model_id}/train/{training_id}
```

响应：
```json
{
  "status": "in_progress",
  "current_epoch": 5,
  "metrics": {
    "loss": 0.234,
    "accuracy": 0.945
  }
}
```

### 3. 预测

#### 进行预测

```http
POST /models/{model_id}/predict
```

请求体：
```json
{
  "input": [
    [0.1, 0.2, 0.3, 0.4]
  ]
}
```

响应：
```json
{
  "predictions": [
    [0.7, 0.3]
  ]
}
```

### 4. 可视化

#### 获取网络结构

```http
GET /models/{model_id}/structure
```

响应：
```json
{
  "layers": [
    {
      "id": "layer_1",
      "type": "dense",
      "units": 64,
      "weights": [...],
      "activations": [...]
    }
  ],
  "connections": [...]
}
```

#### 获取激活图

```http
GET /models/{model_id}/activations
```

响应：
```json
{
  "layer_activations": {
    "layer_1": [...],
    "layer_2": [...]
  }
}
```

## 错误处理

API使用标准HTTP状态码表示请求状态：

- 200: 成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器内部错误

错误响应格式：

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "详细错误信息"
  }
}
```

## 速率限制

- 基础用户：100次请求/小时
- 高级用户：1000次请求/小时

超出限制将返回429状态码。

## WebSocket API

用于实时训练数据和可视化更新：

```
ws://localhost:8000/ws/models/{model_id}/stream
```

### 事件类型

1. 训练更新
```json
{
  "type": "training_update",
  "data": {
    "epoch": 1,
    "loss": 0.234,
    "accuracy": 0.945
  }
}
```

2. 网络状态更新
```json
{
  "type": "network_state",
  "data": {
    "layer_states": {...},
    "gradients": {...}
  }
}
``` 