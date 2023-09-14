import RPi.GPIO as GPIO
from time import sleep
import keyboard
import sys
import tty
import termios
import serial

ser = serial.Serial("/dev/ttyAMA0",115200)


def right():
    ser.write('#001P1100T0000!'.encode())
    ser.write('#002P1900T0000!'.encode())
    ser.write('#003P1100T0000!'.encode())
    ser.write('#004P1900T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)

       
def left():
    ser.write('#001P1900T0000!'.encode())
    ser.write('#002P1100T0000!'.encode())
    ser.write('#003P1900T0000!'.encode())
    ser.write('#004P1100T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)

def up():
    ser.write('#001P1900T0000!'.encode())
    ser.write('#002P1900T0000!'.encode())
    ser.write('#003P1900T0000!'.encode())
    ser.write('#004P1900T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)

def down():
    ser.write('#001P1100T0000!'.encode())
    ser.write('#002P1100T0000!'.encode())
    ser.write('#003P1100T0000!'.encode())
    ser.write('#004P1100T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)
def stop():
    ser.write('#001P1500T0000!'.encode())
    ser.write('#002P1500T0000!'.encode())
    ser.write('#003P1500T0000!'.encode())
    ser.write('#004P1500T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1) 
def r():
    ser.write('#001P1100T0000!'.encode())
    ser.write('#002P1100T0000!'.encode())
    ser.write('#003P1900T0000!'.encode())
    ser.write('#004P1900T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1) 
def t():
    ser.write('#001P1900T0000!'.encode())
    ser.write('#002P1900T0000!'.encode())
    ser.write('#003P1100T0000!'.encode())
    ser.write('#004P1100T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)   

# def readchar():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch

# def readkey(getchar_fn=None):
#     getchar = getchar_fn or readchar
#     c1 = getchar()
#     if ord(c1) != 0x1b:
#         return c1
#     c2 = getchar()
#     if ord(c2) != 0x5b:
#         return c1
#     c3 = getchar()
#     return chr(0x10 + ord(c3) - 65)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def tonum(num):  # 用于处理角度转换的函数
    fm = 10.0 / 180.0
    num = num * fm + 2.5
    num = int(num * 10) / 10.0
    return num

servopin1 = 20   #舵机1,方向为左右转
servopin2 = 16   #舵机2,方向为上下转
servopin3 = 7    #舵机3,方向为上下转
servopin4 =12   #舵机4,方向为左右转
servopin5 =5  #舵机5,方向为上下转
servopin6 = 19    #舵机6,方向为上下转

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin1, GPIO.OUT)
GPIO.setup(servopin2, GPIO.OUT)
GPIO.setup(servopin3, GPIO.OUT)
GPIO.setup(servopin4, GPIO.OUT)
GPIO.setup(servopin5, GPIO.OUT)
GPIO.setup(servopin6, GPIO.OUT)
p1 = GPIO.PWM(servopin1,50) #25HZ
p2 = GPIO.PWM(servopin2,50) #50HZ
p3 = GPIO.PWM(servopin3,50) #50HZ
p4 = GPIO.PWM(servopin4,50) #50HZ
p5 = GPIO.PWM(servopin5,50) #50HZ
p6 = GPIO.PWM(servopin6,50) #50HZ

p1.start(tonum(0)) #初始化角度
p2.start(tonum(40)) #初始化角度
p3.start(tonum(85)) #初始化角度
p4.start(tonum(85)) #初始化角度
p5.start(tonum(40)) #初始化角度
p6.start(tonum(85)) #初始化角度
sleep(0.5)
p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p3.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p4.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p5.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p6.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
sleep(0.1)



#a代表舵机的执行次数
#b代表舵机的初始化角度
a1 = 0  #云台舵机1的执行次数
b1 = 90  #云台舵机1初始化角度：90度
a2 = 0  #云台舵机2的执行次数
b2 = 90  #云台舵机2初始化角度：40度
a3 = 0  #云台舵机3的执行次数
b3 = 90  #云台舵机3初始化角度：20度
a4 = 0  #云台舵机4的执行次数
b4 = 90  #云台舵机4初始化角度：20度
a5 = 0  #云台舵机5的执行次数
b5 = 90  #云台舵机5初始化角度：20度
a6 = 0  #云台舵机6的执行次数
b6 = 90  #云台舵机6初始化角度：20度

q = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
    100, 110, 120, 130, 140, 150, 160, 170, 180,
    190, 200,210, 220, 230, 240, 250, 260, 270]  #旋转角度列表 一共19个元组

def left1():
    global a1, b1   #引入全局变量
    # a1 += 1
    if b1 > 0 :  #判断角度是否大于20度
        b1 -= 2
        # g = q[b1]  #调用q列表中的第c位元素
        # print('当前角度为',b1)
        p1.ChangeDutyCycle(tonum(b1))  #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动

    else:
        print('\n**超出范围**\n')
        b1 = 0
        # g = q[b1]  #调用q列表中的第c位元素
        p1.ChangeDutyCycle(tonum(b1)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
        
       
def right1():
    global a1, b1    #引入全局变量
    # a1 += 1
    if b1 < 270 :
        b1 += 1
        # g = q[b1]  #调用q列表中的第c位元素
        # print('当前角度为',b1)
        p1.ChangeDutyCycle(tonum(b1)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        
    else:
        print('\n****超出范围****\n')
        b1 = 270
        # g = q[b1]  #调用q列表中的第c位元素
        p1.ChangeDutyCycle(tonum(b1)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        
    
def left2():
    global a2, b2   #引入全局变量
    a2 += 1
    if b2 > 0:  #判断角度是否大于20度
        
        b2 -= 1
        # g = q[b2]  #调用q列表中的第c位元素
        print('当前角度为',b2)
        p2.ChangeDutyCycle(tonum(b2))  #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.1)
        p2.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动

    else:
        print('\n**超出范围**\n')
        b2 = 0
        # g = q[b2]  #调用q列表中的第c位元素
        p2.ChangeDutyCycle(tonum(b2)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.1)
        p2.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动

       
def right2():
    global a2, b2    #引入全局变量
    a2 += 1
    if b2 < 170:
        b2 = b2+1
        #g = q[b2]  #调用q列表中的第c位元素
        print('当前角度为',b2)
        p2.ChangeDutyCycle(tonum(b2)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n****超出范围****\n')
        b2 = 170
        # g = q[b2]  #调用q列表中的第c位元素
        p2.ChangeDutyCycle(tonum(b2)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动


def left3():
    global a3, b3   #引入全局变量
    a3 += 1
    if b3 > 20:  #判断角度是否大于20度
        
        b3 -= 1
        # g = q[b3]  #调用q列表中的第c位元素
        print('当前角度为',b3)
        p3.ChangeDutyCycle(tonum(b3))  #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p3.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动

    else:
        print('\n**超出范围**\n')
        b3 = 20
        # g = q[b3]  #调用q列表中的第c位元素
        p3.ChangeDutyCycle(tonum(b3)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p3.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动

       
def right3():
    global a3, b3    #引入全局变量
    a3 += 1
    if b3 < 180:
        b3 += 1
        # g = q[b3]  #调用q列表中的第c位元素
        print('当前角度为',b3)
        p3.ChangeDutyCycle(tonum(b3)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p3.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n****超出范围****\n')
        b3 = 180
        # g = q[b3]  #调用q列表中的第c位元素
        p3.ChangeDutyCycle(tonum(b3)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.01)
        p3.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动



def left4():
    global a4, b4    #引入全局变量
    a4 += 1
    if b4 > 3:
        b4 -= 1
        # g = q[b4]  #调用q列表中的第d位元素
        print('当前角度为',b4)
        p4.ChangeDutyCycle(tonum(b4)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p4.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n**超出范围**\n')
        b4 = 30
        # g = q[b4]  #调用q列表中的第d位元素
        p4.ChangeDutyCycle(tonum(b4)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p4.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动


def right4():
    global a4, b4    #引入全局变量
    a4 += 1
    if b4 < 170:
        b4 += 1
        # g = q[b4]  #调用q列表中的第d位元素
        print('当前角度为',b4)
        p4.ChangeDutyCycle(tonum(b4)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p4.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n****超出范围****\n')
        b4 = 170
        # g = q[b4]  #调用q列表中的第d位元素
        p4.ChangeDutyCycle(tonum(b4)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p4.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动


def left5():
    global a5, b5    #引入全局变量
    a5 += 1
    if b5 > 30:
        b5-= 1
        # g = q[b5]  #调用q列表中的第d位元素
        print('当前角度为',b5)
        p5.ChangeDutyCycle(tonum(b5)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p5.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n**超出范围**\n')
        b5 = 30
        # g = q[b5]  #调用q列表中的第d位元素
        p5.ChangeDutyCycle(tonum(b5)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p5.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动


def right5():
    global a5, b5    #引入全局变量
    a5 += 1
    if b5 < 160:
        b5 += 1
        # g = q[b5]  #调用q列表中的第d位元素
        print('当前角度为',b5)
        p5.ChangeDutyCycle(tonum(b5)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p5.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n****超出范围****\n')
        b5 = 160
        # g = q[b5]  #调用q列表中的第d位元素
        p5.ChangeDutyCycle(tonum(b5)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p5.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动



def left6():
    global a6, b6    #引入全局变量
    a6 += 1
    if b6 > 60:
        b6 -= 1
        # g = q[b6]  #调用q列表中的第d位元素
        print('当前角度为',b6)
        p6.ChangeDutyCycle(tonum(b6)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p6.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n**超出范围**\n')
        b6 = 80
        # g = q[b6]  #调用q列表中的第d位元素
        p6.ChangeDutyCycle(tonum(b6)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p6.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动


def right6():
    global a6, b6    #引入全局变量
    a6 += 1
    if b6 < 130 :
        b6 += 1
        # g = q[b6]  #调用q列表中的第d位元素
        print('当前角度为',b6)
        p6.ChangeDutyCycle(tonum(b6)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p6.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动

    else:
        print('\n****超出范围****\n')
        b6 = 130
        # g = q[b6]  #调用q列表中的第d位元素
        p6.ChangeDutyCycle(tonum(b6)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.01)
        p6.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动


#获取键盘值
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == '__main__':

    while True :

        keyboard.add_hotkey('a', left1)
        keyboard.add_hotkey('d', right1)
    # 按f1输出aaa
        keyboard.wait()
            # i = readchar()
        
            # if i ==  'a':
            #     left()
            # elif i == 'd':
            #     right()
            # elif i == 'w':
            #     up()
            # elif i == 's':
            #     down()
            # elif i == 'n':
            #     r()
            # elif i == 'm':   
            #     t()
            # elif i == 'b':  
            #     stop()    


            # elif i == 'r':
            #     left1()
            # elif i == 'f':
            #     right1()
            # elif i == 't':
            #     left2()
            # elif i == 'g':
            #     right2()
            # elif i == 'y':
            #     left3()
            # elif i == 'h':
            #     right3()
            # elif i == 'u':
            #     left4()
            # elif i == 'j':
            #     right4()
            # elif i == 'i':
            #     left5()
            # elif i == 'k':
            #     right5()
            # elif i == 'o':
            #     left6()
            # elif i == 'l':
            #     right6()
            # elif i == 'q':  
            #     GPIO.cleanup()
            #     sys.exit()
               
