import RPi.GPIO as GPIO
import time
from time import sleep
import serial
from plot_pid import sub_plot_c

ser = serial.Serial("/dev/ttyAMA0",115200)

draw = sub_plot_c()
class PID_MOTOR_4D(object):
    def __init__(self, spd_init, spd_targe):

        # 初始一个速度
        self.spd_temp_l1 = self.spd_temp_l2 = self.spd_temp_r1 = self.spd_temp_r2 = spd_init
        # 设定一个目标速度
        self.spd_target = spd_targe

        # self.L1_PWA = 17
        # self.L1_AIN1 = 22
        # self.L1_AIN2 = 27
        self.L1_SensorINPUT = 2
        self.L1_encoder_c = 0  # 编码器当前数值
        self.L1_record_encoder = 0  # 编码器计数数值
        self.L1_bias_last = 0
        self.L1_bias_integral = 0
        self.L1_motor_pwm_out = 0
        self.L1_Motor = None

        # self.R1_PWA = 25
        # self.R1_AIN1 = 23
        # self.R1_AIN2 = 24
        self.R1_SensorINPUT = 3
        self.R1_encoder_c = 0  # 编码器当前数值
        self.R1_record_encoder = 0  # 编码器计数数值
        self.R1_bias_last = 0
        self.R1_bias_integral = 0
        self.R1_motor_pwm_out = 0
        self.R1_Motor = None

        # self.L2_PWA = 19
        # self.L2_AIN1 = 6
        # self.L2_AIN2 = 13
        self.L2_SensorINPUT = 17
        self.L2_encoder_c = 0  # 编码器当前数值
        self.L2_record_encoder = 0  # 编码器计数数值
        self.L2_bias_last = 0
        self.L2_bias_integral = 0
        self.L2_motor_pwm_out = 0
        self.L2_Motor = None

        # self.R2_PWA = 21
        # self.R2_AIN1 = 16
        # self.R2_AIN2 = 20
        self.R2_SensorINPUT = 18
        self.R2_encoder_c = 0  # 编码器当前数值
        self.R2_record_encoder = 0  # 编码器计数数值
        self.R2_bias_last = 0
        self.R2_bias_integral = 0
        self.R2_motor_pwm_out = 0
        self.R2_Motor = None

        self.PID_SCALE = 0.01  # PID缩放系数
        self.PID_INTEGRAL_UP = 1000  # 积分上限

        self.ax_motor_kp = 600;  # 电机转速PID-P
        self.ax_motor_ki = 500;  # 电机转速PID-I
        self.ax_motor_kd = 400;  # 电机转速PID-D

        self.record_count = self.record_time = 0  # 计数器, 时间器,   # 每3次计算一次速度

    def setup(self):
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)  # BCM model

        # 左电机引脚配置
        # GPIO.setup(self.L1_AIN1, GPIO.OUT)  # total output model
        # GPIO.setup(self.L1_AIN2, GPIO.OUT)
        # GPIO.setup(self.L1_PWA, GPIO.OUT)
        GPIO.setup(self.L1_SensorINPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # GPIO.setup(self.L2_AIN1, GPIO.OUT)  # total output model
        # GPIO.setup(self.L2_AIN2, GPIO.OUT)
        # GPIO.setup(self.L2_PWA, GPIO.OUT)
        GPIO.setup(self.L2_SensorINPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # 右电机引脚配置
        # GPIO.setup(self.R1_AIN1, GPIO.OUT)  # total output model
        # GPIO.setup(self.R1_AIN2, GPIO.OUT)
        # GPIO.setup(self.R1_PWA, GPIO.OUT)
        GPIO.setup(self.R1_SensorINPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # GPIO.setup(self.R2_AIN1, GPIO.OUT)  # total output model
        # GPIO.setup(self.R2_AIN2, GPIO.OUT)
        # GPIO.setup(self.R2_PWA, GPIO.OUT)
        GPIO.setup(self.R2_SensorINPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # # 左电机输出
        # self.L1_Motor = GPIO.PWM(self.L1_PWA, 100)
        # self.L1_Motor.start(0)

        # self.L2_Motor = GPIO.PWM(self.L2_PWA, 100)
        # self.L2_Motor.start(0)

        # # 右电机输出
        # self.R1_Motor = GPIO.PWM(self.R1_PWA, 100)
        # self.R1_Motor.start(0)

        # self.R2_Motor = GPIO.PWM(self.R2_PWA, 100)
        # self.R2_Motor.start(0)

        # 左电机转速边缘检测，每转一次，读取一次速度
        def exti_moter_L1(channel):

            if GPIO.input(self.L1_SensorINPUT) == 1:
                self.L1_encoder_c += 1

        def exti_moter_L2(channel):

            if GPIO.input(self.L2_SensorINPUT) == 1:
                self.L2_encoder_c += 1

        # 边缘检测
        GPIO.add_event_detect(self.L1_SensorINPUT, GPIO.RISING, callback=exti_moter_L1)
        GPIO.add_event_detect(self.L2_SensorINPUT, GPIO.RISING, callback=exti_moter_L2)

        def exti_moter_R1(channel):

            if GPIO.input(self.R1_SensorINPUT) == 1:
                self.R1_encoder_c += 1

        def exti_moter_R2(channel):

            if GPIO.input(self.R2_SensorINPUT) == 1:
                self.R2_encoder_c += 1

        GPIO.add_event_detect(self.R1_SensorINPUT, GPIO.RISING, callback=exti_moter_R1)
        GPIO.add_event_detect(self.R2_SensorINPUT, GPIO.RISING, callback=exti_moter_R2)

    # 通过计数1000，求得时间差dt, 读取转速差dc， 通过dc/dt求得速度
    def get_spd(self):

        print('code_L1', self.L1_encoder_c)
        print(self.record_count)

        if self.record_count == 1:

            current_time = round(time.time() * 1000)

            # 电机编码器的计数差
            dc_l1 = self.L1_encoder_c - self.L1_record_encoder
            self.L1_record_encoder = self.L1_encoder_c

            dc_l2 = self.L2_encoder_c - self.L2_record_encoder
            self.L2_record_encoder = self.L2_encoder_c

            dc_r1 = self.R1_encoder_c - self.R1_record_encoder
            self.R1_record_encoder = self.R1_encoder_c

            dc_r2 = self.R2_encoder_c - self.R2_record_encoder
            self.R2_record_encoder = self.R2_encoder_c

            # 更新参数
            dt = current_time - self.record_time

            self.record_time = current_time

            self.record_count = 0

            # L1电机速度
            spd_l1 = dc_l1 / dt
            spd_l2 = dc_l2 / dt
            spd_r1 = dc_r1 / dt
            spd_r2 = dc_r2 / dt

            return spd_l1, spd_l2, spd_r1, spd_r2
        else:
            self.record_count += 1

        return None, None, None, None

    def PID_MotorCtl_L1(self, target, current):

        # 获得偏差值
        bias = target - current

        # 计算偏差累加值
        self.L1_bias_integral += bias

        # 抗积分饱和
        if (self.L1_bias_integral > self.PID_INTEGRAL_UP): self.L1_bias_integral = self.PID_INTEGRAL_UP
        if (self.L1_bias_integral < -self.PID_INTEGRAL_UP): self.L1_bias_integral = -self.PID_INTEGRAL_UP

        # PID计算电机输出PWM值
        self.L1_motor_pwm_out += self.ax_motor_kp * bias * self.PID_SCALE + self.ax_motor_kd * (
                    bias - self.L1_bias_last) * self.PID_SCALE + self.ax_motor_ki * self.L1_bias_integral * self.PID_SCALE

        # 记录上次偏差
        self.L1_bias_last = bias

        # 限制最大输出
        if self.L1_motor_pwm_out > 100:
            self.L1_motor_pwm_out = 100
        if self.L1_motor_pwm_out <= 0:
            self.L1_motor_pwm_out = 10

        return self.L1_motor_pwm_out

    def PID_MotorCtl_L2(self, target, current):

        # 获得偏差值
        bias = target - current

        # 计算偏差累加值
        self.L2_bias_integral += bias

        # 抗积分饱和
        if (self.L2_bias_integral > self.PID_INTEGRAL_UP): self.L2_bias_integral = self.PID_INTEGRAL_UP
        if (self.L2_bias_integral < -self.PID_INTEGRAL_UP): self.L2_bias_integral = -self.PID_INTEGRAL_UP

        # PID计算电机输出PWM值
        self.L2_motor_pwm_out += self.ax_motor_kp * bias * self.PID_SCALE + self.ax_motor_kd * (
                    bias - self.L2_bias_last) * self.PID_SCALE + self.ax_motor_ki * self.L2_bias_integral * self.PID_SCALE

        # 记录上次偏差
        self.L2_bias_last = bias

        # 限制最大输出
        if self.L2_motor_pwm_out > 100:
            self.L2_motor_pwm_out = 100
        if self.L2_motor_pwm_out <= 0:
            self.L2_motor_pwm_out = 10

        return self.L2_motor_pwm_out

    def PID_MotorCtl_R1(self, target, current):

        # 获得偏差值
        bias = target - current

        # 计算偏差累加值
        self.R1_bias_integral += bias

        # 抗积分饱和
        if (self.R1_bias_integral > self.PID_INTEGRAL_UP): self.R1_bias_integral = self.PID_INTEGRAL_UP
        if (self.R1_bias_integral < -self.PID_INTEGRAL_UP): self.R1_bias_integral = -self.PID_INTEGRAL_UP

        # PID计算电机输出PWM值
        self.R1_motor_pwm_out += self.ax_motor_kp * bias * self.PID_SCALE + self.ax_motor_kd * (
                    bias - self.R1_bias_last) * self.PID_SCALE + self.ax_motor_ki * self.R1_bias_integral * self.PID_SCALE

        # 记录上次偏差
        self.R1_bias_last = bias

        # 限制最大输出
        if self.R1_motor_pwm_out > 100:
            self.R1_motor_pwm_out = 100
        if self.R1_motor_pwm_out <= 0:
            self.R1_motor_pwm_out = 10

        return self.R1_motor_pwm_out

    def PID_MotorCtl_R2(self, target, current):

        # 获得偏差值
        bias = target - current

        # 计算偏差累加值
        self.R2_bias_integral += bias

        # 抗积分饱和
        if (self.R2_bias_integral > self.PID_INTEGRAL_UP): self.R2_bias_integral = self.PID_INTEGRAL_UP
        if (self.R2_bias_integral < -self.PID_INTEGRAL_UP): self.R2_bias_integral = -self.PID_INTEGRAL_UP

        # PID计算电机输出PWM值
        self.R2_motor_pwm_out += self.ax_motor_kp * bias * self.PID_SCALE + self.ax_motor_kd * (
                    bias - self.R2_bias_last) * self.PID_SCALE + self.ax_motor_ki * self.R2_bias_integral * self.PID_SCALE

        # 记录上次偏差
        self.R2_bias_last = bias

        # 限制最大输出
        if self.R2_motor_pwm_out > 100:
            self.R2_motor_pwm_out = 100
        if self.R2_motor_pwm_out <= 0:
            self.R2_motor_pwm_out = 10

        return self.R2_motor_pwm_out

    def t_up(self, spd_l1, spd_l2, spd_r1, spd_r2, t_time):

        # self.L1_Motor = int(1500 + spd_l1 *10)
        # self.L2_Motor = int(1500 + spd_l2 *10)
        # self.R1_Motor = int(1500 + spd_r1 *10)
        # self.R2_Motor = int(1500 + spd_r2 *10)
        a = '#001P%s'%(int(1500 + spd_l1 *10))+'T0000!'
        b = '#002P%s'%(int(1500 + spd_l2 *10))+'T0000!'
        c = '#003P%s'%(int(1500 + spd_r1 *10))+'T0000!'
        d = '#004P%s'%(int(1500 + spd_r2 *10))+'T0000!'
        ser.write(a.encode())
        ser.write(b.encode())
        ser.write(c.encode())
        ser.write(d.encode())

        time.sleep(t_time)

    # def t_down(self, spd_l1, spd_l2, spd_r1, spd_r2, t_time):

    #     self.L1_Motor.ChangeDutyCycle(spd_l1)
    #     GPIO.output(self.L1_AIN2, GPIO.LOW)  # AIN2
    #     GPIO.output(self.L1_AIN1, GPIO.HIGH)  # AIN1

    #     self.L2_Motor.ChangeDutyCycle(spd_l2)
    #     GPIO.output(self.L2_AIN2, GPIO.HIGH)  # AIN2
    #     GPIO.output(self.L2_AIN1, GPIO.LOW)  # AIN1

    #     self.R1_Motor.ChangeDutyCycle(spd_r1)
    #     GPIO.output(self.R1_AIN2, GPIO.LOW)  # AIN2
    #     GPIO.output(self.R1_AIN1, GPIO.HIGH)  # AIN1

    #     self.R2_Motor.ChangeDutyCycle(spd_r2)
    #     GPIO.output(self.R2_AIN2, GPIO.HIGH)  # AIN2
    #     GPIO.output(self.R2_AIN1, GPIO.LOW)  # AIN1

    #     time.sleep(t_time)

    # def t_left(self, spd_l1, spd_l2, spd_r1, spd_r2, t_time):

    #     self.L1_Motor.ChangeDutyCycle(spd_l1)
    #     GPIO.output(self.L1_AIN2, GPIO.LOW)  # AIN2
    #     GPIO.output(self.L1_AIN1, GPIO.HIGH)  # AIN1

    #     self.L2_Motor.ChangeDutyCycle(spd_l2)
    #     GPIO.output(self.L2_AIN2, GPIO.HIGH)  # AIN2
    #     GPIO.output(self.L2_AIN1, GPIO.LOW)  # AIN1

    #     self.R1_Motor.ChangeDutyCycle(spd_r1)
    #     GPIO.output(self.R1_AIN2, GPIO.HIGH)  # AIN2
    #     GPIO.output(self.R1_AIN1, GPIO.LOW)  # AIN1

    #     self.R2_Motor.ChangeDutyCycle(spd_r2)
    #     GPIO.output(self.R2_AIN2, GPIO.LOW)  # AIN2
    #     GPIO.output(self.R2_AIN1, GPIO.HIGH)  # AIN1

    #     time.sleep(t_time)

    # def t_right(self, spd_l1, spd_l2, spd_r1, spd_r2, t_time):

    #     self.L1_Motor.ChangeDutyCycle(spd_l1)
    #     GPIO.output(self.L1_AIN2, GPIO.HIGH)  # AIN2
    #     GPIO.output(self.L1_AIN1, GPIO.LOW)  # AIN1

    #     self.L2_Motor.ChangeDutyCycle(spd_l2)
    #     GPIO.output(self.L2_AIN2, GPIO.LOW)  # AIN2
    #     GPIO.output(self.L2_AIN1, GPIO.HIGH)  # AIN1

    #     self.R1_Motor.ChangeDutyCycle(spd_r1)
    #     GPIO.output(self.R1_AIN2, GPIO.LOW)  # AIN2
    #     GPIO.output(self.R1_AIN1, GPIO.HIGH)  # AIN1

    #     self.R2_Motor.ChangeDutyCycle(spd_r2)
    #     GPIO.output(self.R2_AIN2, GPIO.HIGH)  # AIN2
    #     GPIO.output(self.R2_AIN1, GPIO.LOW)  # AIN1

    #     time.sleep(t_time)

        # 执行新动作时，要重置参数

    # def reset_param(self):

    # 使用PID计算PWM输出
    def pwm_with_pid(self):

        spd_cuurent_l1, spd_cuurent_l2, spd_current_r1, spd_current_r2 = self.get_spd()

        if spd_cuurent_l1:  # 如何有反馈，则进行更新
            self.spd_temp_l1, self.spd_temp_l2, self.spd_temp_r1, self.spd_temp_r2 = spd_cuurent_l1, spd_cuurent_l2, spd_current_r1, spd_current_r2
            draw.update(y=spd_cuurent_l1)
            draw.draw_img()
            print('spd_cuurent_l1', self.spd_temp_l1)
            print('spd_cuurent_r1', self.spd_temp_r1)
            print('spd_cuurent_l1', self.spd_temp_l2)
            print('spd_cuurent_r1', self.spd_temp_r2)

        pwm_l1 = self.PID_MotorCtl_L1(self.spd_target, self.spd_temp_l1)
        pwm_l2 = self.PID_MotorCtl_L2(self.spd_target, self.spd_temp_l2)
        pwm_r1 = self.PID_MotorCtl_R1(self.spd_target, self.spd_temp_r1)
        pwm_r2 = self.PID_MotorCtl_R2(self.spd_target, self.spd_temp_r2)

        return pwm_l1, pwm_l2, pwm_r1, pwm_r2

    # 停止电机
    def stop(self):
        ser.write('#001P1500T0000!'.encode())
        ser.write('#002P1500T0000!'.encode())
        ser.write('#003P1500T0000!'.encode())
        ser.write('#004P1500T0000!'.encode())
        ser.flushInput()                 # 清空接收缓存区
        sleep(0.1) 
        GPIO.cleanup()  # 程序的最后别忘记清除所有资源

    def loop(self):
        try:

            while True:
                pwm_l1, pwm_l2, pwm_r1, pwm_r2 = self.pwm_with_pid()

                # print('pwm_l1', pwm_l1)

                self.t_up(pwm_l1, pwm_l2, pwm_r1, pwm_r2, 0.5)  # 0.5秒改变一次

        except Exception as r:
            print(r)

        finally:
            self.stop()

if __name__ == '__main__':
    d =  PID_MOTOR_4D(spd_init=0.5, spd_targe=1)
    d.setup()

    d.loop()
