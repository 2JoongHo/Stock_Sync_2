"""품목(Item) 도메인의 입출력 데이터 검증 및 직렬화 스키마"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class Item(BaseModel):
    """품목 조회 및 응답용"""
    id: int
    item_code: str = Field(description="제품 코드")
    name: str = Field(description="제품명")
    spec: str | None = Field(default=None, description="제품 사양")
    current_stock: int = Field(description="현재 재고")
    safety_stock: int = Field(description="안전 재고")
    location: str | None = Field(default=None, description="제품 위치")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    """신규 품목 등록 요청용"""
    item_code: str = Field(description="제품 코드")
    name: str = Field(description="제품명")
    spec: str | None = Field(default=None, description="제품 사양")
    current_stock: int = Field(default=0, ge=0, description="현재 재고")
    safety_stock: int = Field(default=0, ge=0, description="안전 재고")
    location: str | None = Field(default=None, description="제품 위치")

    @field_validator("item_code", "name")
    def not_empty(cls, v: str) -> str:
        """필수 문자열 필드에 공백 입력 차단"""
        if not v or not v.strip():
            raise ValueError("빈 문자열이거나 공백만 입력할 수 없습니다.")
        return v

class ItemUpdate(BaseModel):
    """품목 수정"""
    name: str = Field(description="제품명")
    spec: str | None = Field(default=None, description="제품 사양")
    current_stock: int = Field(default=0, ge=0, description="현재 재고")
    safety_stock: int = Field(default=0, ge=0, description="안전 재고")
    location: str | None = Field(default=None, description="제품 위치")

    @field_validator("name")
    def check_not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError("제품명은 빈 값일 수 없습니다.")
        return v
