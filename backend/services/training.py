import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from typing import List, Dict, Any, Callable
import asyncio
import logging
import os
from datetime import datetime

from ..models.domain.model import Model
from ..models.schemas.training import TrainingConfig
from .training_history import TrainingHistoryService

logger = logging.getLogger(__name__)

class TrainingService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dataset_loaders = {
            'mnist': self._get_mnist_loader,
            'cifar10': self._get_cifar10_loader,
            'fashion_mnist': self._get_fashion_mnist_loader
        }
        # 创建模型保存目录
        self.models_dir = "saved_models"
        os.makedirs(self.models_dir, exist_ok=True)
        self.history_service = TrainingHistoryService()

    async def train_model(
        self, 
        config: TrainingConfig, 
        model: Model,
        progress_callback: Callable[[Dict[str, Any]], None]
    ):
        try:
            start_time = datetime.now()
            metrics = []
            
            # 构建数据加载器
            train_loader = self.dataset_loaders[config.dataset](
                batch_size=config.batch_size
            )
            
            # 构建模型
            net = self._build_model(model.layers)
            net.to(self.device)
            
            # 定义损失函数和优化器
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(net.parameters(), lr=config.learning_rate)
            
            # 开始训练
            best_accuracy = 0.0
            best_model_path = None
            for epoch in range(config.epochs):
                running_loss = 0.0
                correct = 0
                total = 0
                
                for i, (inputs, labels) in enumerate(train_loader):
                    inputs, labels = inputs.to(self.device), labels.to(self.device)
                    
                    optimizer.zero_grad()
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
                    
                    running_loss += loss.item()
                    _, predicted = outputs.max(1)
                    total += labels.size(0)
                    correct += predicted.eq(labels).sum().item()
                    
                    if i % 100 == 99:
                        accuracy = 100. * correct / total
                        avg_loss = running_loss / 100
                        progress = {
                            'epoch': epoch + 1,
                            'batch': i + 1,
                            'loss': avg_loss,
                            'accuracy': accuracy
                        }
                        metrics.append(progress)
                        await progress_callback(progress)
                        running_loss = 0.0
                        correct = 0
                        total = 0
                        
                        # 保存最佳模型
                        if accuracy > best_accuracy:
                            best_accuracy = accuracy
                            best_model_path = self._save_model(net, model.id, epoch + 1, accuracy)
                        
                        # 让出控制权给其他协程
                        await asyncio.sleep(0)
            
            end_time = datetime.now()
            
            # 记录训练历史
            self.history_service.create_history(
                model_id=model.id,
                config=config.dict(),
                start_time=start_time,
                end_time=end_time,
                final_accuracy=best_accuracy,
                final_loss=metrics[-1]['loss'] if metrics else 0.0,
                best_model_path=best_model_path,
                metrics=metrics
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Training error: {str(e)}")
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
        
        logger.info(f"Model saved to {filepath}")
        return filepath

    def _build_model(self, layers: List[Dict]) -> nn.Module:
        """根据层配置构建PyTorch模型"""
        layers_list = []
        in_features = None
        
        for layer in layers:
            if layer['type'] == 'linear':
                if in_features is None:
                    in_features = layer['units']  # 第一层
                else:
                    layers_list.extend([
                        nn.Linear(in_features, layer['units']),
                        self._get_activation(layer.get('activation', 'relu'))
                    ])
                    in_features = layer['units']
        
        return nn.Sequential(*layers_list)
    
    def _get_activation(self, name: str) -> nn.Module:
        """获取激活函数"""
        activations = {
            'relu': nn.ReLU(),
            'sigmoid': nn.Sigmoid(),
            'tanh': nn.Tanh()
        }
        return activations.get(name, nn.ReLU())
    
    def _get_mnist_loader(self, batch_size: int):
        """获取MNIST数据集加载器"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        dataset = datasets.MNIST(
            './data', 
            train=True, 
            download=True, 
            transform=transform
        )
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True
        )
    
    def _get_cifar10_loader(self, batch_size: int):
        """获取CIFAR10数据集加载器"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        dataset = datasets.CIFAR10(
            './data', 
            train=True, 
            download=True, 
            transform=transform
        )
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True
        )
    
    def _get_fashion_mnist_loader(self, batch_size: int):
        """获取Fashion MNIST数据集加载器"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        dataset = datasets.FashionMNIST(
            './data', 
            train=True, 
            download=True, 
            transform=transform
        )
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True
        ) 