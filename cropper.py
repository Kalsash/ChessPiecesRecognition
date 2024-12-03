import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.cropped_image = None  # Хранит обрезанное изображение

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.image = None
        self.image_id = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 400), Image.LANCZOS)  # Уменьшаем изображение
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.delete(self.rect)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        end_x = event.x
        end_y = event.y

        left = min(self.start_x, end_x)
        right = max(self.start_x, end_x)
        top = min(self.start_y, end_y)
        bottom = max(self.start_y, end_y)

        self.cropped_image = self.image.crop((left, top, right, bottom))

        # Обновление изображения на canvas
        self.photo = ImageTk.PhotoImage(self.cropped_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def save_image(self):
        if not self.cropped_image:
            self.cropped_image = self.image
        file_path = os.path.join(os.getcwd(), "cropped_image.png")
        self.cropped_image.save(file_path)
        print(f"Image saved as '{file_path}'")
