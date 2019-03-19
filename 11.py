import cv2 as cv
import numpy as np

#全局阈值
def threshold_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    cv.imwrite('gtay.jpg', gray)
    '''
     threshold(src, thresh, maxval, type[, dst]) -> retval, dst
    src参数表示输入图像（多通道，8位或32位浮点）。
    thresh参数表示阈值。
    maxval参数表示与THRESH_BINARY和THRESH_BINARY_INV阈值类型一起使用设置的最大值。
    type参数表示阈值类型。
    retval参数表示返回的阈值。若是全局固定阈值算法，则返回thresh参数值。若是全局自适应阈值算法，则返回自适应计算得出的合适阈值。
    dst参数表示输出与src相同大小和类型以及相同通道数的图像。
    '''
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    #https://www.cnblogs.com/FHC1994/p/9125570.html
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE) #TRIANGLE法,全局自适应阈值,第二个参数值0可改为任意数字但不起作用，适用于单个波峰。
    print("threshold value %s"%ret)
    cv.imwrite('binary.jpg', binary)
    cv.namedWindow("binary0", cv.WINDOW_NORMAL)
    cv.imshow("binary0", binary)

#局部阈值
def local_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    '''
    adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst]) -> dst
    src参数表示输入图像（8位单通道图像）。
    maxValue参数表示使用THRESH_BINARY和THRESH_BINARY_INV的最大值.
    adaptiveMethod参数表示自适应阈值算法，平均 （ADAPTIVE_THRESH_MEAN_C）或高斯（ADAPTIVE_THRESH_GAUSSIAN_C）。
    thresholdType参数表示阈值类型，必须为THRESH_BINARY或THRESH_BINARY_INV的阈值类型。
    blockSize参数表示块大小（奇数且大于1，比如3，5，7........ ）。
    C参数是常数，表示从平均值或加权平均值中减去的数。 通常情况下，这是正值，但也可能为零或负值。
    '''
    #自适应阈值化能够根据图像不同区域亮度分布，改变阈值
    binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 25, 10)
    cv.namedWindow("binary1", cv.WINDOW_NORMAL)
    cv.imshow("binary1", binary)

#用户自己计算阈值
def custom_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    h, w =gray.shape[:2]
    m = np.reshape(gray, [1,w*h])
    mean = m.sum()/(w*h)
    print("mean:",mean)
    ret, binary =  cv.threshold(gray, mean, 255, cv.THRESH_BINARY)
    cv.namedWindow("binary2", cv.WINDOW_NORMAL)
    cv.imshow("binary2", binary)

src = cv.imread('1.jpg')
# #namedWindow函数，用于创建一个窗口，默认值为WINDOW_AUTOSIZE，所以一般情况下，这个函数我们填第一个变量就可以了。其实这一行代码没有也可以正常显示的（下面imshow会显示）
cv.namedWindow('input_image', cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
cv.imshow('input_image', src)  #在指定的窗口中显示一幅图像
threshold_demo(src)
local_threshold(src)
custom_threshold(src)
cv.waitKey(0) # 参数=0: （也可以是小于0的数值）一直显示，不会有返回值      若在键盘上按下一个键即会消失 ，则会返回一个按键对应的ascii码值；参数>0:显示多少毫秒；超过这个指定时间则返回-1
cv.destroyAllWindows()  #删除建立的全部窗口，释放资源