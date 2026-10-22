"""재고 관리 핵심 엔티티(품목, 재고 이력) ORM 모델 정의."""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String, unique=True, index=True, nullable=False) # 품번/품목 코드
    name = Column(String, nullable=False) # 품명
    spec = Column(String, nullable=True) # 규격/사양
    current_stock = Column(Integer, default=0, nullable=False) # 현재 재고 수량
    safety_stock = Column(Integer, default=0, nullable=False) # 적정/안전재고
    location = Column(String, nullable=True) # 창고 내 보관 위치
    created_at = Column(DateTime, default=datetime.utcnow) # 등록 일시