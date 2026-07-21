from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import image_router, document_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=False, # 允许跨域请求携带凭据（如 Cookies）
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(image_router, tags=['图片模块'])
app.include_router(document_router, tags=['文件模块'])

if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080)