"""재고 입출고 도메인 스키마"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StockInCreate(BaseModel):
    """자재 입고 요청 (클라이언트 -> 서버)"""

    item_id: int = Field(..., description="입고할 제품 ID")
    quantity: int = Field(..., gt=0, description="입고 수량 (1개 이상)")
    reference_note: str | None = Field(default=None, description="입고 비고")


class StockTransactionResponse(BaseModel):
    """입출고 전표 응답 (서버 -> 클라이언트))"""

    id: int
    item_id: int
    transaction_type: str
    quantity: int
    reference_note: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StockOutCreate(BaseModel):
    """자재 출고 요청 (클라이언트 -> 서버)"""

    item_id: int = Field(..., description="출고할 제품 ID")
    quantity: int = Field(..., gt=0, description="출고 수량 (1개 이상)")
    reference_note: str | None = Field(default=None, description="출고 비고")
