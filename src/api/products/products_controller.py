from src.api.products.products_service import ProductsService
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.dto.product_dto import ProductResponseDTO, ProductCreateDTO, Product

class ProductsController():
    def get_all_products(self,page: int ):
        try:
            products_sv = ProductsService()
            products = products_sv.get_all_products(page)
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
    
    def get_product_byID(self,id: int):
        try:
            products_sv = ProductsService()
            product = products_sv.get_product_byID(id)
            if not product:
                return JSONResponse(
                    content={
                        "message": "Product not found",
                    },
                    status_code=404
                )

            return JSONResponse(
                content={
                    "message": "Products retrieved successfully",
                    "product": product.dict()
                },
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def create_product(self, product: ProductCreateDTO):
        try:
            product_sv = ProductsService()

            if product.Quantity < 0:
                return JSONResponse(
                    content={
                        "message": "Failed to create product (Quantity >= 0)",
                    },
                    status_code=400
                )

            if product.Price <= 0:
                return JSONResponse(
                    content={
                        "message": "Failed to create product (Price > 0)",
                    },
                    status_code=400
                )

            product_id = product_sv.create_product(product)
            if product_id:
                return JSONResponse(
                    content={
                        "message": "Product created successfully",
                        "product": {"id": product_id}
                    },
                    status_code=201
                )

        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_product(self,product: Product):
        try:
            product_sv = ProductsService()

            if product.ProductID is None or product.CategoryID is None or product.Price is None or product.isActive is None:
                return JSONResponse(
                    content={"message": "Please fill in all information"},
                    status_code=400
                )

            if product.Price <= 0:
                return JSONResponse(
                    content={"message": "Failed to update product (Price > 0)"},
                    status_code=400
                )
            old_product = product_sv.get_product_byID(product.ProductID)
            if old_product is None:
                return JSONResponse(
                    content={"message": "Product not found"},
                    status_code=404
                )
            check_newName =  (old_product.ProductName != product.ProductName)
            # Update
            product_sv.update_product(product, check_newName)

            return JSONResponse(
                content={"message": "Product updated successfully"},
                status_code=200
            )

        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete_product(self, id: int):
        try:
            product_sv = ProductsService()

            product = product_sv.get_product_byID(id)
            if product is None:
                return JSONResponse(
                    content={"message": "Product not found"},
                    status_code=404
                )
            product_sv.delete_product(id)

            return JSONResponse(
                content={"message": "Product deleted successfully"},
                status_code=200
            )

        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")