from fastapi import APIRouter, Depends
from src.middlewares.verify_middleware import admin_verify
from src.dto.inventory_dto import InventoryDTO
from src.api.inventories.inventories_controller import InventoriesController

router = APIRouter(prefix="/inventories", tags=["Inventories"])
inventories_ctl = InventoriesController()

@router.get("/", dependencies=[Depends(admin_verify)])
def get_all_inventories(Page: int = 1):
    return inventories_ctl.get_all_inventories(Page)

@router.get("/{id}", dependencies=[Depends(admin_verify)])
def get_inventory_byProductID(ProductID: int):
    return inventories_ctl.get_inventory_byProductID(ProductID)

@router.post("/", dependencies=[],)
def restock(product: InventoryDTO, payload=Depends(admin_verify)):
    return inventories_ctl.restock(product, payload)