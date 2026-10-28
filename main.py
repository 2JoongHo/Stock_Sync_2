"""StockSync 애플리케이션 진입점 및 라우터 등록 모듈"""

from fastapi import FastAPI
from domain.item import item_router

app = FastAPI()

app.include_router(item_router.router)

@app.get("/hello")
def hello():
    return {"message": "안녕하세요 스톡싱크"}