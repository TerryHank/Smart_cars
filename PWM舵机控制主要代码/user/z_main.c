/****************************************************************************
	*	@笔者	：	W
	*	@日期	：	2019年12月03日
	*	@所属	：	杭州众灵科技
	*	@论坛	：	www.ZL-robot.com
	*	@功能	：	ZL-KPZ控制板（32版）模块例程例程8————PWM舵机控制
	*	@函数列表:
	*	1.	void main(void) -- 主函数
 ****************************************************************************/

#include "z_main.h"

/*******全局变量定义*******/
u8 i=0;
servo_data_t servo_data[SERVO_NUM];
u8 servo_index;

int main(void) {																																																																																																																															//ZL
	setup_systick();	//初始化滴答时钟，1S增加一次systick_ms的值
	setup_key();			//初始化按键
	setup_servo();		//初始化舵机相关设置

	while (1) {
		loop_key();			//循环检测按键状态
		loop_servo();		//循环处理舵机的指令
	}
}
