import logging
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
    FastapiProvider,
    inject,
    setup_dishka,
)
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from sqlalchemy.orm import configure_mappers

from core.di.container import container
from presentation.receipts.router import router as receipt_router
from presentation.registration.router import router as reg_router

# from logstash import TCPLogstashHandler
# from logstash import TCPLogstashHandler
# from starlette_exporter import PrometheusMiddleware, handle_metrics
import core.db.logs  # noqa: F401

from infrastructure.db_models.user.models import User
from infrastructure.db_models.role.models import Role

# Конфигурируем мапперы
configure_mappers()

# from auth.jwt_auth import router as jwt_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()

# Создание экземпляра FastAPI с определенным lifespan
app = FastAPI(lifespan=lifespan, root_path="/api")

# Настройка интеграции Dishka с FastAPI
setup_dishka(container=container, app=app)

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# logstash_handler = TCPLogstashHandler("logstash", 50000)
# logger.addHandler(logstash_handler)


# def get_default_context(request: Request) -> dict:
#     return {
#         "auth_token": request.state.auth_token.replace("Bearer ", ""),
#         "refresh_token": request.state.refresh_token,
#         "fingerprint": request.state.fingerprint,
#         # "nats_client": nats_client,
#     }
# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

app.include_router(receipt_router)
app.include_router(reg_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
