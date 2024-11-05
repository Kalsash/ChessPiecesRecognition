import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2
import os
# Глобальная переменная для хранения текущих координат курсора
current_coordinates = (0, 0)


def Points(x, y, image):
    radius = 10
    h, w, _ = image.shape
    if x < radius or x >= w - radius or y < radius or y >= h - radius:
        print("Координаты вне пределов изображения")
        return
    cv2.circle(image, (x, y), radius, (255, 0, 0), -1)


def grayscale_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur_image(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def detect_edges(image):
    return cv2.Canny(image, 100, 200)


def dilate_image(edges):
    return cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)


def hough_transform(image):
    lines = cv2.HoughLinesP(image, 1, np.pi / 180, threshold=80, minLineLength=100, maxLineGap=10)
    return lines


def calculate_intersections(lines, image_shape):
    if lines is None:
        return []
    points = []
    h, w = image_shape[:2]  # Получаем высоту и ширину изображения
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            line1 = lines[i][0]
            line2 = lines[j][0]
            x1, y1, x2, y2 = line1
            x3, y3, x4, y4 = line2
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom != 0:
                x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
                y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

                # Проверяем, находится ли точка внутри границ изображения
                if 0 <= x < w and 0 <= y < h:
                    points.append((int(x), int(y)))
    return points


def cluster_intersections(points):
    if len(points) < 4:
        print("Недостаточно точек для кластеризации.")
        return []
    points_array = np.array(points)
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(points_array)
    centers = kmeans.cluster_centers_.astype(int)
    return centers


def show_image(title, image):
    plt.figure(title)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()


def process_image(input_image_path, output_dir):
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"Ошибка загрузки изображения: {input_image_path}. Убедитесь, что файл существует.")
        return

    gray = grayscale_image(image)
    blurred = blur_image(gray)
    edges = detect_edges(blurred)
    dilated = dilate_image(edges)

    lines = hough_transform(dilated)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Передаем размеры изображения в calculate_intersections
    intersection_points = calculate_intersections(lines, image.shape)

    if len(intersection_points) == 0:
        print("Пересечения не найдены.")
        return

    clustered_centers = cluster_intersections(intersection_points)
    show_image("Обнаруженные линии", image)
    cv2.imwrite('lined.jpg', image)
    return image





def GetSquares(image):
    output_folder = 'squares'
    os.makedirs(output_folder, exist_ok=True)
    height, width, _ = image.shape
    cell_size = height // 8  # Поскольку у вас 8 клеток по вертикали и горизонтали
    num_cells_x = 8
    num_cells_y = 8
    for i in range(num_cells_y):
        for j in range(num_cells_x):
            x_start = j * cell_size
            y_start = i * cell_size
            cell = image[y_start:y_start + cell_size, x_start:x_start + cell_size]

            cell_file_name = os.path.join(output_folder, f'cell_{i * num_cells_x + j + 1}.jpg')
            cv2.imwrite(cell_file_name, cell)

    print("Клетки успешно сохранены!")