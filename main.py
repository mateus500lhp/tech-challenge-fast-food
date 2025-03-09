from fastapi import FastAPI
from app.adapters.controllers.product_controller import router as product_router
from app.adapters.controllers.client_controller import router as client_router
from app.adapters.controllers.coupon_controller import router as coupon_router
from app.adapters.controllers.order_controller import router as order_router
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()


def create_app() -> FastAPI:
    app = FastAPI(title="Fast Food Self-Service")
    app.include_router(client_router, prefix="/api", tags=["clients"])
    app.include_router(product_router, prefix="/api", tags=["products"])
    app.include_router(coupon_router, prefix="/api", tags=["coupons"])
    app.include_router(order_router, prefix="/api", tags=["orders"])
    return app

app = create_app()