from typing import Dict, Any, List, Callable
import asyncio
import os
from datetime import datetime
import json
import uuid
import logging
import random
import time
import math

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量存储训练进度
training_progress = {}
training_history = {}

class MockTrainingService:
    """完全模拟的训练服务，不依赖PyTorch"""
    def __init__(self):
        # 创建模型保存目录
        self.models_dir = "saved_models"
        os.makedirs(self.models_dir, exist_ok=True)
    
    async def train_model(self, model_id: str, dataset: str, batch_size: int, 
                         epochs: int, learning_rate: float):
        """模拟训练模型"""
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
            
            # 模拟参数
            # 基于数据集的不同，模拟不同的数据大小
            if dataset == 'mnist':
                total_batches = 600  # 约60000样本，每批100个
                max_accuracy = 0.98
            elif dataset == 'cifar10':
                total_batches = 500  # 约50000样本，每批100个
                max_accuracy = 0.90
            else:  # fashion_mnist
                total_batches = 600
                max_accuracy = 0.92
            
            # 训练指标记录
            metrics = []
            best_accuracy = 0.0
            best_model_path = None
            
            # 模拟训练过程
            for epoch in range(epochs):
                # 更新状态为训练中
                training_progress[model_id]['status'] = 'training'
                training_progress[model_id]['epoch'] = epoch + 1
                
                # 初始损失（较高）和准确率（较低）
                base_loss = 2.0 * math.exp(-0.5 * epoch)  # 损失随着epoch指数下降
                base_accuracy = max_accuracy * (1 - math.exp(-0.4 * (epoch + 1)))  # 准确率随着epoch逐渐提高
                
                for batch in range(total_batches):
                    # 模拟每批次的训练
                    batch_progress = batch / total_batches
                    
                    # 添加一些随机性以模拟训练波动
                    loss = base_loss * (1 + 0.1 * random.random() - 0.05)
                    accuracy = base_accuracy * (1 + 0.05 * random.random() - 0.025)
                    
                    # 限制准确率最大值
                    accuracy = min(accuracy, max_accuracy)
                    
                    # 每10批次更新一次进度
                    if batch % 10 == 9 or batch == total_batches - 1:
                        progress = {
                            'epoch': epoch + 1,
                            'batch': batch + 1,
                            'loss': loss,
                            'accuracy': accuracy,
                            'progress': (epoch * total_batches + batch) / (epochs * total_batches) * 100
                        }
                        
                        metrics.append(progress.copy())
                        training_progress[model_id].update(progress)
                        
                        logger.info(f"Model {model_id}: Epoch {epoch+1}/{epochs}, Batch {batch+1}/{total_batches}, "
                                   f"Loss: {loss:.4f}, Accuracy: {accuracy:.2f}%")
                        
                        # 释放CPU时间给其他任务并模拟训练时间
                        await asyncio.sleep(0.05)
                
                # 每个epoch结束，检查是否为最佳模型
                epoch_accuracy = training_progress[model_id]['accuracy']
                if epoch_accuracy > best_accuracy:
                    best_accuracy = epoch_accuracy
                    best_model_path = self._save_model(model_id, epoch + 1, epoch_accuracy)
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
    
    def _save_model(self, model_id: str, epoch: int, accuracy: float) -> str:
        """模拟保存模型到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{model_id}_{timestamp}_epoch{epoch}_acc{accuracy:.2f}.mock"
        filepath = os.path.join(self.models_dir, filename)
        
        # 创建一个空文件模拟模型文件
        with open(filepath, 'w') as f:
            json.dump({
                'model_id': model_id,
                'epoch': epoch,
                'accuracy': accuracy,
                'timestamp': timestamp,
                'type': 'mock_model'
            }, f, indent=2)
        
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
                        accuracy = parts[3].replace('acc', '').replace('.mock', '')
                        
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
    """模拟评估模型性能"""
    try:
        # 检查模型文件是否存在
        if not os.path.exists(model_path):
            return {'error': f'Model file not found: {model_path}'}
        
        # 读取模型信息
        with open(model_path, 'r') as f:
            model_info = json.load(f)
        
        # 模拟评估过程
        await asyncio.sleep(1)  # 模拟评估时间
        
        # 从模型信息中获取准确率，并添加一些随机变化
        base_accuracy = model_info.get('accuracy', 90.0)
        accuracy = base_accuracy * (0.95 + 0.1 * random.random())  # 模拟测试集上的准确率稍低
        
        # 模拟按类别的准确率
        class_accuracy = []
        for i in range(10):
            class_acc = accuracy * (0.9 + 0.2 * random.random())
            correct = int(100 * (class_acc / 100))
            total = 100
            
            class_accuracy.append({
                'class': i,
                'accuracy': class_acc,
                'correct': correct,
                'total': total
            })
        
        return {
            'accuracy': accuracy,
            'total_samples': 1000,
            'correct_predictions': int(10 * accuracy),
            'class_accuracy': class_accuracy,
            'model_path': model_path,
            'dataset': dataset
        }
    
    except Exception as e:
        logger.error(f"评估错误: {str(e)}")
        return {'error': str(e)} 