class MockService:
    """模拟服务类，替代真实服务以解决依赖问题"""
    
    def __init__(self):
        self.data = {}
    
    def evaluate_model(self, model=None, model_path=None, dataset=None, batch_size=64):
        """模拟评估模型方法"""
        return {
            "status": "success",
            "accuracy": 0.95,
            "loss": 0.05,
            "metrics": {
                "precision": 0.94,
                "recall": 0.93,
                "f1": 0.93
            },
            "dataset": dataset,
            "model_path": model_path
        }
        
    def get_model(self, model_id):
        """获取模型"""
        return {
            "id": model_id,
            "name": f"Model {model_id}",
            "type": "CNN",
            "created_at": "2025-04-13"
        } 