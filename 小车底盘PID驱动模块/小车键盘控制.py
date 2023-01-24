from time import sleep
import sys
import tty
import termios
import serial

ser = serial.Serial("/dev/ttyAMA0",115200)
# ser1 = serial.Serial("/dev/ttyAMA1",1200)
# color = ser1.read()
# print("颜色是",color)
def left():
    ser.write('#001P1000T0000!'.encode())
    ser.write('#002P2000T0000!'.encode())
    ser.write('#003P1000T0000!'.encode())
    ser.write('#004P2000T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)

       
def right():
    ser.write('#001P2000T0000!'.encode())
    ser.write('#002P1000T0000!'.encode())
    ser.write('#003P2000T0000!'.encode())
    ser.write('#004P1000T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)

def up():
    ser.write('#001P2000T0000!'.encode())
    ser.write('#002P2000T0000!'.encode())
    ser.write('#003P2000T0000!'.encode())
    ser.write('#004P2000T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)

def down():
    ser.write('#001P1300T0000!'.encode())
    ser.write('#002P1300T0000!'.encode())
    ser.write('#003P1300T0000!'.encode())
    ser.write('#004P1300T0000!'.encode())
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
    ser.write('#001P1000T0000!'.encode())
    ser.write('#002P1000T0000!'.encode())
    ser.write('#003P2000T0000!'.encode())
    ser.write('#004P2000T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1) 
def t():
    ser.write('#001P2000T0000!'.encode())
    ser.write('#002P2000T0000!'.encode())
    ser.write('#003P1000T0000!'.encode())
    ser.write('#004P1000T0000!'.encode())
    ser.flushInput()                 # 清空接收缓存区
    sleep(0.1)   
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

if __name__ == '__main__':
    while True:
        i = readkey()
        
        if i ==  'a':
            left()
        if i == 'd':
            right()
        if i == 'w':
            up()
        if i == 's':
            down()
        if i == 'n':
            r()
        if i == 'm':   
            t()
        if i == 'b':  
            stop()    
        if i == 'q':  
            sys.exit()
            

           
