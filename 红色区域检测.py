import cv2
import numpy as np

Kp = 0.85
Ki = 0
Kd = 0  # 定义pid初始值
last_Err_y = last_Err_x = 0  # 上一个误差值初始化
total_Err_y = total_Err_x = 0  # 误差累加初始化
output_y = output_x = 0  # PID输出初始化


# 面向对象的编程思想，创建pid类
class PID:
    # 实例化
    def __init__(self, Kp, Kd, Ki):
        self.Error = 0
        self.Kp = Kp  # 比例增益
        self.Kd = Kd  # 积分增益
        self.Ki = Ki  # 微分增益
        self.last_Err = 0
        self.total_Err = 0

    # pid算法
    def PIDcal(self, Target_value, ActualValue):
        self.Error = Target_value - ActualValue  # 计算偏差
        self.total_Err = self.total_Err + self.Error  # 偏差累加
        output = self.Kp * self.Error + self.Ki * self.total_Err + self.Kd * (self.Error - self.last_Err)  # PID运算
        self.last_Err = self.Error  # 将本次偏差赋给上次一偏差
        return output


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # 打开相机接口
    while 1:
        ret, img = cap.read()  # 读取从相机接口中收到的图片，ret为布尔值，img为矩阵
        center_w = int(img.shape[0] / 2)
        center_h = int(img.shape[1] / 2)  # 利用shape函数算出当前图片的中心坐标
        # 在彩色图像的情况下，解码图像将以b g r顺序存储通道。
        grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 高斯模糊，对图片进行降噪
        grid_RGB = cv2.GaussianBlur(grid_RGB, (15, 15), 0)
        # 从RGB色彩空间转换到HSV色彩空间
        grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)
        # 设定HSV空间阈值，根据HSV色彩空间阈值图我设定的阈值为红色
        lower2 = np.array([156, 43, 46])
        upper2 = np.array([180, 255, 255])
        # 图像二值化
        mask2 = cv2.inRange(grid_HSV, lower2, upper2)

        # 形态学去噪，cv2.MORPH_CLOSE先腐蚀再膨胀，cv2.MORPH_CLOSE先膨胀再腐蚀
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel, iterations=1)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel, iterations=1)
        # 获取轮廓的点集
        cnts = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        # 画出图像中心，为了后来的标定
        cv2.circle(img, (center_h, center_w), 7, (255, 255, 255), -1)
        # 检测画面是否有红色的图像
        if cnts != 0:
            for i in cnts:
                # 求取轮廓的矩
                M = cv2.moments(i)
                # 除数不为0原则
                if M['m00'] != 0:
                    # 求轮廓的中心坐标
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    # 画出轮廓与中心
                    cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
                    cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                    pid = PID(0.8, 0.5, 0.5)
                    # 利用pid算法算出和目标值误差
                    output_x = pid.PIDcal(center_h, cx)
                    output_y = pid.PIDcal(center_w, cy)
                    # 输出与目标的差值
                    print(f"x偏移量:{output_x}, y偏移量:{output_y}")
        # 展示画面
        cv2.imshow('hsv', grid_HSV)
        cv2.imshow('red', mask2)
        cv2.imshow('final', img)
        # 50毫秒的画面等待
        key = cv2.waitKey(50)
        if key == ord('q'):  # 判断是哪一个键按下，退出循环程序
            break
cv2.destroyAllWindows()  # 窗口清空
