from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NNLab API",
    description="神经网络实验室API",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 暂时移除所有控制器
# from controllers import evaluation
# app.include_router(evaluation.router, prefix="/api", tags=["评估"])
# from controllers import training
# app.include_router(training.router, prefix="/api", tags=["训练"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "API is working"} 