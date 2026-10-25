"""품목(Item) 도메인의 데이터베이스 CRUD 연산 모듈"""

from sqlalchemy.orm import Session
from domain.item import item_schema
import models

def get_item_list(db: Session):
    """전체 품목 목록을 최신 등록일 순으로 조회"""
    return db.query(models.Item).order_by(models.Item.created_at.desc()).all()

def get_item(db: Session, item_id: int) -> models.Item | None:
    """ID로 개별 품목 조회"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_item_by_code(db: Session, item_code: str) -> models.Item | None:
    """품목 코드(item_code)로 품목을 조회"""
    return (db.query(models.Item).filter(models.Item.item_code == item_code).first())

def create_item(db: Session, item_create: item_schema.ItemCreate) -> models.Item:
    """검증 된 품목 데이터를 바탕으로 신규 레코드를 생성하고 DB에 영구 반영"""
    db_item = models.Item(
        item_code=item_create.item_code,
        name=item_create.name,
        spec=item_create.spec,
        current_stock=item_create.current_stock,
        safety_stock=item_create.safety_stock,
        location=item_create.location,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item