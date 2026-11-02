"""StockSync 애플리케이션 진입점 및 라우터 등록 모듈"""

from fastapi import FastAPI
from domain.item import item_router
from domain.stock import stock_router

app = FastAPI()

app.include_router(item_router.router)  # 전체 품목 라우터
app.include_router(stock_router.router) # 재고 입출고 라우터

@app.get("/hello")
def hello():
    return {"message": "안녕하세요 스톡싱크"}