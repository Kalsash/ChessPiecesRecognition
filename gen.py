import os
import shutil
import cv2
import uuid  # Для генерации уникальных имен
from squares import process_image, GetSquares

chess_positions = {
    57: "A1", 49: "A2", 41: "A3", 33: "A4", 25: "A5", 17: "A6", 9: "A7", 1: "A8",
    58: "B1", 50: "B2", 42: "B3", 34: "B4", 26: "B5", 18: "B6", 10: "B7", 2: "B8",
    59: "C1", 51: "C2", 43: "C3", 35: "C4", 27: "C5", 19: "C6", 11: "C7", 3: "C8",
    60: "D1", 52: "D2", 44: "D3", 36: "D4", 28: "D5", 20: "D6", 12: "D7", 4: "D8",
    61: "E1", 53: "E2", 45: "E3", 37: "E4", 29: "E5", 21: "E6", 13: "E7", 5: "E8",
    62: "F1", 54: "F2", 46: "F3", 38: "F4", 30: "F5", 22: "F6", 14: "F7", 6: "F8",
    63: "G1", 55: "G2", 47: "G3", 39: "G4", 31: "G5", 23: "G6", 15: "G7", 7: "G8",
    64: "H1", 56: "H2", 48: "H3", 40: "H4", 32: "H5", 24: "H6", 16: "H7", 8: "H8",
}
def fen_to_pieces(fen):
    # Словарь для символов фигур
    piece_dict = {
        'K': 'White King',
        'Q': 'White Queen',
        'R': 'White Rook',
        'B': 'White Bishop',
        'N': 'White Knight',
        'P': 'White Pawn',
        'k': 'Black King',
        'q': 'Black Queen',
        'r': 'Black Rook',
        'b': 'Black Bishop',
        'n': 'Black Knight',
        'p': 'Black Pawn',
    }

    # Разбиваем FEN на части
    fen_parts = fen.split(' ')[0]  # Берем только первую часть, отвечающую за фигуры
    rows = fen_parts.split('/')  # Разделяем строки на ряд

    # Создаем словарь для позиций
    board = {pos: "empty" for pos in chess_positions.values()}

    for row_index, row in enumerate(rows):
        column_index = 0
        for char in row:
            if char.isdigit():
                column_index += int(char)  # Пропускаем числа, увеличивая колонку на соответствующее количество
            else:
                # Преобразуем в шахматные координаты
                rank = 8 - row_index  # Ранг (ряд) от 1 до 8
                file = chr(column_index + ord('a')).upper()  # Файл (колонка) от 'a' до 'h'
                position = f"{file}{rank}"  # Формирование строки позиции, например, A5, G4

                # Заполняем информацию о фигуре на позиции
                board[position] = piece_dict.get(char, f'Unknown piece: {char}')
                column_index += 1

    return board

def move(fen):
    pieces = fen_to_pieces(fen)
    photos = {}
    for i in range(1, 65):
        position = chess_positions[i]
        photos[i] = pieces[position]

    # Исходные данные
    images_folder = 'squares'  # Папка с изображениями

    # Перемещение изображений в соответствующие папки
    empty_counter = 0  # Счетчик для папки empty

    for i in range(1, 65):
        image_name = f'cell_{i}.jpg'
        image_path = os.path.join(images_folder, image_name)

        if os.path.exists(image_path):
            destination_folder = photos.get(i, 'empty')  # Используем i как ключ для словаря photos
            destination_path = os.path.join('data', destination_folder)

            # Проверяем, существует ли папка, и создаем ее, если не существует
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)  # Создаем папку
                print(f'Папка создана: {destination_path}')

            # Если папка пустая и мы уже переместили 5 изображений, пропускаем
            if destination_folder == 'empty':
                if empty_counter >= 1:
                    continue  # Пропускаем перемещение в 'empty'
                empty_counter += 1

            # Генерируем новое случайное имя файла
            new_file_name = str(uuid.uuid4()) + '.jpg'  # Генерируем уникальное имя

            # Перемещение изображения
            shutil.move(image_path, os.path.join(destination_path, new_file_name))

    print('Все изображения перемещены!')




import os

# Путь к вашей папке
folder_path = 'positions'

# Перебираем файлы в папке
for filename in os.listdir(folder_path):
    if filename.endswith('.jpeg'):
        GetSquares(cv2.imread(f'positions/{filename}'))
        s = os.path.splitext(filename)[0]
        s = s.replace("-", "/")
        move(s)






