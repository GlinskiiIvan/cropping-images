import cv2
import pandas as pd
from PIL import Image
from datetime import datetime
import os

def process_directory(input_dir, output_excel):
    supported_formats = ('.jpg', '.jpeg', '.png')
    data = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as image:
                        # Получаем размеры изображения
                        width, height = image.size
                        data.append({
                            'image': file_path,
                            'height': height,
                            'width': width
                        })
                        print(f'image: {file_path}; height: {height}; width: {width}')
                except Exception as e:
                    print(f"Ошибка при обработке файла {file_path}: {e}")
                    continue

    # Преобразуем данные в DataFrame и сохраняем
    new_df = pd.DataFrame(data)
    if os.path.exists(output_excel):
        print(f'output_excel: {output_excel}')
        existing_df = pd.read_excel(output_excel, engine='openpyxl')
        final_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        final_df = new_df
    final_df.to_excel(output_excel, index=False, engine='openpyxl')
    print(f"Данные сохранены в {output_excel}")

def select_directory():
    main_directory = input("Введите путь к основной директории: ").strip().strip("'\"")
    
    # Проверяем, что путь существует и является директорией
    if not os.path.isdir(main_directory):
        print("Указанный путь не является директорией. Повторите попытку.")
        return select_directory()

    return main_directory

if __name__ == '__main__':
    start_time = datetime.now()
    output_excel = 'sizes.xlsx'

    directory = select_directory()
    process_directory(directory, output_excel)

    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Время выполнения скрипта: {execution_time}")
