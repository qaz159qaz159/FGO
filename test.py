import cv2
import pytesseract
from pytesseract import Output

def read_qp(image):
    # 預處理圖片
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # 用pytesseract來識別文字
    custom_config = r'--oem 3 --psm 6'
    d = pytesseract.image_to_data(thresh, output_type=Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if '獲得' in d['text'][i]: # VAI—EXP
            # 如果找到了“QP”，那麼我們假設數字就在它旁邊
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # 將文字周圍的區域切割出來
            cropped = thresh[y:y+h, x+w:x+w+1000]  # 你可能需要調整這個50
            # 再次使用pytesseract來識別數字
            qp_value = pytesseract.image_to_string(cropped, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            qp_value = qp_value[1:]
            print(qp_value)
            # return qp_value

# 使用方法：
if __name__ == '__main__':
    img = cv2.imread('image/screenshot.png')
    print(read_qp(img))
