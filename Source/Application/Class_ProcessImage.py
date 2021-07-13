import cv2 as cv
import imutils
from Function import CheckSeparated, AdjustImage

class ProcessImage():

    def __init__(self, param, mode = 1):
        if mode == 1:
            self.image = param
        elif mode == 2:
            self.image = cv.imread(param)
        
    def find_digits(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
        edged = cv.Canny(blurred, 50, 200, 255)
        cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
						cv.CHAIN_APPROX_SIMPLE)
        #Chuyển định dạng cnts
        cnts = imutils.grab_contours(cnts)
        self.list_info = [] # Danh sách thông tin của các con số trong ảnh gốc, mỗi phần tử là một list [x, y, w, h]
        self.list_digits = [] # Danh sách ảnh được cắt ra

        # Vòng lặp qua các phần tử được xác định trong ảnh gốc
        for c in cnts:
            # Tạo hình chữ nhật bao quanh các vùng ảnh được vẽ
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(self.image, (x, y), (x + w+1, y + h+1), (0, 255, 0), 3)

            # Với mỗi ảnh xét xem liệu nó có phân biệt với các ảnh đã cắt hay không
            i = 0
            while i < len(self.list_digits):
                if CheckSeparated(self.list_info[i][0], self.list_info[i][1], self.list_info[i][2], self.list_info[i][3], x, y, w, h) == False:
                    # Nếu nó trùng với một ảnh nào đã cắt nhưng kích thước lớn hơn thì sẽ quan trọng hơn, dùng nó thay thế ảnh cũ
                    if w*h > self.list_info[i][2] * self.list_info[i][3]:
                        split_img = AdjustImage(self.image, x, y, w, h)
                        self.list_digits[i] = split_img
                        self.list_info[i] = [x, y, w, h]
                    break
                i += 1
            
            # Nếu phân biệt thì thêm nó như một ảnh mới vào danh sách
            if i == len(self.list_digits):
                split_img = AdjustImage(self.image, x, y, w, h)
                self.list_digits.append(split_img)
                self.list_info.append([x, y, w, h])