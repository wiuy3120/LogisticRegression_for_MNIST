import cv2 as cv
import numpy as np

# Hàm kiểm tra xem liệu 2 vùng ảnh là trùng nhau hay tách biệt
def CheckSeparated(x1, y1, w1, h1, x2, y2, w2, h2):
	check = False
	if ((x1>x2+3) and (x1>x2+w2+3)) or ((x2>x1+3) and (x2>x1+w1+3)) or ((y1>y2+3) and (y1>y2+h2+3)) or ((y2>y1+3) and (y2>y1+h1+3)):
		check = True
	return check

# Hàm để cắt ảnh và cân chỉnh lại ảnh phù hợp với kích thước để dự đoán
def AdjustImage(img, x, y, w, h):
	# Xét các trường hợp để lấy thêm ô trống bao quanh chữ số, tạo điều kiện cho việc làm đậm nét
	extra_width = min(x, 599-(x+w-1))
	extra_height = min(y, 599-(y+h-1))

	if extra_width >= 5:
		x -= 5
		w += 10
	else:
		x -= extra_width
		w += 2*extra_width

	if extra_height >= 5:
		y -= 5
		h += 10
	else:
		y -= extra_height
		h += 2*extra_height
		
	# Tiến hành cắt khung chứa số
	split_img = []
	for row in range(y, y+h):
		for col in range(x, x+w):
			split_img.append(img[row][col])

	# Cân chỉnh lại khung ảnh và đổi màu phù hợp với dữ liệu đưa vào mô hình
	split_img = np.array(split_img)
	bgrImage = cv.cvtColor(split_img, cv.COLOR_RGB2BGR)
	grayImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2GRAY)
	#Chuyển background
	grayImage = 255 - grayImage[:,1]
	grayImage = grayImage.reshape((h,w))

	# Làm đậm nét chữ số bằng kernel
	kernel = np.ones((10,10),np.uint8)
	new_img = cv.dilate(grayImage,kernel,iterations = 1)
	# cv.imshow("Test", new_img)
	# cv.waitKey(10000)
	# cv.destroyAllWindows()
	# Nén lại kích thước (28, 28) rồi trải ra thành array (784,) phù hợp với dữ liệu đưa vào mô hình
	new_img = cv.resize(new_img, dsize=(28, 28), interpolation=cv.INTER_AREA)
	new_img = new_img.reshape(784)

	return new_img