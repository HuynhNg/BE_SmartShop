from pydantic import BaseModel

class Category(BaseModel):
    CategoryID: int
    CategoryName: str
    Description: str

class CategoryCreateDTO(BaseModel):
    CategoryName: str
    Description: str