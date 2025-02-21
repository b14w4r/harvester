import random
import pandas as pd
from datetime import datetime

# Генерация одинаковых случайных id для всех файлов
fixed_ids = random.sample(range(50, 150), 5)

for i in range(10):
    # Генерация случайной даты с разными месяцами в 2025 году
    month = random.randint(1, 12)
    date = datetime(2025, month, 20).strftime("%d.%m.%Y")

    # Генерация случайных данных для id и цены
    data = {
        "id": fixed_ids,  # 5 одинаковых случайных id во всех файлах
        "Цена за единицу": [random.randint(50, 1000) for _ in range(5)]
    }
    df = pd.DataFrame(data)

    # Создание нового файла xlsx
    file_name = f"file_{i + 1}.xlsx"
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        # Запись заголовка и даты в первую строку
        df_meta = pd.DataFrame([["Дата актуальности", date]])
        df_meta.to_excel(writer, sheet_name="Sheet1", index=False, header=False, startrow=0)

        # Запись основной таблицы начиная с 2-й строки
        df.to_excel(writer, sheet_name="Sheet1", index=False, startrow=1)

    print(f"Файл {file_name} создан.")
