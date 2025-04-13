from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simplified_controllers import evaluation_router, simple_router

app = FastAPI(
    title="简化版NNLab API",
    description="简化版神经网络实验室API",
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

# 添加路由
app.include_router(evaluation_router, prefix="/api", tags=["评估"])
app.include_router(simple_router, prefix="/api/simple", tags=["简单"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "API is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8040) 