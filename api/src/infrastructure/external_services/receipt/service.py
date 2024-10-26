import os
import httpx
from typing import Optional, List
from fastapi import HTTPException
from dishka import Provider, provide, Scope
from fastapi import Request

from presentation.receipts.schemas import Purchaser, Receipt

class ExternalAPIService:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def get_purchaser(self, email: Optional[str] = None, phone_number: Optional[str] = None) -> Purchaser:
        params = {}
        if email:
            params["email"] = email
        if phone_number:
            params["phone_number"] = phone_number

        response = await self.client.get("/purchasers", params=params)
        if response.status_code == 200:
            data = response.json()
            return Purchaser(**data)
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Покупатель не найден")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    async def grant_access(self, purchaser_id: str) -> None:
        response = await self.client.post(f"/purchasers/{purchaser_id}/grantAccess")
        if response.status_code not in [204, 200]:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    async def confirm_access(self, purchaser_id: str, code: str) -> None:
        response = await self.client.post(f"/purchasers/{purchaser_id}/grantAccess/{code}")
        if response.status_code not in [204, 200]:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    async def get_receipts(self, purchaser_id: str, from_time: str, to_time: str) -> List[Receipt]:
        params = {"from": from_time, "to": to_time}
        response = await self.client.get(f"/purchasers/{purchaser_id}/receipts", params=params)
        if response.status_code == 200:
            data = response.json()
            return [Receipt(**receipt) for receipt in data]
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Чеки не найдены")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    async def close(self):
        await self.client.aclose()

class ExternalAPIProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_external_service(self, request: Request) -> ExternalAPIService:
        # Предполагается, что основной сервис хранит токен аутентификации
        auth_token = os.getenv("RECEIPT_SERVICE_AUTH_TOKEN")  # Ваш токен аутентификации
        if not auth_token:
            raise HTTPException(status_code=500, detail="Токен аутентификации не настроен")

        base_url = os.getenv("RECEIPT_SERVICE_BASE_URL")  # Адрес вашего внешнего приложения
        if not base_url:
            raise HTTPException(status_code=500, detail="Базовый URL внешнего сервиса не настроен")

        return ExternalAPIService(base_url=base_url, auth_token=auth_token)
