import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = "C:\\py-libs\\Tesseract-OCR\\Tesseract.exe"

def imgToText(file_path):
        # Abrir a imagem usando OpenCV (cv2.imread) a partir do arquivo salvo
        image = cv2.imread(file_path)

        if image is None:
            return None

        # Aplicar OCR usando pytesseract
        return pytesseract.image_to_string(image, config="--psm 6")