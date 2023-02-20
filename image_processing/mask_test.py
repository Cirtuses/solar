import numpy as np
import cv2

print('1')
# image = cv2.imread("../1.jpg")
image = cv2.imread("LR.jpg")
# cv2.imshow("Mask Applied to Image", image)
print(image)

circle = np.zeros(image.shape[0:2], dtype="uint8")
cv2.circle(circle, (image.shape[1] // 2, image.shape[0] // 2), 600, 255, -1)

masked = cv2.bitwise_and(image, image, mask=circle)
cv2.imshow("Mask Applied to Image", masked)
cv2.waitKey(0)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# img_gray = cv2.cvtColor(image)

gray_img_eq = cv2.equalizeHist(gray_image)

# hist_eq = cv2.calcHist([gray_img_eq], [0], None, [256], [0, 256])
# cv2.imshow("EQU", gray_img_eq)
#
# k = cv2.waitKey(0)
# if k == 27:  # wait for ESC key to exit
#     cv2.destroyAllWindows()


methods = [
    ("THRESH_BINARY", cv2.THRESH_BINARY),
    ("THRESH_BINARY_INV", cv2.THRESH_BINARY_INV),
    ("THRESH_TRUNC", cv2.THRESH_TRUNC),
    ("THRESH_TOZERO", cv2.THRESH_TOZERO),
    ("THRESH_TOZERO_INV", cv2.THRESH_TOZERO_INV)]
# 遍历阈值方法
for (threshName, threshMethod) in methods:
    #  将255（白色）作为阈值测试时的值作为第三个参数
    # (T, thresh) = cv2.threshold(gray_image, 122, 255, threshMethod)
    (T, thresh) = cv2.threshold(gray_image, 145, 255, threshMethod)
    cv2.imshow(threshName, thresh)
    cv2.waitKey(0)

(T, mask_image) = cv2.threshold(gray_image, 145, 255, cv2.THRESH_BINARY)
cv2.imshow("ans", mask_image)
cv2.imwrite("ans.jpg", mask_image)
cv2.waitKey(0)
# bitwiseAnd = cv2.bitwise_and(image, mask_image)
# cv2.imshow("ans", bitwiseAnd)
masked = cv2.bitwise_and(image, image, mask=mask_image)
cv2.imshow("ans", masked)
cv2.imwrite("masked.jpg", masked)
cv2.waitKey(0)
