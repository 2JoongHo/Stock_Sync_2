"""재고 입출고 CRUD"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
from domain.stock.stock_schema import StockInCreate, StockOutCreate

def process_stock_in(db: Session, stock_in: StockInCreate) -> models.StockTransaction:
    """자재 입고 처리"""

    # 대상 품목 조회
    item = (
        db.query(models.Item).filter(models.Item.id == stock_in.item_id).first())
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {stock_in.item_id}번 품목을 찾을 수 없습니다."
        )

    # 품목 현재고 증가
    item.current_stock += stock_in.quantity

    # 입고 전표 객체 생성 (유형은 'IN'으로 고정 주입)
    tx = models.StockTransaction(
        item_id=stock_in.item_id,
        transaction_type="IN",
        quantity=stock_in.quantity,
        reference_note=stock_in.reference_note,
    )
    db.add(tx)

    # 재고 증가와 전표 저장을 한 번에 커밋
    db.commit()
    db.refresh(tx)

    return tx

def process_stock_out(db: Session, stock_out: StockOutCreate) -> models.StockTransaction:
    """자재 출고 처리"""

    # 대상 품목 조회
    item = (
        db.query(models.Item)
        .filter(models.Item.id == stock_out.item_id)
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {stock_out.item_id}번 품목을 찾을 수 없습니다."
        )

    # 재고 부족 검증
    if item.current_stock < stock_out.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"재고가 부족합니다. (현재 재고: {item.current_stock}),"
                f"요청 수량: {stock_out.quantity}개"
            )
        )

    # 현재 재고 차감
    item.current_stock -= stock_out.quantity

    # 출고 전표 객체 생성
    tx = models.StockTransaction(
        item_id=stock_out.item_id,
        transaction_type="OUT",
        quantity=stock_out.quantity,
        reference_note=stock_out.reference_note,
    )
    db.add(tx)

    # 재고 감소와 전표 저장을 한 번에 커밋
    db.commit()
    db.refresh(tx)

    return tx