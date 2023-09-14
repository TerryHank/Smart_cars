from time import sleep
import sys
import tty
import termios
import serial
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = True

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
        if event.key() == Qt.Key_N and self.flag:
            self.t()
            self.flag = False
        if event.key() == Qt.Key_M and self.flag:
            self.r()
            self.flag = False


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
