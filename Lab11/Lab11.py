import pandas as pd
import zipfile
import os

# Шлях до ZIP-файлу
zip_file_path = 'C:/Users/Notebook/P_Data_Extract_From_World_Development_Indicators (1).zip'
extracted_folder = 'C:/Users/Notebook/extracted_files'  # Папка для розпакованих файлів

# Розпаковка
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
        print(f"Файли успішно розпаковано у папку: {extracted_folder}")

    # Пошук CSV-файлу в розпакованій папці
    for file_name in os.listdir(extracted_folder):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(extracted_folder, file_name)
            print(f"Знайдено CSV-файл: {csv_file_path}")

            # Зчитування даних
            df = pd.read_csv(csv_file_path)

            # Перетворення DataFrame з широкого формату в довгий
            df_melted = df.melt(id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
                                var_name='Year', value_name='Value')

            # Видалення додаткових символів з колонок 'Year'
            df_melted['Year'] = df_melted['Year'].str.extract('(\d{4})').astype(int)

            # Фільтрація даних для України з 1991 по 2019 роки
            df_ukraine = df_melted[(df_melted['Country Name'] == 'Ukraine') & (df_melted['Year'].between(1991, 2019))]

            # Виведення даних на екран
            print(df_ukraine)

            # Пошук мінімальних і максимальних значень показника
            min_value = df_ukraine['Value'].min()
            max_value = df_ukraine['Value'].max()

            # Створення нового DataFrame для запису результатів
            result_df = pd.DataFrame({
                'Показник': ['Мінімальна тривалість життя', 'Максимальна тривалість життя'],
                'Значення': [min_value, max_value]
            })

            # Збереження результатів у новий CSV файл
            result_df.to_csv('результати_тривалості_життя.csv', index=False)

            print("Результати збережено у файл 'результати_тривалості_життя.csv'.")
            break
    else:
        print("CSV-файл не знайдено у розпакованій папці.")

except FileNotFoundError:
    print("Помилка: ZIP-файл не знайдено.")
except zipfile.BadZipFile:
    print("Помилка: Неможливо розпакувати ZIP-файл.")
except pd.errors.EmptyDataError:
    print("Помилка: Файл порожній.")
except pd.errors.ParserError:
    print("Помилка: Сталася помилка під час розбору файлу.")
except KeyError as e:
    print(f"Помилка: Колонка {e} не знайдена у CSV файлі.")
except Exception as e:
    print(f"Виникла непередбачувана помилка: {e}")


