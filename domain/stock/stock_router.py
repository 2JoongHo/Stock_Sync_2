"""자재 입출고 라우터 모듈"""

from fastapi import APIRouter, status, Depends
from domain.stock import stock_schema, stock_crud
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/api/stock", tags=["stock"])


@router.post(
    "/in",
    response_model=stock_schema.StockTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="자재 입고 등록",
)
def stock_in(stock_in_data: stock_schema.StockInCreate, db: Session = Depends(get_db)):
    """자재 입고 처리"""
    return stock_crud.process_stock_in(db=db, stock_in=stock_in_data)


@router.post(
    "/out",
    response_model=stock_schema.StockTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="자재 출고 등록",
)
def stock_out(
    stock_out_data: stock_schema.StockOutCreate, db: Session = Depends(get_db)
):
    """자재 출고 처리
    - 재고가 부족할 경우 400 BAD REQUEST 반환
    - 재고가 충분할 시 현 재고 차감"""
    return stock_crud.process_stock_out(db=db, stock_out=stock_out_data)
