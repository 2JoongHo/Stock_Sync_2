"""품목(Item) 도메인의 입출력 데이터 검증 및 직렬화 스키마"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    """품목 조회 및 응답용 스키마"""
    id: int
    item_code: str = Field(description="제품 코드")
    name: str = Field(description="제품명")
    spec: str | None = Field(default=None, description="제품 사양")
    current_stock: int = Field(description="현재 재고")
    safety_stock: int = Field(description="안전 재고")
    location: str | None = Field(default=None, description="제품 위치")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)