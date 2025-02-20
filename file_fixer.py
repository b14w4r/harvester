import pandas as pd

def process_file(file_path):
    # Определяем, xlsx это или csv
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, header=None)
    else:
        df = pd.read_csv(file_path, header=None)

    # Проверяем, что первая ячейка содержит "Дата актуальности"
    if df.iloc[0, 0] != "Дата актуальности:":
        raise ValueError("Файл не содержит 'Дата актуальности' в первой ячейке.")

    # Проверяем, что вторая ячейка содержит дату
    date_value = df.iloc[0, 1]
    try:
        date = pd.to_datetime(date_value, dayfirst=True)  # Парсим дату
    except ValueError:
        raise ValueError("Вторая ячейка не является корректной датой.")

    print(f"Дата актуальности: {date.date()}")

    # Ищем начало таблицы (столбцы id и Цена за единицу)
    start_idx = None
    for i in range(1, len(df)):
        if df.iloc[i, 0] == "id" and df.iloc[i, 1] == "Цена за единицу":
            start_idx = i + 1
            break

    if start_idx is None:
        raise ValueError("Не найдены заголовки 'id' и 'Цена за единицу'.")

    # Читаем таблицу
    table = df.iloc[start_idx:].dropna(how="all")  # Убираем пустые строки
    table.columns = ["product_id", "price"]

    # Приводим id к int, а Цена за единицу к float
    table["product_id"] = table["product_id"].astype(int)
    table["price"] = table["price"].astype(float)
    table["date"] = date

    print("Обработанная таблица:")
    print(table)
    return table
