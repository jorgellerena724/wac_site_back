from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel
from sqlmodel import JSON, Column, Field, Relationship, SQLModel
from sqlalchemy import Text

class ProductVariant(BaseModel):
    description: str
    price: float
    
class ProductImage(BaseModel):
    title: str
    media: str

if TYPE_CHECKING:
    from .wep_category_model import WepCategoryModel

class WepProductModel(SQLModel, table=True):
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None, max_length=100, nullable=True)
    description: Optional[str] = Field(default=None, sa_type=Text(), nullable=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", nullable=True)
    status: bool      = Field(nullable=False, default=True)
    cal_url: str = Field(max_length=255, nullable=True)
    
    variants: List[ProductVariant] = Field(
        sa_column=Column(JSON), 
        default=[]
    )
    
    files: List[ProductImage] = Field(
        sa_column=Column(JSON), 
        default=[]
    )
    
    category: Optional["WepCategoryModel"] = Relationship(
        back_populates="products",
        sa_relationship_kwargs={"lazy": "joined"}  # Carga automática
    )
    class Config:
        from_attributes = True

    def __repr__(self):
        return f"<WepProductModel(nombre={self.title})>"