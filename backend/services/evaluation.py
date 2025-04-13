import torch
import torch.nn as nn
from torchvision import datasets, transforms
from typing import Dict, Any, List
import logging
from ..models.domain.model import Model
from torch.utils.data import DataLoader
from ..models.schemas.evaluation import EvaluationRequest

logger = logging.getLogger(__name__)

class EvaluationService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dataset_loaders = {
            'mnist': self._get_mnist_loader,
            'cifar10': self._get_cifar10_loader,
            'fashion_mnist': self._get_fashion_mnist_loader
        }

    async def evaluate_model(self, request: EvaluationRequest) -> Dict[str, Any]:
        try:
            # 加载模型
            model = torch.load(request.model_path)
            model = model.to(self.device)
            model.eval()

            # 准备数据集
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,))
            ])

            if request.dataset == 'mnist':
                test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
            elif request.dataset == 'cifar10':
                test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
            else:  # fashion_mnist
                test_dataset = datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

            test_loader = DataLoader(test_dataset, batch_size=request.batch_size, shuffle=False)

            # 评估模型
            correct = 0
            total = 0
            with torch.no_grad():
                for images, labels in test_loader:
                    images, labels = images.to(self.device), labels.to(self.device)
                    outputs = model(images)
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

            accuracy = 100 * correct / total

            return {
                "accuracy": accuracy,
                "total_samples": total,
                "correct_predictions": correct
            }

        except Exception as e:
            raise Exception(f"评估模型时出错: {str(e)}")

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
    
    def _compute_confusion_matrix(self, predictions: List[int], labels: List[int]) -> List[List[int]]:
        """计算混淆矩阵"""
        num_classes = max(max(predictions), max(labels)) + 1
        matrix = [[0] * num_classes for _ in range(num_classes)]
        
        for pred, label in zip(predictions, labels):
            matrix[label][pred] += 1
            
        return matrix
    
    def _compute_class_accuracy(self, confusion_matrix: List[List[int]]) -> List[float]:
        """计算每个类别的准确率"""
        num_classes = len(confusion_matrix)
        class_accuracy = []
        
        for i in range(num_classes):
            correct = confusion_matrix[i][i]
            total = sum(confusion_matrix[i])
            accuracy = 100. * correct / total if total > 0 else 0.0
            class_accuracy.append(accuracy)
            
        return class_accuracy
    
    def _get_mnist_loader(self, batch_size: int):
        """获取MNIST测试数据集加载器"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        dataset = datasets.MNIST(
            './data', 
            train=False, 
            download=True, 
            transform=transform
        )
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=False
        )
    
    def _get_cifar10_loader(self, batch_size: int):
        """获取CIFAR10测试数据集加载器"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        dataset = datasets.CIFAR10(
            './data', 
            train=False, 
            download=True, 
            transform=transform
        )
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=False
        )
    
    def _get_fashion_mnist_loader(self, batch_size: int):
        """获取Fashion MNIST测试数据集加载器"""
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        dataset = datasets.FashionMNIST(
            './data', 
            train=False, 
            download=True, 
            transform=transform
        )
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=False
        ) 