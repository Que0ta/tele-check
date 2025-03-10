import requests

# Отримання випадкових фактів про котів
def get_cat_facts():
    # static_facts = [
    #     "Коти можуть мати до 100 різних звуків.",
    #     "Деякі коти люблять воду і можуть плавати.",
    #     "Серце кота б'ється в два рази швидше, ніж у людини.",
    #     "Коти мають чудову здатність бачити в темряві.",
    # ]

    try:
        response = requests.get('https://meowfacts.herokuapp.com/', timeout=5)
        response.raise_for_status()
        facts_data = response.json()
        api_facts = facts_data.get("data", [])

        # return static_facts + api_facts
        return api_facts

    except requests.exceptions.RequestException as e:
        print(f"Помилка отримання фактів: {e}")
        # return static_facts

# Отримання інформації про породи котів
def get_cat_breeds():
    api_url = "https://api.thecatapi.com/v1/breeds"

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        breeds_data = response.json()

        return [f"{breed['name']}: {breed['temperament']}" for breed in breeds_data]

    except requests.exceptions.RequestException as e:
        print(f"Помилка отримання порід: {e}")
        return [
            "Сіамська: Дуже активні і цікаві.",
            "Перська: Спокійні і доброзичливі.",
            "Мейн-кун: Великі і добрі.",
            "Шотландська висловуха: З м'яким характером.",
        ]

# Отримання рекомендацій щодо харчування
# def get_food_recommendations():
#     return [
#         "Не давайте коту шоколад, він отруйний для них.",
#         "Корисні продукти: курка, яловичина, морепродукти.",
#         "Уникайте годування кота молоком.",
#         "Ідеальний корм для кота — це той, що відповідає його віку та здоров'ю.",
#     ]
