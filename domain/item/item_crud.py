"""품목(Item) 도메인의 데이터베이스 CRUD 연산 모듈."""

from sqlalchemy.orm import Session
import models

def get_item_list(db: Session):
    """전체 품목 목록을 최신 등록일 순으로 조회"""
    return db.query(models.Item).order_by(models.Item.created_at.desc()).all()