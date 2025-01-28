import os
import math
import cv2
from PIL import Image
from datetime import datetime
from multiprocessing import Pool, cpu_count
from typing import List

def select_directory():
    main_directory = input("Введите путь к основной директории: ").strip().strip("'\"")
   
    # Проверяем, что путь существует и является директорией
    if not os.path.isdir(main_directory):
        print("Указанный путь не является директорией. Повторите попытку.")
        return select_directory()
    
    return main_directory

def select_images(main_directory):
    supported_formats = ('.jpg', '.jpeg', '.png')
    data = []
    for root, _, files in os.walk(main_directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_path = os.path.join(root, file)
                data.append(image_path)
    return data

def chunk_images(images, num_chunks):
    chunk_size = math.ceil(len(images) / num_chunks)
    return [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

def get_crop_box(image_path: str, ksx: int, ksy: int, kx: int, ky: int):
    image = Image.open(image_path)
    
    origin_width, origin_height = image.size
    # print('origin_width, origin_height', origin_width, origin_height)
    
    window_width = round((origin_width * ksx) / 100)
    window_height = round((origin_height * ksy) / 100)
    # print('window_width, window_height', window_width, window_height)

    left = round((origin_width * kx) / 100)
    up = round((origin_height * ky) / 100)
    right = left + window_width
    down = up + window_height

    if(right > origin_width):
        left = origin_width - window_width
        right = left + window_width

    if(down > origin_height):
        up = origin_height - window_height
        down = up + window_height

    # print('crop_box', (left, up, right, down))
    return (left, up, right, down)


def cropping_image(image_path: str, output_path: str):
    # x, y, w, h = 384, 384, 640, 640 # 1024 x, y, x+w, y+h
    try:
        print(f"Обрабатывается изображение {image_path}")

        image = Image.open(image_path)
        crop_box = get_crop_box(image_path, 50, 50, 25, 25)

        image_crop = image.crop(crop_box)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Создаем директорию, если её нет
        image_crop.save(output_path)
    except Exception as e:
        print(f"Ошибка обработки {image_path}: {e}")

def process_images(chunk: List[str], input_dir: str, output_dir: str):
    for image_path in chunk:
        relative_path = os.path.relpath(image_path, input_dir)
        output_path = os.path.join(output_dir, relative_path)
        cropping_image(image_path, output_path)

if __name__ == '__main__':
    start_time = datetime.now()

###################################################################
    # main_directory = select_directory()
    # print(main_directory)

    # files = select_images(main_directory)
    # print('data', len(files))

    # chunks = chunk_images(files, 12)
    # print('chunks', len(chunks[10]))

    # cropping_image('test-1024.png')
###################################################################
    # input_dir = select_directory()
    # output_dir = 'cropped-images/'
    # crop_box = (0,0,100,100)
    # process_images(input_dir, output_dir, crop_box)
###################################################################
    num_processes = cpu_count()
    input_dir = select_directory()
    output_dir = 'cropped-images/'
    images = select_images(input_dir)
    image_chunks = chunk_images(images, num_processes)

    try:
        with Pool(processes=num_processes) as pool:
            pool.starmap(
                process_images,
                [(chunk, input_dir, output_dir) for chunk in image_chunks]
            )
    except Exception as e:
        print(f"Ошибка в основном процессе: {e}")

    # crop_box_test = get_crop_box("C:\\Users\\brodyga\\Downloads\\Здоровые-нездоровые мениски\\PD\\Sagittal\\1\\Сингербаева-5-IMG-0005-00007.png", 50, 50, 25, 25)


    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Время выполнения скрипта: {execution_time}")
    print(f'Количество задействованных процессов: {num_processes}')