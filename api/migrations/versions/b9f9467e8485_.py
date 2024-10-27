"""empty message

Revision ID: b9f9467e8485
Revises: 4cebeea6f9ff
Create Date: 2024-10-27 05:15:25.221094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9f9467e8485'
down_revision: Union[str, None] = '4cebeea6f9ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    ACHIEVEMENT_REWARDS = [
        {"achievement_id": 1, "reward_id": 2, "amount": 30},  # Эко-Исследователь – XP
        {"achievement_id": 2, "reward_id": 1, "amount": 10},  # Батарейный Герой – листья
        {"achievement_id": 3, "reward_id": 1, "amount": 20},  # Пластиковый Спасатель – листья
        {"achievement_id": 4, "reward_id": 2, "amount": 50},  # Мастер Сортировки – XP
        {"achievement_id": 5, "reward_id": 1, "amount": 30},  # Защитник Берега – листья
        {"achievement_id": 6, "reward_id": 5, "amount": 1},  # Экологический Патруль – худи
        {"achievement_id": 7, "reward_id": 2, "amount": 70},  # Эко-Чемпион – XP
        {"achievement_id": 8, "reward_id": 4, "amount": 1},  # Эко-Транспорт – футболка
        {"achievement_id": 9, "reward_id": 1, "amount": 15},  # Эко-Питание – листья
        {"achievement_id": 10, "reward_id": 6, "amount": 1}  # Чистота без вреда – билет
    ]
    ACHIEVEMENTS = [
        {
            "id": 1,
            "title": "Эко-Исследователь",
            "description": "Посетите 3 семинара и правильно ответьте на все вопросы.",
            "file_path": "http://90.156.170.155:9001/achievements/eco-researcher.png",
            "goal": 3.0
        },
        {
            "id": 2,
            "title": "Батарейный Герой",
            "description": "Сдайте 10 батареек в пункт приема для улучшения экологической обстановки.",
            "file_path": "http://90.156.170.155:9001/achievements/battery-hero.png",
            "goal": 10.0
        },
        {
            "id": 3,
            "title": "Пластиковый Спасатель",
            "description": "Сдайте 20 пластиковых бутылок для переработки.",
            "file_path": "http://90.156.170.155:9001/achievements/plastic-savior.png",
            "goal": 20.0
        },
        {
            "id": 4,
            "title": "Мастер Сортировки",
            "description": "Отсортируйте 5 кг мусора в специализированных контейнерах.",
            "file_path": "http://90.156.170.155:9001/achievements/sorting-master.png",
            "goal": 5.0
        },
        {
            "id": 5,
            "title": "Защитник Берега",
            "description": "Очистите не менее 10 кв. м берега от отходов.",
            "file_path": "http://90.156.170.155:9001/achievements/beach-guardian.png",
            "goal": 10.0
        },
        {
            "id": 6,
            "title": "Экологический Патруль",
            "description": "Выполните все пять видов заданий хотя бы по одному разу.",
            "file_path": "http://90.156.170.155:9001/achievements/ecological-patrol.png",
            "goal": 5.0  # 5 типов задач
        },
        {
            "id": 7,
            "title": "Эко-Чемпион",
            "description": "Завершите 10 заданий любого типа, внося вклад в защиту окружающей среды.",
            "file_path": "http://90.156.170.155:9001/achievements/eco-champion.png",
            "goal": 10.0
        },
        {
            "id": 8,
            "title": "Эко-Транспорт",
            "description": "Купите не менее 3 единиц экологичного транспорта (велосипед, электросамокат и т.п.).",
            "file_path": "http://90.156.170.155:9001/achievements/eco-transport.png",
            "goal": 3.0
        },
        {
            "id": 9,
            "title": "Эко-Питание",
            "description": "Приобретите 5 продуктов с маркировкой 'органическое' или 'с минимальным углеродным следом'.",
            "file_path": "http://90.156.170.155:9001/achievements/eco-food.png",
            "goal": 5.0
        },
        {
            "id": 10,
            "title": "Чистота без вреда",
            "description": "Купите 3 продукта для гигиены с экологичной упаковкой или минимальным углеродным следом.",
            "file_path": "http://90.156.170.155:9001/achievements/clean-without-harm.png",
            "goal": 3.0
        }
    ]
    op.bulk_insert(
        sa.table(
            'achievement',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('title', sa.String, nullable=False),
            sa.Column('description', sa.String, nullable=False),
            sa.Column('file_path', sa.String, nullable=True),
            sa.Column('goal', sa.Float, nullable=True)
        ),
        ACHIEVEMENTS
    )

    # Вставляем связи между достижениями и наградами
    op.bulk_insert(
        sa.table(
            'reward_achievement',  # Убедитесь, что имя таблицы соответствует вашей схеме
            sa.Column('achievement_id', sa.Integer, nullable=False),
            sa.Column('reward_id', sa.Integer, nullable=False),
            sa.Column('amount', sa.Integer, nullable=False)
        ),
        ACHIEVEMENT_REWARDS
    )


def downgrade() -> None:
    op.execute('DELETE FROM reward_achievement')
    op.execute('DELETE FROM achievement')
