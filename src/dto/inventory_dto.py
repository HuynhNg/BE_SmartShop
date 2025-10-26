from pydantic import BaseModel

class InventoryDTO(BaseModel):
    ProductID: int
    Quantity: int

class InventoryLogDTO(BaseModel):
    ProductID: int
    Quantity: int
    UserID: int


class InventoryLog_full(BaseModel):
    ProductID: int
    ProductName: str
    Quantity: int
    UserID: int
    UserName: str