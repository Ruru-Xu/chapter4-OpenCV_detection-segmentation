# -*- coding=GBK -*-
import cv2 as cv
import numpy as np


# ͼ���ֵ�� 0��ɫ 1��ɫ
# ȫ����ֵ
def threshold_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow("ԭ��", gray)

    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)  # ���ɷ�,ȫ������Ӧ��ֵ ����0�ɸ�Ϊ�������ֵ���������
    print("��ֵ��%s" % ret)
    cv.imshow("OTSU", binary)

    ret, binary = cv.threshold(gray, 0, 255,
                               cv.THRESH_BINARY | cv.THRESH_TRIANGLE)  # TRIANGLE��,��ȫ������Ӧ��ֵ, ����0�ɸ�Ϊ�������ֵ��������ã������ڵ�������
    print("��ֵ��%s" % ret)
    cv.imshow("TRIANGLE", binary)

    ret, binary = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)  # �Զ�����ֵΪ150,����150���ǰ�ɫ С�ڵ��Ǻ�ɫ
    print("��ֵ��%s" % ret)
    cv.imshow("�Զ���", binary)

    ret, binary = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)  # �Զ�����ֵΪ150,����150���Ǻ�ɫ С�ڵ��ǰ�ɫ
    print("��ֵ��%s" % ret)
    cv.imshow("�Զ��巴ɫ", binary)

    ret, binary = cv.threshold(gray, 150, 255, cv.THRESH_TRUNC)  # �ض� ����150���Ǹ�Ϊ150  С��150�ı���
    print("��ֵ��%s" % ret)
    cv.imshow("�ض�1", binary)

    ret, binary = cv.threshold(gray, 150, 255, cv.THRESH_TOZERO)  # �ض� С��150���Ǹ�Ϊ150  ����150�ı���
    print("��ֵ��%s" % ret)
    cv.imshow("�ض�2", binary)


src = cv.imread("C:/Users/Administrator/Desktop/pic/mask/00.jpg")
threshold_image(src)
cv.waitKey(0)
cv.destroyAllWindows()