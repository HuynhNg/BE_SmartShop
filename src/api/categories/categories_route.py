from fastapi import APIRouter,  Depends
from src.api.categories.categories_controller import CategoriesController
from src.dto.category_dto import CategoryCreateDTO
from src.middlewares.verify_middleware import admin_verify
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/categories", tags=["Categories"])
categories_ctl = CategoriesController()

@router.get("/")
@cache(expire=300)
def get_all_categories():
    return categories_ctl.get_all_categories()

@router.get("/{id}")
def get_category_byID(id: int):
    return categories_ctl.get_category_byID(id)

@router.get("/{id}/Products")
@cache(expire=300)
def get_all_products_byCategoryID(id: int):
    return categories_ctl.get_all_products_byCategoryID(id)

@router.post("/", dependencies=[Depends(admin_verify)])
def create_category(category: CategoryCreateDTO):
    return categories_ctl.create_category(category)

@router.put("/{id}", dependencies=[Depends(admin_verify)])
def update_category(id: int, category: CategoryCreateDTO):
    return categories_ctl.update_category(id, category)

@router.delete("/{id}", dependencies=[Depends(admin_verify)])
def delete_category(id: int):
    return categories_ctl.delete_category(id)
