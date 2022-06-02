
import cv2
import pytesseract



pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread("img_1.png")

# Only accepts RGB: OpenCV has everything in BGR
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
string = pytesseract.image_to_string(img)

hImg, wImg, _ = img.shape
boxes = pytesseract.image_to_boxes(img)

for b in boxes.splitlines():
    print(b)
    b = b.split(' ')
    print(b)






