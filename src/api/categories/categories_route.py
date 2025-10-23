from fastapi import APIRouter
from src.api.categories.categories_controller import CategoriesController
from src.dto.category_dto import CategoryCreateDTO

router = APIRouter(prefix="/categories", tags=["Categories"])
categories_ctl = CategoriesController()

@router.get("/")
def get_all_categories():
    return categories_ctl.get_all_categories()

@router.get("/{id}")
def get_category_byID(id: int):
    return categories_ctl.get_category_byID(id)

@router.get("/{id}/Products")
def get_all_products_byCategoryID(id: int):
    return categories_ctl.get_all_products_byCategoryID(id)

@router.post("/create")
def create_category(category: CategoryCreateDTO):
    return categories_ctl.create_category(category)

@router.put("/update/{id}")
def update_category(id: int, category: CategoryCreateDTO):
    return categories_ctl.update_category(id, category)

@router.delete("/delete/{id}")
def delete_category(id: int):
    return categories_ctl.delete_category(id)
