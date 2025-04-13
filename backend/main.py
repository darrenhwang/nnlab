from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import model, training

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

# 注册路由
app.include_router(model.router, prefix="/api/models", tags=["models"])
app.include_router(training.router, prefix="/api", tags=["training"])

@app.get("/")
async def root():
    return {"message": "Welcome to NNLab API"} 