from src.model.categories_model import Categories_model
from src.dto.category_dto import CategoryCreateDTO

class CategoriesService():
    def get_all_categories(self):
        try:
            return Categories_model.get_all_categories()
        except Exception as e:
            raise e
    
    def get_category_byID(self, CategoryID):
        try:
            return Categories_model.get_category_byID(CategoryID)
        except Exception as e:
            raise e
    
    def get_all_products_byCategoryID(self, CategoryID):
        try:
            return Categories_model.get_all_products_byCategoryID(CategoryID)
        except Exception as e:
            raise e
    
    def create_category(self, category: CategoryCreateDTO):
        try:
            return Categories_model.create_category(category)
        except Exception as e:
            raise e
        
    def update_category(self, CategoryID, category: CategoryCreateDTO):
        try:
            return Categories_model.update_category(CategoryID, category)
        except Exception as e:
            raise e
        
    def delete_category(self, CategoryID):
        try:
            return Categories_model.delete_category(CategoryID)
        except Exception as e:
            raise e