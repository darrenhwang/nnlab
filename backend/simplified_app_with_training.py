from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simplified_training_controllers import router as training_router

app = FastAPI(
    title="神经网络实验室API",
    description="具有训练和评估功能的神经网络实验室API",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加训练路由
app.include_router(training_router, prefix="/api", tags=["训练与评估"])

@app.get("/")
async def root():
    return {"message": "Hello from Neural Network Lab API"}

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "API is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8050) 