from pydantic import BaseModel

class InventoryDTO(BaseModel):
    ProductID: int
    Quantity: int

class InventoryLogDTO(BaseModel):
    ProductID: int
    Quantity: int
    UserID: int
