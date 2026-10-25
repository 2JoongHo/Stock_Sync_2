"""품목(Item) 도메인의 HTTP 엔드포인트 라우팅 모듈"""

from fastapi import APIRouter, Depends, status, HTTPException
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
    """신규 품목을 등록하고 생성된 품목 정보 반환
    이미 존재 할 경우 409 에러 반환"""
    # 1. 이미 존재하는지 확인
    existing_item = item_crud.get_item_by_code(
        db, item_code=_item_create.item_code
    )
    if existing_item:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"이미 존재하는 제품 코드입니다: {_item_create.item_code}"
        )
    # 2. 중복이 아닐 시 정상적으로 생성
    item = item_crud.create_item(db=db, item_create=_item_create)
    return item

@router.get("/{item_id}",
            response_model=item_schema.Item)
def item_detail(item_id: int,
                db: Session = Depends(get_db)):
    """ID로 개별 품목 정보 조회
    없을 시 404 에러 반환"""
    item = item_crud.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"해당 ID의 품목을 찾을 수 없습니다: {item_id}"
        )
    return item
