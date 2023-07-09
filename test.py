import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import matplotlib.pyplot as plt


def read_qp(image):
    # 預處理圖片
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # 用pytesseract來識別文字
    custom_config = r'--oem 3 --psm 6'
    d = pytesseract.image_to_data(thresh, output_type=Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if '獲得' in d['text'][i]:  # VAI—EXP
            # 如果找到了“QP”，那麼我們假設數字就在它旁邊
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # 將文字周圍的區域切割出來
            cropped = thresh[y:y + h, x + w:x + w + 1000]  # 你可能需要調整這個50
            # 再次使用pytesseract來識別數字
            qp_value = pytesseract.image_to_string(cropped,
                                                   config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            qp_value = qp_value[1:]
            print(qp_value)
            # return qp_value

def count_and_add(template_path='image/material/cristal.png', threshold=0.97):
    """Count the number of times a template appears in a screenshot and add it to the match_counter."""
    # self.fgo_script.dc.take_screenshot()
    match_counter = 0
    main_image = cv2.imread('image/test.png')
    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)

    res = cv2.matchTemplate(main_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # zip the locations and get the unique coordinates (thus getting rid of overlapping locations)
    locations = list(set(list(zip(*loc[::-1]))))
    print(locations)
    # Draw a rectangle around the matched region.
    plt.imshow(main_image)
    for pt in zip(*loc[::-1]):
        print(pt)
        cv2.rectangle(main_image, pt, (pt[0] + 50, pt[1] + 50), (0, 0, 255), 2)
    plt.show()

    # Add the number of matches to the counter
    match_counter += len(locations)
    print(f"Current matches: {match_counter}")
    # self.counter_label.setText(f"Current matches: {self.match_counter}")


# 使用方法：
if __name__ == '__main__':
    # img = cv2.imread('image/screenshot.png')
    # print(read_qp(img))
    count_and_add()