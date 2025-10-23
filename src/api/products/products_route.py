from fastapi import APIRouter
from src.dto.product_dto import ProductCreateDTO, Product
from src.api.products.products_controller import ProductsController

router = APIRouter(prefix="/products", tags=["Products"])

products_clt = ProductsController()

@router.get("/")
def get_all_products(page: int = 1):
    return products_clt.get_all_products(page)
    
@router.get("/{id}")
def get_product_byID(id: int):
    return products_clt.get_product_byID(id)

@router.post("/create")
def create_product(Product: ProductCreateDTO):
    return products_clt.create_product(Product)

@router.put("/update")
def update_product(product: Product):
    return products_clt.update_product(product)

@router.delete("/delete/{id}")
def delete_product(id: int):
    return products_clt.delete_product(id)