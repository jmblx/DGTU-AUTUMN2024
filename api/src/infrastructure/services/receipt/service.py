carbon_factors = {
    "Джем вишнёвый дой-пак": {"category": "food", "factor": 0.6},
    "Куриная грудка охлаждённая": {"category": "food", "factor": 5.4},
    "Электро-велосипед": {"category": "electronics", "factor": 96.0},
    "Апельсины": {"category": "food", "factor": 0.3},
    "Хлеб": {"category": "food", "factor": 0.25},
    "Молоко": {"category": "food", "factor": 1.2},
    "Проезд на автобусе": {"category": "transport", "factor": 0.105},  # на км
    "delivery_per_km": {"category": "transport", "factor": 0.2}  # для доставки
}


def calculate_carbon_footprint(purchases, carbon_factors):
    total_carbon_footprint = 0
    category_footprints = {}

    for purchaser in purchases:
        for receipt in purchaser.get("receipts", []):
            for item in receipt["items"]:
                name = item["name"]
                count = item["count"]

                # Получаем коэффициент и категорию для данного товара
                if name in carbon_factors:
                    factor_info = carbon_factors[name]
                    footprint = count * factor_info["factor"]
                    category = factor_info["category"]

                    # Увеличиваем углеродный след для категории
                    if category not in category_footprints:
                        category_footprints[category] = 0
                    category_footprints[category] += footprint

            # Учитываем транспортные расходы на доставку товаров
            distance_km = receipt.get("distance_km", 0)
            if distance_km > 0:
                transport_footprint = distance_km * carbon_factors["delivery_per_km"]["factor"]
                category_footprints["transport"] = category_footprints.get("transport", 0) + transport_footprint

    # Считаем общий углеродный след и процентное распределение по категориям
    total_carbon_footprint = sum(category_footprints.values())
    category_percentages = {k: (v / total_carbon_footprint) * 100 for k, v in category_footprints.items()}

    # Выбираем топ-3 категории и формируем рекомендации
    sorted_categories = sorted(category_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
    recommendations = {
        "food": "Сократите потребление продуктов с высоким углеродным следом, таких как мясо.",
        "electronics": "Учитывайте влияние электроники и оптимизируйте её использование.",
        "transport": "Сократите транспортные расходы или используйте экологически чистый транспорт."
    }

    top3_recommendations = {cat: recommendations[cat] for cat, _ in sorted_categories}

    return {
        "total_carbon_footprint": total_carbon_footprint,
        "category_percentages": category_percentages,
        "top3_recommendations": top3_recommendations
    }

# Пример вызова функции
result = calculate_carbon_footprint(, carbon_factors)
print(result)
