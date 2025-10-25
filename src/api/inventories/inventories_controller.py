from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.api.inventories.inventories_service import InventoriesService
from src.dto.inventory_dto import InventoryDTO, InventoryLog_full
from src.api.products.products_service import ProductsService
from src.model.users_model import Users_model

class InventoriesController():
    def get_all_inventories(self, Page: int = 1):
        try:
            inventories_sv = InventoriesService()
            inventories = inventories_sv.get_all_inventories(Page)
            return JSONResponse(
                content=jsonable_encoder({
                    "message": "Inventoris retrieved successfully",
                    "length": len(inventories),
                    "inventories": [inventorie.dict() for inventorie in inventories],
                }),
                status_code=200,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def get_inventory_byProductID(self, ProductID: int):
        try:
            inventories_sv = InventoriesService()
            products_sv = ProductsService()
            item = products_sv.get_product_byID(ProductID)
            if not item:
                return JSONResponse(
                content=jsonable_encoder({
                    "message": "Product not found",
                }),
                status_code=404,
            )
            inventorie = inventories_sv.get_inventory_byProductID(ProductID)
            return JSONResponse(
                content=jsonable_encoder({
                    "message": "Inventoris retrieved successfully",
                    "inventorie": inventorie.dict(),
                }),
                status_code=200,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def restock(self, product: InventoryDTO, payload: dict):
        try:
            inventories_sv = InventoriesService()
            products_sv = ProductsService()
            item = products_sv.get_product_byID(product.ProductID)
            if not item:
                return JSONResponse(
                content=jsonable_encoder({
                    "message": "Product not found",
                }),
                status_code=404,
            )
            user_id = payload.get("UserID") or payload.get("user_id")
            user = Users_model.get_user_byID(user_id)
            inventory_log = InventoryLog_full(
                ProductID= product.ProductID,
                ProductName= item.ProductName,
                UserID= user_id,
                UserName= user.UserName,
                Quantity= product.Quantity
            )
            inventories_sv.restock(product, inventory_log)
            return JSONResponse(
                content=jsonable_encoder({
                    "message": "restock successfully",
                }),
                status_code=200,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
