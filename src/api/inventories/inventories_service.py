import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.model.inventories_model import Inventories_model

class InventoriesService():
    def get_all_inventories(self, Page: int):
        return Inventories_model.get_all_inventories(Page)
    
    def get_inventory_byProductID(self, ProductID: int):
        return Inventories_model.get_inventory_byProductID(ProductID)
    
    def restock(self, product, log):
        return Inventories_model.restock(product, log)