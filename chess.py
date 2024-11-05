import tkinter as tk
import cv2
from cropper import ImageCropper
from recognition import recognize
from squares import process_image, GetSquares

if __name__ == "__main__":
    # root = tk.Tk()
    # app = ImageCropper(root)
    # root.mainloop()
    # process_image('cropped_image.png', 'output/tiles/')
    # GetSquares(cv2.imread('lined.jpg'))
    recognize()
