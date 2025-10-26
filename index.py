from fastapi import FastAPI
from src.api.products.products_route import router as product_router
from src.api.categories.categories_route import router as categories_router
from src.api.auth.auth_route import router as auth_router
from src.api.order.orders_router import router as order_router
from src.api.users.users_router import router as users_router
from src.api.inventories.inventories_route import router as inventories_router
from fastapi.responses import JSONResponse

app = FastAPI()


# Gắn router
app.include_router(product_router)
app.include_router(categories_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(inventories_router)
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    import os

    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_config_path = os.path.join(os.path.dirname(__file__), "log_config.yaml")

    uvicorn.run(
        "index:app",
        port=8080,
        reload=True,
        log_config=log_config_path,  
        log_level="info"
    )
