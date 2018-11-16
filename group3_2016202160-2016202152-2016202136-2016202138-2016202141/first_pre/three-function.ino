#include <SoftwareSerial.h> // 软件串口 for blue tooth


#define BUTTON   A2 //按键 数字A2接口

#define STATE1   1  //功能1-循迹
#define STATE2   2  //功能2-避障
#define STATE3   3  //功能3-蓝牙控制

int LED1 = 7;  //LED1 数字7 接口
int LED2 = 12; //LED2 数字12接口

char get_str;          //从蓝牙接受的字符
int  set_speed = 90;   //设置速度

int left_motor = 8;       //左电机
int left_motor_PWM = 9;   //左电机调速
int right_motor = 11;     //右电机
int right_motor_PWM = 10; //右电机调速

uint8_t run_state = 0;      //记录运动的上一个状态 0-stop     1-goForward     3-goBack
uint8_t button_state;       //记录功能的上一个选择   STATE1     STATE2          STATE3
uint8_t button_press = 0;   //记录按钮的状态       0-没有按下 1-按下按钮  

int left_track = 4;     //左循迹传感器  LOW - 有信号 - 白色区域
int right_track = 3;    //右循迹传感器  HIGH- 无信号 - 黑色区域
int ltrack_state;
int rtrack_state;

int left_avoid = 6;     //左避障传感器  LOW - 有信号 - 有障碍
int right_avoid = 5;    //右避障传感器  HIGH- 无信号 - 无障碍
int lavoid_state;
int ravoid_state;



void setup() {
	// init motor
	pinMode(left_motor, OUTPUT);
	pinMode(left_motor_PWM, OUTPUT);
	pinMode(right_motor, OUTPUT);
	pinMode(right_motor_PWM, OUTPUT);
	// init trace
	pinMode(left_track, INPUT);
	pinMode(right_track, INPUT);
	// init avoid
	pinMode(left_avoid, INPUT);
	pinMode(right_avoid, INPUT);
	
	pinMode(13, OUTPUT);
	
	Serial.begin(9600);
	//init BUTTON
	pinMode(BUTTON, INPUT_PULLUP);
	button_state = STATE1;
	//init LED
	pinMode(LED1, OUTPUT);
	pinMode(LED2, OUTPUT);
	digitalWrite(LED1, LOW);
	digitalWrite(LED2, LOW);
}


// 前进函数
void goForward() {
	digitalWrite(left_motor, LOW);
	digitalWrite(right_motor, LOW);
	
	digitalWrite(left_motor_PWM, HIGH);
	analogWrite(left_motor_PWM, set_speed);

	digitalWrite(right_motor_PWM, HIGH);
	analogWrite(right_motor_PWM, set_speed);
}
// 停止函数
void stop() {
	digitalWrite(left_motor, LOW);
	digitalWrite(right_motor, LOW);
	
	digitalWrite(left_motor_PWM, LOW);
	analogWrite(left_motor_PWM, 0);

	digitalWrite(right_motor_PWM, LOW);
	analogWrite(right_motor_PWM, 0);
}
// 左转函数
void turnLeft() {
	digitalWrite(left_motor, HIGH);
	digitalWrite(right_motor, LOW);
	
	digitalWrite(left_motor_PWM, HIGH);
	analogWrite(left_motor_PWM, set_speed);

	digitalWrite(right_motor_PWM, HIGH);
	analogWrite(right_motor_PWM, set_speed);	
}
// 右转函数
void turnRight() {
	digitalWrite(left_motor, LOW);
	digitalWrite(right_motor, HIGH);
	
	digitalWrite(left_motor_PWM, HIGH);
	analogWrite(left_motor_PWM, set_speed);

	digitalWrite(right_motor_PWM, HIGH);
	analogWrite(right_motor_PWM, set_speed);
}
// 后退函数
void goBack() {
	digitalWrite(left_motor, HIGH);
	digitalWrite(right_motor, HIGH);
	
	digitalWrite(left_motor_PWM, HIGH);
	analogWrite(left_motor_PWM, set_speed);

	digitalWrite(right_motor_PWM, HIGH);
	analogWrite(right_motor_PWM, set_speed);
}


