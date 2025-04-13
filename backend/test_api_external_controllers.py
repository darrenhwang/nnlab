from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.simple import router as simple_router

app = FastAPI(
    title="测试API外部控制器",
    description="测试API服务外部控制器",
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

# 注册外部路由
app.include_router(simple_router, prefix="/api/simple", tags=["简单控制器"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "API is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8032) 