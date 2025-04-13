from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="测试API带控制器",
    description="测试API服务带控制器",
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

# 创建简单控制器
simple_router = APIRouter()

@simple_router.get("/simple")
async def simple_endpoint():
    return {"message": "This is a simple endpoint from controller"}

# 注册路由
app.include_router(simple_router, prefix="/api", tags=["简单控制器"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "API is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8031) 