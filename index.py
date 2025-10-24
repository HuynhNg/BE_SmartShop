from fastapi import FastAPI
from src.api.products.products_route import router as product_router
from src.api.categories.categories_route import router as categories_router
from src.api.auth.auth_route import router as auth_router
from fastapi.responses import JSONResponse

app = FastAPI()


# Gắn router
app.include_router(product_router)
app.include_router(categories_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "index:app",
        # host="0.0.0.0",
        port=8080,
        reload=True, 
        log_level="info"
    )