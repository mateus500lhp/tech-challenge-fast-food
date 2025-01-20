from fastapi import FastAPI
from app.adapters.driver.controllers.product_controller import router as product_router
from app.adapters.driver.controllers.client_controller import router as client_router
from app.adapters.driver.controllers.order_controller import router as order_router
<<<<<<< HEAD
from app.adapters.driver.controllers.client.client_controller import router as client_router
from app.adapters.driver.controllers.coupon.coupon_controller import router as coupon_router
=======
>>>>>>> origin/feature/criacao-do-pedido

def create_app() -> FastAPI:
    app = FastAPI(title="Fast Food Self-Service")
    app.include_router(client_router, prefix="/api", tags=["clients"])
    app.include_router(product_router, prefix="/api", tags=["products"])
<<<<<<< HEAD
    app.include_router(coupon_router, prefix="/api", tags=["coupons"])
=======
>>>>>>> origin/feature/criacao-do-pedido
    app.include_router(order_router, prefix="/api", tags=["orders"])
    return app

app = create_app()