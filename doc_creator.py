import random
import pandas as pd
from datetime import datetime

k = 5
# Генерация одинаковых случайных id для всех файлов
fixed_ids = random.sample(range(50, 150), k)

for i in range(3):
    # Генерация случайной даты с разными месяцами в 2025 году
    month = (11+i)%12# random.randint(1, 12)
    if month == 0:
        month = 12
    date = datetime(2024, month, 20).strftime("%d.%m.%Y")

    # Генерация случайных данных для id и цены
    data = {
        "id": fixed_ids,  # 5 одинаковых случайных id во всех файлах
        "Цена за единицу": [random.randint(50, 1000) for _ in range(k)]
    }
    df = pd.DataFrame(data)

    # Определение, добавлять ли строку с валютой (примерно в 50% случаев)
    add_currency = random.choice([True, False])
    currency = random.choice(["RUB", "EUR", "USD"])

    # Создание нового файла xlsx
    file_name = f"file_{i + 1}.xlsx"
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        # Запись заголовка и даты в первую строку
        df_meta = pd.DataFrame([["Дата актуальности", date]])
        df_meta.to_excel(writer, sheet_name="Sheet1", index=False, header=False, startrow=0)

        start_row = 1
        if add_currency:
            # Добавление строки с валютой
            df_currency = pd.DataFrame([["Валюта", currency]])
            df_currency.to_excel(writer, sheet_name="Sheet1", index=False, header=False, startrow=1)
            start_row = 2

        # Запись основной таблицы начиная с нужной строки
        df.to_excel(writer, sheet_name="Sheet1", index=False, startrow=start_row)

    print(f"Файл {file_name} создан.")
