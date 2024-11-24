import tkinter as tk
import cv2
from cropper import ImageCropper
from recognition import recognize
from squares import process_image, GetSquares


#pip install -r requirements.txt
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.mainloop()
    #GetSquares(cv2.imread('positions/1b1B1b2-2pK2q1-4p1rB-7k-8-8-3B4-3rb3.jpeg'))
    GetSquares(cv2.imread('cropped_image.png'))
    recognize()
