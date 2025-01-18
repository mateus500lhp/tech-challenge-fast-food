from fastapi import FastAPI
from app.adapters.driver.controllers.product_controller import router as product_router

def create_app() -> FastAPI:
    app = FastAPI(title="Fast Food Self-Service")
    app.include_router(product_router, prefix="/api")
    return app

app = create_app()