from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.api.categories.categories_service import CategoriesService
from src.dto.category_dto import CategoryCreateDTO

class CategoriesController():
    def get_all_categories(self):
        try:
            categories_sv = CategoriesService()
            categories = categories_sv.get_all_categories()
            return JSONResponse(
                content={
                    "message": "Categories retrived successfully",
                    "length": len(categories),
                    "categories":[category.dict() for category in categories]
                },
                status_code= 200
            )
        except Exception as e:
                print(f"Error: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def get_category_byID(self, CategoryID):
        try:
            categories_sv = CategoriesService()
            category = categories_sv.get_category_byID(CategoryID)
            if not category:
                return JSONResponse(
                    content={
                        "message": "Category not found",
                    },
                    status_code= 404
                )
            return JSONResponse(
                content={
                    "message": "Products retrieved successfully",
                    "category": category.dict()
                },
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def get_all_products_byCategoryID(self, CategoryID):
        try:
            categories_sv = CategoriesService()
            if not categories_sv.get_category_byID(CategoryID):
                return JSONResponse(
                    content={
                        "message": "Category not found",
                    },
                    status_code= 404
                )
            products = categories_sv.get_all_products_byCategoryID(CategoryID)
            return JSONResponse(
                content={
                    "message": "Products retrieved successfully",
                    "length": len(products),
                    "products": [product.dict() for product in products]
                },
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def create_category(self, category: CategoryCreateDTO):
        try:
            categories_sv = CategoriesService()
            if category.CategoryName is None or not category.CategoryName:
                return JSONResponse(
                    content={
                        "message": "Failed to create category (CategoryName is None)",
                    },
                    status_code= 400
                )
            category_id = categories_sv.create_category(category)
            if not category_id :
                return JSONResponse(
                    content={
                        "message": "Failed to create category",
                    },
                    status_code= 400
                )
            return JSONResponse(
                    content={
                        "message": "Category created successfully",
                        "category": {"id": category_id }
                    },
                    status_code=201
                )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def update_category(self, CategoryID, category: CategoryCreateDTO):
        try:
            categories_sv = CategoriesService()
            if not categories_sv.get_category_byID(CategoryID):
                return JSONResponse(
                    content={
                        "message": "Category not found",
                    },
                    status_code= 404
                )
            
            if category.CategoryName is None or not category.CategoryName:
                return JSONResponse(
                    content={
                        "message": "Failed to update category (CategoryName is None)",
                    },
                    status_code= 400
                )
            categories_sv.update_category(CategoryID, category)
            return JSONResponse(
                    content={
                        "message": "Category updated successfully",
                    },
                    status_code=200
                )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def delete_category(self, CategoryID):
        try:
            categories_sv = CategoriesService()
            if not categories_sv.get_category_byID(CategoryID):
                return JSONResponse(
                    content={
                        "message": "Category not found",
                    },
                    status_code= 404
                )
            categories_sv.delete_category(CategoryID)
            return JSONResponse(
                    content={
                        "message": "Category deleted successfully",
                    },
                    status_code=200
                )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")