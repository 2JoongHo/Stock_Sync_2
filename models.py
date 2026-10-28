"""재고 관리 핵심 엔티티(품목, 재고 이력) ORM 모델 정의"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Item(Base):
    """품목 마스터 테이블"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String, unique=True, index=True, nullable=False) # 제품 코드
    name = Column(String, nullable=False) # 제품명
    spec = Column(String, nullable=True) # 제품 사양
    current_stock = Column(Integer, default=0, nullable=False) # 현재 재고
    safety_stock = Column(Integer, default=0, nullable=False) # 안전 재고
    location = Column(String, nullable=True) # 제품 위치
    created_at = Column(DateTime, default=datetime.utcnow) # 등록 일시

    stock_transactions = relationship(
        "StockTransaction", back_populates="item", cascade="all, delete-orphan"
    )

class StockTransaction(Base):
    """재고 입출고 내역 테이블"""
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)   # 품목 참조 외래키
    transaction_type = Column(String, nullable=False)   # 변동 유형
    quantity = Column(Integer, nullable=False)  # 변동 수량
    reference_note = Column(String, nullable=True)  # 비고 및 사유
    created_at = Column(DateTime, default=datetime.utcnow)  # 발생 일시

    item = relationship("Item", back_populates="stock_transactions")
