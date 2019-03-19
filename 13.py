#https://cloud.tencent.com/developer/article/1052878
import cv2
import numpy as np

#转换灰度
def get_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, gray

# 并去噪声 , 去噪很多种方法，均值滤波器、高斯滤波器、中值滤波器、双边滤波器等。这里取高斯是因为高斯去噪效果是最好的
def Gaussian_Blur(gray):
    blurred = cv2.GaussianBlur(gray, (9, 9), 0) #高斯滤波
    return blurred


# 提取图像的梯度
'''
用Sobel算子计算x，y方向上的梯度，之后在x方向上 minus y方向上的梯度。
通过这个操作，会留下具有高水平梯度和低垂直梯度的图像区域。
'''
def Sobel_gradient(blurred):
    gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    return gradX, gradY, gradient

# 继续去噪声
'''
考虑到图像的孔隙 首先使用低通滤泼器平滑图像, 这将有助于平滑图像中的高频噪声。 低通滤波器的目标是降低图像的变化率。 
如将每个像素替换为该像素周围像素的均值， 这样就可以平滑并替代那些强度变化明显的区域。
对模糊图像二值化，顾名思义，就是把图像数值以某一边界分成两种数值
'''
def Thresh_and_blur(gradient):
    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    return thresh

'''
上个函数得到：其实就算手动分割我们也是需要找到一个边界吧，可以看到轮廓出来了，但是我们最终要的是整个轮廓，所以内部小区域就不要了
'''
def image_morphology(thresh):
    #图像形态学。以下两行：在这里我们选取ELLIPSE核，采用CLOSE操作
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    #细节刻画。以下两行：从上图我们可以发现和原图对比，发现有细节丢失，这会干扰之后的轮廓的检测，要把它们扩充，分别执行4次形态学腐蚀与膨胀
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    return closed

def findcnts_and_box_point(closed):
    (_, cnts, _) = cv2.findContours(closed.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    return box

#找出区域的轮廓
def drawcnts_and_cut(original_img, box):
    # 此时用cv2.findContours()函数。 第一个参数是要检索的图片，必须是为二值图，即黑白的（不是灰度图）
    # draw a bounding box arounded the detected barcode and display the image
    draw_img = cv2.drawContours(original_img.copy(), [box], -1, (0, 0, 255), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    crop_img = original_img[y1:y1 + hight, x1:x1 + width]
    return draw_img, crop_img

#画出轮廓
#找到轮廓了，接下来，要画出来的，即用cv2.drawContours()函数
def walk():
    img_path = r'1.jpg'
    save_path = r'An_IOU.jpg'
    original_img, gray = get_image(img_path)
    blurred = Gaussian_Blur(gray)
    gradX, gradY, gradient = Sobel_gradient(blurred)
    thresh = Thresh_and_blur(gradient)
    closed = image_morphology(thresh)
    box = findcnts_and_box_point(closed)
    draw_img, crop_img = drawcnts_and_cut(original_img, box)

    cv2.imshow('original_img', original_img)
    cv2.imshow('blurred', blurred)
    cv2.imshow('gradX', gradX)
    cv2.imshow('gradY', gradY)
    cv2.imshow('final', gradient)
    cv2.imshow('thresh', thresh)
    cv2.imshow('closed', closed)
    cv2.imshow('draw_img', draw_img)
    cv2.imshow('crop_img', crop_img)
    cv2.waitKey(20171219)
    cv2.imwrite(save_path, crop_img)

    walk()