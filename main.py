from fastapi import FastAPI
from app.adapters.controllers.product_controller import router as product_router
from app.adapters.controllers.client_controller import router as client_router
from app.adapters.controllers.coupon_controller import router as coupon_router
from app.adapters.controllers.order_controller import router as order_router
from app.adapters.controllers.auth_proxy_controller import router as auth_proxy_router
from app.adapters.controllers.payment_webhook_controller import router as payment_router
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()


def create_app() -> FastAPI:
    app = FastAPI(title="Fast Food Self-Service")
    app.include_router(client_router, prefix="/api", tags=["clients"])
    app.include_router(product_router, prefix="/api", tags=["products"])
    app.include_router(coupon_router, prefix="/api", tags=["coupons"])
    app.include_router(order_router, prefix="/api", tags=["orders"])
    app.include_router(payment_router, prefix="/api", tags=["payment_webhook"])
    app.include_router(auth_proxy_router, prefix="/api", tags=["auth_proxy"])
    return app

app = create_app()