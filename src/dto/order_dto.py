from pydantic import BaseModel
from datetime import datetime
from typing import List

class Order(BaseModel):
    OrderID: int
    UserID: int
    UserName: str
    Address: str
    PhoneNumber: str
    Price: int
    OrderDate: datetime

class OrderDetail(BaseModel):
    OrderDetailID: int
    OrderID: int
    ProductID: int
    ProductName: str
    Quantity: int
    Unit_price: int


class NewOrderDetail(BaseModel):
    ProductID: int
    Quantity: int

class NewOrder(BaseModel):
    UserName: str = ""
    Address: str = ""
    PhoneNumber: str = ""
    Email: str = ""
    Orderdetail: List[NewOrderDetail] 
