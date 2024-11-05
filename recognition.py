import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os
import cv2
SIZE = 80
# Загрузить модель
model = tf.keras.models.load_model('chess_piece_recognition_model.h5')


# Функция для предобработки изображения
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(SIZE, SIZE))  # Приведение к размеру 50x50
    img_array = image.img_to_array(img) / 255.0  # Нормализация
    img_array = np.expand_dims(img_array, axis=0)  # Добавление размерности для батча
    return img_array


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


def determine_piece_color(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Не удалось загрузить изображение по пути: {image_path}")

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width, _ = image.shape
    center_pixel = hsv_image[height // 2, width // 2]

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])

    if (lower_white <= center_pixel).all() and (center_pixel <= upper_white).all():
        return "White"
    elif (lower_black <= center_pixel).all() and (center_pixel <= upper_black).all():
        return "Black"
    else:
        return "Unknown"

def recognize():
    # Путь к папке с изображениями
    folder_path = 'squares'  # Замените на ваш путь к папке

    # Декодирование метки
    label_map = {idx: label for idx, label in enumerate(['bishop', 'empty', 'king', 'night', 'pawn', 'queen', 'rook'])}

    arr = []
    # Обработка всех изображений в папке
    for i in range(1, 65):
        image_name = f'cell_{i}.jpg'
        image_path = os.path.join(folder_path, image_name)

        if os.path.exists(image_path):
            processed_image = preprocess_image(image_path)
            predictions = model.predict(processed_image)
            predictions[0][1] *= 1000
            predicted_class = np.argmax(predictions[0])
            predicted_label = label_map[predicted_class]

            square_color = determine_piece_color(image_path)  # Передаем полный путь

            print(f"{chess_positions[i]}:{predicted_label}:{square_color}")
            arr.append(f"{chess_positions[i]}:{predicted_label}:{square_color}")
        else:
            print(f"{image_name} не найден.")

    import webbrowser

    positions = arr

    board = [['.' for _ in range(8)] for _ in range(8)]

    for position in positions:
        square, piece_type, color = position.split(':')
        x = ord(square[0]) - ord('A')
        y = 8 - int(square[1])
        if 'empty' in piece_type:
            board[y][x] = '.'
        else:
            if color == 'White':
                piece = piece_type[0].upper()
            else:
                piece = piece_type[0].lower()
            board[y][x] = piece

    # Преобразуем доску в FEN
    fen_parts = []
    for row in board:
        empty_count = 0
        row_str = ''
        for square in row:
            if square == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    row_str += str(empty_count)
                    empty_count = 0
                row_str += square
        if empty_count > 0:
            row_str += str(empty_count)
        fen_parts.append(row_str)

    fen_position = '/'.join(fen_parts) + ' w - - 0 1'
    url = f'https://lichess.org/editor/{fen_position}'
    webbrowser.open(url)