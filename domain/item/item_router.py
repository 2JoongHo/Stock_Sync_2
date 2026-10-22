"""품목(Item) 도메인의 HTTP 엔드포인트 라우팅 모듈"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.item import item_crud, item_schema

router = APIRouter(
    prefix="/api/item",
    tags=["item"],
)

@router.get("/list", response_model=list[item_schema.Item])
def item_list(db: Session = Depends(get_db)):
    """등록된 전체 품목 목록 조회"""
    items = item_crud.get_item_list(db)
    return items

