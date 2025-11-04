from fastapi import APIRouter, Depends
from src.dto.product_dto import ProductCreateDTO, Product
from src.middlewares.verify_middleware import admin_verify
from src.api.products.products_controller import ProductsController
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/products", tags=["Products"])

products_ctl = ProductsController()

@router.get("/")
@cache(expire=300)
def get_all_products(page: int = 1, size: int = 20, sort_order: int = None):
    return products_ctl.get_all_products(page, size, sort_order)
    
@router.get("/{id}")
def get_product_byID(id: int):
    return products_ctl.get_product_byID(id)

@router.post("/", dependencies=[Depends(admin_verify)])
def create_product(Product: ProductCreateDTO):
    return products_ctl.create_product(Product)

@router.put("/", dependencies=[Depends(admin_verify)])
def update_product(product: Product):
    return products_ctl.update_product(product)

@router.delete("/{id}", dependencies=[Depends(admin_verify)])
def delete_product(id: int):
    return products_ctl.delete_product(id)