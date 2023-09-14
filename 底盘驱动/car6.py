from time import sleep
import sys
import tty
import termios
import serial
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
import sys
import RPi.GPIO as GPIO
from time import sleep
import keyboard

servopin1 = 20   # 舵机1,方向为左右转
servopin2 = 16  # 舵机2,方向为上下转
servopin3 = 7  # 舵机3,方向为上下转
servopin4 = 12  # 舵机4,方向为左右转
servopin5 = 5  # 舵机5,方向为上下转
servopin6 = 19  # 舵机6,方向为上下转

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin1, GPIO.OUT, initial=False)
GPIO.setup(servopin2, GPIO.OUT, initial=False)
GPIO.setup(servopin3, GPIO.OUT, initial=False)
GPIO.setup(servopin4, GPIO.OUT, initial=False)
GPIO.setup(servopin5, GPIO.OUT, initial=False)
GPIO.setup(servopin6, GPIO.OUT, initial=False)
p1 = GPIO.PWM(servopin1, 50)  # 50
p2 = GPIO.PWM(servopin2, 50)  # 50HZ
p3 = GPIO.PWM(servopin3, 50)  # 50HZ
p4 = GPIO.PWM(servopin4, 50)  # 50HZ
p5 = GPIO.PWM(servopin5, 50)  # 50HZ
p6 = GPIO.PWM(servopin6, 50)  # 50HZ

p1.start(12.5)  # 初始化角度
p2.start(11.63)  # 初始化角度
p3.start(3.9)  # 初始化角度
p4.start(4.7)  # 初始化角度
p5.start(4.72)  # 初始化角度
p6.start(9.72)  # 初始化角度
sleep(0.1)
p1.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
p2.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
p3.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
p4.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
p5.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
p6.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
sleep(0.1)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = True
        self.b1 = 12.5  # 云台舵机1初始化角度：90度
        self.b2 = 11.63  # 云台舵机2初始化角度：40度
        self.b3 = 3.9  # 云台舵机3初始化角度：20度
        self.b4 = 4.7  # 云台舵机4初始化角度：20度
        self.b5 = 4.72  # 云台舵机5初始化角度：20度
        self.b6 = 9.72  # 云台舵机6初始化角度：20度
        self.x = 0.3    # 步进长度
        self.s = 0.02

    def left1(self):
        if self.b1 >= 2.5:  # 判断角度是否大于0度
            self.b1 -= self.x
            print('当前角度为', self.b1)
            p1.ChangeDutyCycle(self.b1)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p1.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n**超出范围**\n')
            self.b1 = 2.5 - self.x
            p1.ChangeDutyCycle(self.b1)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p1.ChangeDutyCycle(0)
            sleep(0.01)  # 清除当前占空比，使舵机停止抖动

    def right1(self):

        if self.b1 <= 12.5:
            self.b1 += self.x
            print('当前角度为', self.b1)
            p1.ChangeDutyCycle(self.b1)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p1.ChangeDutyCycle(0)
            sleep(0.01)  # 清除当前占空比，使舵机停止抖动
        else:
            print('\n****超出范围****\n')
            self.b1 = 12.5 + self.x
            # g = q[self.b1]  #调用q列表中的第c位元素
            print('当前角度为', self.b1)
            p1.ChangeDutyCycle(self.b1)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p1.ChangeDutyCycle(0)
            sleep(0.01)  # 清除当前占空比，使舵机停止抖动

    def left2(self):

        if self.b2 > 2.8:  # 判断角度是否大于20度

            self.b2 -= self.x
            # g = q[self.b2]  #调用q列表中的第c位元素
            print('当前角度为', self.b2)
            p2.ChangeDutyCycle(self.b2)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p2.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n**超出范围**\n')
            self.b2 = 2.5
            # g = q[self.b2]  #调用q列表中的第c位元素
            p2.ChangeDutyCycle(self.b2)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p2.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def right2(self):

        if self.b2 < 11.94:
            self.b2 += self.x
            print('当前角度为', self.b2)
            p2.ChangeDutyCycle(self.b2)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p2.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n****超出范围****\n')
            self.b2 = 11.94
            # g = q[self.b2]  #调用q列表中的第c位元素
            p2.ChangeDutyCycle(self.b2)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p2.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def left3(self):

        if self.b3 > 3.61:  # 判断角度是否大于20度

            self.b3 -= self.x
            # g = q[self.b3]  #调用q列表中的第c位元素
            print('当前角度为', self.b3)
            p3.ChangeDutyCycle(self.b3)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p3.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n**超出范围**\n')
            self.b3 = 3.61
            # g = q[self.b3]  #调用q列表中的第c位元素
            p3.ChangeDutyCycle(self.b3)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p3.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def right3(self):
        if self.b3 < 12.5:
            self.b3 += self.x
            # g = q[self.b3]  #调用q列表中的第c位元素
            print('当前角度为', self.b3)
            p3.ChangeDutyCycle(self.b3)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p3.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n****超出范围****\n')
            self.b3 = 12.5
            # g = q[self.b3]  #调用q列表中的第c位元素
            p3.ChangeDutyCycle(self.b3)  # 执行角度变化，跳转到q列表中对应第c位元素的角度
            sleep(self.s)
            p3.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def left4(self):
        if self.b4 > 4.1:
            self.b4 -= self.x
            print('当前角度为', self.b4)
            p4.ChangeDutyCycle(self.b4)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p4.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n**超出范围**\n')
            self.b4 = 4.1 -self.x
            # g = q[self.b4]  #调用q列表中的第d位元素
            p4.ChangeDutyCycle(self.b4)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p4.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def right4(self):

        if self.b4 < 11.94:
            self.b4 += self.x
            # g = q[self.b4]  #调用q列表中的第d位元素
            print('当前角度为', self.b4)
            p4.ChangeDutyCycle(self.b4)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p4.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n****超出范围****\n')
            self.b4 = 11.94
            # g = q[self.b4]  #调用q列表中的第d位元素
            p4.ChangeDutyCycle(self.b4)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p4.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def left5(self):

        if self.b5 > 4.16:
            self.b5 -= self.x
            # g = q[self.b5]  #调用q列表中的第d位元素
            print('当前角度为', self.b5)
            p5.ChangeDutyCycle(self.b5)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p5.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n**超出范围**\n')
            self.b5 = 4.16
            # g = q[self.b5]  #调用q列表中的第d位元素
            p5.ChangeDutyCycle(self.b5)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p5.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def right5(self):

        if self.b5 < 11.38:
            self.b5 += self.x
            # g = q[self.b5]  #调用q列表中的第d位元素
            print('当前角度为', self.b5)
            p5.ChangeDutyCycle(self.b5)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p5.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n****超出范围****\n')
            self.b5 = 11.38
            # g = q[self.b5]  #调用q列表中的第d位元素
            p5.ChangeDutyCycle(self.b5)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p5.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def left6(self):

        if self.b6 > 5.83:
            self.b6 -= 0.4
            # g = q[self.b6]  #调用q列表中的第d位元素
            print('当前角度为', self.b6)
            p6.ChangeDutyCycle(self.b6)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p6.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n**超出范围**\n')
            self.b6 = 5.83
            # g = q[self.b6]  #调用q列表中的第d位元素
            p6.ChangeDutyCycle(self.b6)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p6.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
    def right6(self):

        if self.b6 < 9.72:
            self.b6 += 0.4
            # g = q[self.b6]  #调用q列表中的第d位元素
            print('当前角度为', self.b6)
            p6.ChangeDutyCycle(self.b6)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p6.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
        else:
            print('\n****超出范围****\n')
            self.b6 = 9.72
            # g = q[self.b6]  #调用q列表中的第d位元素
            p6.ChangeDutyCycle(self.b6)  # 执行角度变化，跳转到q列表中对应第d位元素的角度
            sleep(self.s)
            p6.ChangeDutyCycle(0)  # 清除当前占空比，使舵机停止抖动
            sleep(0.01)
