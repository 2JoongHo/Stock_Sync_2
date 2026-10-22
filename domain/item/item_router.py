"""품목(Item) 도메인의 HTTP 엔드포인트 라우팅 모듈"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from domain.item import item_crud, item_schema

router = APIRouter(
    prefix="/api/item",
    tags=["item"],
)

@router.get("/list", 
            response_model=list[item_schema.Item]
            )
def item_list(db: Session = Depends(get_db)):
    """등록된 전체 품목 목록 조회"""
    items = item_crud.get_item_list(db)
    return items

@router.post("/create", 
            status_code=status.HTTP_201_CREATED, 
            response_model=item_schema.Item,
            )
def item_create(_item_create: item_schema.ItemCreate, db: Session = Depends(get_db)):
    """신규 품목을 등록하고 생성된 품목 정보 반환"""
    item = item_crud.create_item(db=db, item_create=_item_create)
    return item
