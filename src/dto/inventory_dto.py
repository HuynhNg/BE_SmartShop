from pydantic import BaseModel

class InventoryDTO:
    ProductID: int
    Quantity: int

class InventoryLogDTO:
    ProductID: int
    Quantity: int
    UserID: int