// 循黑线
void trackBlackLine() {
	//读取信号
	ltrack_state = digitalRead(left_track);
	rtrack_state = digitalRead(right_track);
	
	if (ltrack_state == LOW && rtrack_state == LOW) {//白色区域
		goForward();
	}
	else if (ltrack_state == LOW && rtrack_state == HIGH) {//左白右黑
		turnRight();
	}
	else if (ltrack_state == HIGH && rtrack_state == LOW) {//左黑右白
		turnLeft();
	}
	else {//黑色区域
		stop();
	}
}


// 避障
void avoidObstacle() {
	//读取信号
	lavoid_state = digitalRead(left_avoid);
	ravoid_state = digitalRead(right_avoid);
	
	if (lavoid_state == LOW && ravoid_state == LOW) {//两边都是障碍物
		stop();
		delay(500);
		goBack();
		delay(500);
		turnLeft();
		delay(500);
	}
	else if (lavoid_state == LOW && ravoid_state == HIGH) {//左障碍右空空
		turnRight();
	}
	else if (lavoid_state == HIGH && ravoid_state == LOW) {//左空空右障碍
		turnLeft();
	}
	else {//黑色区域
		goForward();
	}
}


// 蓝牙控制
void bluetoothControl() {
	//接收字符
	get_str = Serial.read();
	
	if (get_str == 'f') {
		goForward();
		run_state = 1;
	}
	else if (get_str == 's') {
		stop();
		run_state = 0;
	}
	else if (get_str == 'b') {
		goBack();
		run_state = 3;
	}
	else if (get_str == 'l') {
		turnLeft();
		//恢复运动的上一状态
		if (run_state == 0) stop();
		else if (run_state == 1) goForward();
		else if (run_state == 3) goBack();
	}
	else if (get_str == 'r') {
		turnRight();
		//恢复运动的上一状态
		if (run_state == 0) stop();
		else if (run_state == 1) goForward();
		else if (run_state == 3) goBack();
	}
	else if (get_str == '+' && set_speed < 200) {
		set_speed = set_speed + 10;
		//恢复运动的上一状态
		if (run_state == 0) stop();
		else if (run_state == 1) goForward();
		else if (run_state == 3) goBack();		
	}
	else if (get_str == '-' && set_speed > 60) {
		set_speed = set_speed - 10;
		//恢复运动的上一状态
		if (run_state == 0) stop();
		else if (run_state == 1) goForward();
		else if (run_state == 3) goBack();
	}
} 


// 改变功能
void changeState() {
	//如果按钮没有按下 && 刚刚按下
	if ((button_press == 0) && (digitalRead(BUTTON)) == HIGH) {
		//防止重复执行
		button_press = 1;
		delay(2000);
		//切换功能状态
		if (button_state == STATE1) {
			button_state = STATE2;
		}
		else if (button_state == STATE2) {
			button_state = STATE3;
		}
		else if (button_state == STATE3) {
			button_state = STATE1;
		}
	}
	//按钮恢复
	if (digitalRead(BUTTON) == LOW) {
		button_press = 0;
	}
}


// 对应功能执行
void chooseFunction() {
	if (button_state == STATE1) {//红灯亮
		digitalWrite(LED1, HIGH);
		digitalWrite(LED2, LOW);
		trackBlackLine();
	}
	else if (button_state == STATE2) {//绿灯亮
		digitalWrite(LED1, LOW);
		digitalWrite(LED2, HIGH);
		avoidObstacle();		
	}
	else if (button_state == STATE3) {//红绿都亮
		digitalWrite(LED1, HIGH);
		digitalWrite(LED2, HIGH);
		bluetoothControl();
	}
}


void loop() {
	changeState();
	chooseFunction();
}
