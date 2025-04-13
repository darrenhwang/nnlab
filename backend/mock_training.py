import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from typing import Dict, Any, List, Callable
import asyncio
import os
from datetime import datetime
import json
import uuid
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量存储训练进度
training_progress = {}
training_history = {}

class SimpleNN(nn.Module):
    """简单的神经网络模型"""
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)  # 展平输入
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class MockTrainingService:
    """模拟训练服务"""
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # 创建模型保存目录
        self.models_dir = "saved_models"
        os.makedirs(self.models_dir, exist_ok=True)
    
    def get_model_architecture(self, dataset: str) -> SimpleNN:
        """根据数据集获取模型架构"""
        if dataset == 'mnist' or dataset == 'fashion_mnist':
            return SimpleNN(28*28, 128, 10)
        elif dataset == 'cifar10':
            return SimpleNN(32*32*3, 256, 10)
        else:
            raise ValueError(f"不支持的数据集: {dataset}")
    
    def get_data_loader(self, dataset: str, batch_size: int, is_train=True):
        """获取数据加载器"""
        if dataset == 'mnist':
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
            data = datasets.MNIST('./data', train=is_train, download=True, transform=transform)
        
        elif dataset == 'cifar10':
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ])
            data = datasets.CIFAR10('./data', train=is_train, download=True, transform=transform)
        
        elif dataset == 'fashion_mnist':
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,))
            ])
            data = datasets.FashionMNIST('./data', train=is_train, download=True, transform=transform)
        
        else:
            raise ValueError(f"不支持的数据集: {dataset}")
        
        return torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=is_train)
    
    async def train_model(self, model_id: str, dataset: str, batch_size: int, 
                         epochs: int, learning_rate: float):
        """训练模型"""
        try:
            # 创建一个唯一的训练ID
            training_id = str(uuid.uuid4())
            
            # 记录开始时间
            start_time = datetime.now()
            
            # 初始化训练进度
            training_progress[model_id] = {
                'status': 'starting',
                'epoch': 0,
                'batch': 0,
                'loss': 0.0,
                'accuracy': 0.0,
                'progress': 0.0,
                'training_id': training_id
            }
            
            # 获取模型和数据加载器
            net = self.get_model_architecture(dataset)
            net.to(self.device)
            train_loader = self.get_data_loader(dataset, batch_size)
            
            # 定义损失函数和优化器
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(net.parameters(), lr=learning_rate)
            
            # 训练指标记录
            metrics = []
            best_accuracy = 0.0
            best_model_path = None
            
            # 开始训练
            for epoch in range(epochs):
                running_loss = 0.0
                correct = 0
                total = 0
                
                # 更新状态为训练中
                training_progress[model_id]['status'] = 'training'
                training_progress[model_id]['epoch'] = epoch + 1
                
                for i, (inputs, labels) in enumerate(train_loader):
                    inputs, labels = inputs.to(self.device), labels.to(self.device)
                    
                    # 前向 + 反向 + 优化
                    optimizer.zero_grad()
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
                    
                    # 计算统计信息
                    running_loss += loss.item()
                    _, predicted = outputs.max(1)
                    total += labels.size(0)
                    correct += predicted.eq(labels).sum().item()
                    
                    # 每100批次更新一次进度
                    if i % 100 == 99 or i == len(train_loader) - 1:
                        accuracy = 100. * correct / total
                        avg_loss = running_loss / (i % 100 + 1)
                        progress = {
                            'epoch': epoch + 1,
                            'batch': i + 1,
                            'loss': avg_loss,
                            'accuracy': accuracy,
                            'progress': (epoch * len(train_loader) + i) / (epochs * len(train_loader)) * 100
                        }
                        
                        metrics.append(progress.copy())
                        training_progress[model_id].update(progress)
                        
                        logger.info(f"Model {model_id}: Epoch {epoch+1}/{epochs}, Batch {i+1}/{len(train_loader)}, "
                                   f"Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")
                        
                        # 释放CPU时间给其他任务
                        await asyncio.sleep(0.01)
                
                # 每个epoch结束，检查是否为最佳模型
                epoch_accuracy = training_progress[model_id]['accuracy']
                if epoch_accuracy > best_accuracy:
                    best_accuracy = epoch_accuracy
                    best_model_path = self._save_model(net, model_id, epoch + 1, epoch_accuracy)
                    logger.info(f"保存最佳模型: {best_model_path}, 准确率: {best_accuracy:.2f}%")
            
            # 训练完成，更新状态
            end_time = datetime.now()
            training_progress[model_id]['status'] = 'completed'
            
            # 保存训练历史
            history = {
                'id': training_id,
                'model_id': model_id,
                'dataset': dataset,
                'batch_size': batch_size,
                'epochs': epochs,
                'learning_rate': learning_rate,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration': (end_time - start_time).total_seconds(),
                'final_accuracy': best_accuracy,
                'final_loss': metrics[-1]['loss'] if metrics else 0.0,
                'best_model_path': best_model_path,
                'metrics': metrics
            }
            
            training_history[training_id] = history
            self._save_history(history)
            
            return {
                'training_id': training_id,
                'model_id': model_id,
                'status': 'completed',
                'accuracy': best_accuracy,
                'duration': (end_time - start_time).total_seconds(),
                'best_model_path': best_model_path
            }
            
        except Exception as e:
            logger.error(f"训练错误: {str(e)}")
            if model_id in training_progress:
                training_progress[model_id]['status'] = 'error'
                training_progress[model_id]['error'] = str(e)
            raise
    
    def _save_model(self, model: nn.Module, model_id: str, epoch: int, accuracy: float) -> str:
        """保存模型到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{model_id}_{timestamp}_epoch{epoch}_acc{accuracy:.2f}.pth"
        filepath = os.path.join(self.models_dir, filename)
        
        # 保存模型状态字典
        torch.save({
            'model_state_dict': model.state_dict(),
            'epoch': epoch,
            'accuracy': accuracy
        }, filepath)
        
        return filepath
    
    def _save_history(self, history: Dict[str, Any]):
        """保存训练历史到文件"""
        history_dir = "training_history"
        os.makedirs(history_dir, exist_ok=True)
        
        filename = f"{history['model_id']}_{history['id']}.json"
        filepath = os.path.join(history_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_training_progress(self, model_id: str) -> Dict[str, Any]:
        """获取训练进度"""
        if model_id not in training_progress:
            return {'status': 'not_found', 'error': 'No training progress found'}
        return training_progress[model_id]
    
    def get_saved_models(self, model_id: str) -> List[Dict[str, Any]]:
        """获取保存的模型"""
        if not os.path.exists(self.models_dir):
            return []
        
        model_files = []
        for filename in os.listdir(self.models_dir):
            if filename.startswith(model_id):
                # 解析文件名获取信息
                parts = filename.split('_')
                if len(parts) >= 4:
                    try:
                        timestamp = parts[1]
                        epoch = parts[2].replace('epoch', '')
                        accuracy = parts[3].replace('acc', '').replace('.pth', '')
                        
                        model_files.append({
                            'filename': filename,
                            'timestamp': timestamp,
                            'epoch': int(epoch),
                            'accuracy': float(accuracy),
                            'path': os.path.join(self.models_dir, filename)
                        })
                    except Exception as e:
                        logger.error(f"解析模型文件名错误: {filename}, {str(e)}")
        
        # 按准确率排序
        model_files.sort(key=lambda x: x['accuracy'], reverse=True)
        return model_files
    
    def get_training_history(self, model_id: str = None, history_id: str = None) -> List[Dict[str, Any]]:
        """获取训练历史"""
        history_dir = "training_history"
        if not os.path.exists(history_dir):
            return []
        
        if history_id:
            # 获取特定历史记录
            for filename in os.listdir(history_dir):
                if history_id in filename:
                    filepath = os.path.join(history_dir, filename)
                    with open(filepath, 'r') as f:
                        return json.load(f)
            return None
        
        if model_id:
            # 获取特定模型的所有历史记录
            histories = []
            for filename in os.listdir(history_dir):
                if filename.startswith(model_id):
                    filepath = os.path.join(history_dir, filename)
                    with open(filepath, 'r') as f:
                        histories.append(json.load(f))
            return histories
        
        # 获取所有历史记录
        histories = []
        for filename in os.listdir(history_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(history_dir, filename)
                with open(filepath, 'r') as f:
                    histories.append(json.load(f))
        return histories

# 创建训练服务实例
mock_training_service = MockTrainingService()

# 异步评估函数
async def evaluate_model(model_path: str, dataset: str, batch_size: int) -> Dict[str, Any]:
    """评估模型性能"""
    try:
        service = MockTrainingService()
        test_loader = service.get_data_loader(dataset, batch_size, is_train=False)
        
        # 加载模型
        checkpoint = torch.load(model_path)
        model_architecture = service.get_model_architecture(dataset)
        model_architecture.load_state_dict(checkpoint['model_state_dict'])
        model_architecture.to(service.device)
        model_architecture.eval()
        
        # 评估模型
        correct = 0
        total = 0
        class_correct = [0] * 10
        class_total = [0] * 10
        
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(service.device), labels.to(service.device)
                outputs = model_architecture(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
                # 计算每个类别的准确率
                for i in range(labels.size(0)):
                    label = labels[i]
                    class_total[label] += 1
                    if predicted[i] == label:
                        class_correct[label] += 1
        
        # 计算每个类别的准确率
        class_accuracy = []
        for i in range(10):
            accuracy = 100 * class_correct[i] / max(1, class_total[i])
            class_accuracy.append({
                'class': i,
                'accuracy': accuracy,
                'correct': class_correct[i],
                'total': class_total[i]
            })
        
        return {
            'accuracy': 100 * correct / total,
            'total_samples': total,
            'correct_predictions': correct,
            'class_accuracy': class_accuracy,
            'model_path': model_path,
            'dataset': dataset
        }
    
    except Exception as e:
        logger.error(f"评估错误: {str(e)}")
        return {'error': str(e)} 