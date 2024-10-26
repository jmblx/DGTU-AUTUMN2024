import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path, Query, BackgroundTasks
from pydantic import BaseModel, EmailStr
import json
from typing import Optional

from starlette.responses import Response

from models import Purchaser, Receipt, ReceiptItem
from fastapi.responses import JSONResponse
import smtplib
import os
from email.message import EmailMessage
import random
import string
import time

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


app = FastAPI(title="Зелёный Ростов - API", version="1.0.0", root_path="/receipt")

DATA_FILE = "data.json"

load_dotenv()

# Загружаем данные из JSON
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# Сохраняем данные в JSON
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Функция для генерации случайного кода подтверждения
def generate_confirmation_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

# Функция для отправки email через SMTP
def send_confirmation_email(email: str, code: str):
    print(f"Отправляем код подтверждения на {email}")
    smtp_user = os.getenv("SMTP_USER")  # Ваш Gmail адрес
    smtp_password = os.getenv("SMTP_PASSWORD")  # Ваш пароль или App Password
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))  # По умолчанию 587 для TLS

    if not smtp_user or not smtp_password:
        print("SMTP_USER и SMTP_PASSWORD должны быть установлены в переменных окружения.")
        print(smtp_user, )
        return

    msg = EmailMessage()
    msg['Subject'] = 'Код подтверждения для доступа к чекам'
    msg['From'] = smtp_user
    msg['To'] = email
    msg.set_content(f'Ваш код подтверждения: {code}')

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        print(f"Код подтверждения отправлен на {email}")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

# Эндпоинт для получения покупателя
@app.get("/purchasers")
def get_purchaser(
        email: Optional[str] = Query(None),
        phone_number: Optional[str] = Query(None)
):
    data = load_data()
    for purchaser in data["purchasers"]:
        logging.info("жаба: %s, %s", purchaser.get("email"), email)

        if purchaser.get("email") == email or purchaser.get("phone_number") == phone_number:
            return {"id": purchaser["id"], "access": purchaser["access"]}
    raise HTTPException(status_code=404, detail="Покупатель не найден")


@app.post("/purchasers/{purchaser_id}/grantAccess")
def grant_access(
        background_tasks: BackgroundTasks,
        purchaser_id: str = Path(...)
):
    data = load_data()
    purchaser = next((p for p in data["purchasers"] if p["id"] == purchaser_id), None)
    if purchaser is None:
        raise HTTPException(status_code=404, detail="Покупатель не найден")

    if not purchaser.get("email"):
        raise HTTPException(status_code=400, detail="У покупателя отсутствует email для отправки кода")

    # Генерация кода подтверждения
    code = generate_confirmation_code()
    purchaser["confirmation_code"] = code
    purchaser["code_expiry"] = int(time.time()) + 600  # Код действителен 10 минут

    save_data(data)

    # Добавление задачи отправки email в фоновый режим
    background_tasks.add_task(send_confirmation_email, purchaser["email"], code)

    return Response(status_code=204)

# Эндпоинт для подтверждения кода доступа
@app.post("/purchasers/{purchaser_id}/grantAccess/{code}")
def confirm_access(
        purchaser_id: str = Path(...),
        code: str = Path(...)
):
    data = load_data()
    purchaser = next((p for p in data["purchasers"] if p["id"] == purchaser_id), None)
    if purchaser is None:
        raise HTTPException(status_code=404, detail="Покупатель не найден")

    stored_code = purchaser.get("confirmation_code")
    code_expiry = purchaser.get("code_expiry")

    current_time = int(time.time())

    if stored_code is None or code_expiry is None:
        raise HTTPException(status_code=400, detail="Код подтверждения не был запрошен")

    if current_time > code_expiry:
        raise HTTPException(status_code=403, detail="Срок действия кода подтверждения истёк")

    if code != stored_code:
        raise HTTPException(status_code=403, detail="Неверный код подтверждения")

    return Response(status_code=204)


@app.get("/purchasers/{purchaser_id}/receipts")
def get_receipts(
        purchaser_id: str,
        from_time: str = Query(..., alias="from"),
        to_time: str = Query(..., alias="to")
):
    data = load_data()
    purchaser = next((p for p in data["purchasers"] if p["id"] == purchaser_id), None)
    if purchaser is None:
        raise HTTPException(status_code=404, detail="Покупатель не найден")

    receipts = [
        receipt for receipt in purchaser["receipts"]
        if from_time <= receipt["time"] <= to_time
    ]
    if not receipts:
        raise HTTPException(status_code=404, detail="Чеки не найдены")
    return receipts
