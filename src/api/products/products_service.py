# from pydantic import BaseModel
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.model.products_model import Products_model
from src.dto.product_dto import ProductCreateDTO, Product
from src.dto.inventory_dto import InventoryDTO, InventoryLogDTO

class ProductsService():
    def get_all_products(self,page: int, size: int = 20, sort_order: int = None):
        try:
            products = Products_model.get_all_products(page, size, sort_order)
            return products
        except Exception as e:
            raise e
    def get_product_byID(self,id: int):
        try:
            product = Products_model.get_product_byID(id)
            return product
        except Exception as e:
            raise e
    def create_product(self,product: ProductCreateDTO):
        try:
            return Products_model.create_product(product)
        except Exception as e:
            raise e
    
    def update_product(self,product: Product, check_newName: int):
        try:
            return Products_model.update_product(product, check_newName)
        except Exception as e:
            raise e
    
    def delete_product(self, id: int):
        try:
            return Products_model.delete_product(id)
        except Exception as e:
            raise e