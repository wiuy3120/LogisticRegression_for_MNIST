'''
Thông tin nhóm
- Nguyễn Huy Hải – 18120023
- Phạm Công Minh – 18120058
- Nguyễn Thanh Tùng – 18120104
- Nguyễn Thị Hồng Nhung – 18120498
'''

from Class_Paint import Paint
from Class_ProcessImage import ProcessImage
from Image_Filter import Image_Filter
import os
if __name__ == '__main__':
    # img_process = ProcessImage("predict.jpg", mode=2)
    # img_process.find_digits()
    # 
    # print(len(img_process.list_digits))
    dir = __file__[:-7]
    os.chdir(dir)
    Paint()