import cv2
from numpy import ndarray, asarray, ones, uint8
import pytesseract
import asyncio

def resize_img(img_array: ndarray):
    return cv2.resize(img_array, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)


def convert_to_grayscale(img_array):
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    return img


def denoise_img(img_array):
    kernel = ones((1, 1), uint8)
    img = cv2.dilate(img_array, kernel, iterations=1)
    img = cv2.erode(img_array, kernel, iterations=1)

    return img


def blur_img(img_array):
    bg = cv2.threshold(
        cv2.medianBlur(img_array, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    img = 255 - cv2.absdiff(img_array, bg)

    return img

def apply_image_processing(image: ndarray):
    # Image processing for better OCR results

    # 1. Resize the image
    proccessed_image = resize_img(image)

    # 2. Convert the image to grayscale
    proccessed_image = convert_to_grayscale(proccessed_image)

    # 3. Denoise the image
    proccessed_image = denoise_img(proccessed_image)

    # 4. Blur the image
    # proccessed_image = blur_img(proccessed_image)

    try:
        pred: str = pytesseract.image_to_string(proccessed_image)
        return pred
    except Exception as e:
        return "Error: " + str(e)