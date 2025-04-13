# NNLab - 神经网络实验室

NNLab是一个交互式的神经网络可视化和实验平台，旨在帮助用户更好地理解和学习神经网络的工作原理。

## 功能特点

- 📊 实时可视化神经网络结构
- 🔄 动态调整网络参数
- 📈 3D数据可视化
- 🎯 支持多种训练数据集
- 🛠️ 自定义网络架构
- 📱 响应式界面设计

## 技术栈

- 前端框架：React + TypeScript
- 状态管理：Redux
- 可视化：D3.js + Three.js
- UI组件：Material-UI
- 构建工具：Vite
- 后端：Python + FastAPI
- 机器学习框架：PyTorch

## 快速开始

### 环境要求

- Node.js >= 16.0.0
- Python >= 3.8
- pip >= 21.0.0

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/darrenhwang/nnlab.git
cd nnlab
```

2. 安装前端依赖
```bash
cd frontend
npm install
```

3. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

4. 启动开发服务器
```bash
# 前端
cd frontend
npm run dev

# 后端
cd backend
uvicorn main:app --reload
```

## 项目结构

```
nnlab/
├── frontend/           # 前端代码
│   ├── src/           
│   │   ├── components/  # React组件
│   │   ├── pages/      # 页面组件
│   │   ├── store/      # Redux状态管理
│   │   └── utils/      # 工具函数
│   └── public/         # 静态资源
├── backend/           # 后端代码
│   ├── api/           # API接口
│   ├── models/        # 神经网络模型
│   ├── utils/         # 工具函数
│   └── tests/         # 测试文件
└── docs/             # 文档
```

## API文档

详细的API文档请参考 [API文档](./docs/api.md)

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情 