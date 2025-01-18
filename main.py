from fastapi import FastAPI
# from app.adapters.driver.controllers import products_controller

def create_app() -> FastAPI:
    app = FastAPI(title="Fast Food Self-Service")
    # app.include_router(products_controller.router)
    return app

app = create_app()