######################################################################################################
    def left(self):
        ser.write('#001P1000T0000!'.encode())
        ser.write('#002P2000T0000!'.encode())
        ser.write('#003P1000T0000!'.encode())
        ser.write('#004P2000T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def right(self):
        ser.write('#001P2000T0000!'.encode())
        ser.write('#002P1000T0000!'.encode())
        ser.write('#003P2000T0000!'.encode())
        ser.write('#004P1000T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def up(self):
        ser.write('#001P2000T0000!'.encode())
        ser.write('#002P2000T0000!'.encode())
        ser.write('#003P2000T0000!'.encode())
        ser.write('#004P2000T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def down(self):
        ser.write('#001P1300T0000!'.encode())
        ser.write('#002P1300T0000!'.encode())
        ser.write('#003P1300T0000!'.encode())
        ser.write('#004P1300T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def stop(self):
        ser.write('#001P1500T0000!'.encode())
        ser.write('#002P1500T0000!'.encode())
        ser.write('#003P1500T0000!'.encode())
        ser.write('#004P1500T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def r(self):
        ser.write('#001P1000T0000!'.encode())
        ser.write('#002P1000T0000!'.encode())
        ser.write('#003P2000T0000!'.encode())
        ser.write('#004P2000T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def t(self):
        ser.write('#001P2000T0000!'.encode())
        ser.write('#002P2000T0000!'.encode())
        ser.write('#003P1000T0000!'.encode())
        ser.write('#004P1000T0000!'.encode())
        ser.flushInput()  # 清空接收缓存区
        sleep(0.1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and self.flag:
            self.left()
            self.flag = False
        if event.key() == Qt.Key_D and self.flag:
            self.right()
            self.flag = False
        if event.key() == Qt.Key_W and self.flag:
            self.up()
            self.flag = False
        if event.key() == Qt.Key_S and self.flag:
            self.down()
            self.flag = False
        if event.key() == Qt.Key_Q and self.flag:
            self.t()
            self.flag = False
        if event.key() == Qt.Key_E and self.flag:
            self.r()
            self.flag = False
        if event.key() == Qt.Key_R:
            self.left1()
        if event.key() == Qt.Key_F:
            self.right1()
        if event.key() == Qt.Key_T:
            self.left2()
        if event.key() == Qt.Key_G:
            self.right2()
        if event.key() == Qt.Key_Y:
            self.left3()
        if event.key() == Qt.Key_H:
            self.right3()
        if event.key() == Qt.Key_U:
            self.left4()
        if event.key() == Qt.Key_J:
            self.right4()
        if event.key() == Qt.Key_I:
            self.left5()
        if event.key() == Qt.Key_K:
            self.right5()
        if event.key() == Qt.Key_O:
            self.left6()
        if event.key() == Qt.Key_L:
            self.right6()

    def keyReleaseEvent(self, event):

        if event.isAutoRepeat():
            pass
        else:
            self.stop()
            self.flag = True


ser = serial.Serial("/dev/ttyAMA0", 115200)

# ser1 = serial.Serial("/dev/ttyAMA1",1200)
# color = ser1.read()
# print("颜色是",color)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
