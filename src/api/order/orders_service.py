import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.dto.order_dto import Order, OrderDetail, NewOrder
from src.dto.product_dto import ProductOrder
from src.model.orders_model import Orders_model
from typing import List

class OrdersService():
    def get_all_orders(self, Page: int):
        return Orders_model.get_all_orders(Page)
    
    def get_order_byID(self, id: int):
        return Orders_model.get_order_byID(id)
    
    def get_order_details(self, OrderID: int):
        return Orders_model.get_order_detail(OrderID)
    
    def create_order(self,user_id: int, newOrder: NewOrder, product_list: List[ProductOrder]):
        return Orders_model.create_order(user_id,newOrder, product_list)
    
    def delete_order(self, order_id : int):
        return Orders_model.delete_order(order_id)
