from fastapi import FastAPI
from src.api.products.products_route import router as product_router
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def get_root():
    try:
        data =  {"message": "Hello, World!"}
        return JSONResponse(content = data, status_code=200)
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content = "{error: Internal Server Error}", status_code=500)

# Gắn router
app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "index:app",
        # host="0.0.0.0",
        port=8080,
        reload=True, 
        log_level="info"
    )