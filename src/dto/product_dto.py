from pydantic import BaseModel

class Product(BaseModel):
    ProductID: int
    ProductName: str
    Price: int
    CategoryID: int
    isActive: bool

class ProductCreateDTO(BaseModel):
    ProductName: str
    Price: int
    CategoryID: int
    Quantity: int
    UserID: int
    UserName: str
    Email: str

class ProductResponseDTO(BaseModel):
    ProductID : int
    ProductName: str
    Category: str
    Price: int
    isActive: bool