//===============================================================
//  智能小车前进实验
//===============================================================
//#include <Servo.h>
int Left_motor_go = 8;   //左电机前进(IN1)
int Left_motor_back = 9; //左电机后退(IN2)

int Right_motor_go = 10;   // 右电机前进(IN3)
int Right_motor_back = 11; // 右电机后退(IN4)

void setup()
{
    //初始化电机驱动IO为输出方式
    pinMode(Left_motor_go, OUTPUT);    // PIN 8 8脚无PWM功能
    pinMode(Left_motor_back, OUTPUT);  // PIN 9 (PWM)
    pinMode(Right_motor_go, OUTPUT);   // PIN 10 (PWM)
    pinMode(Right_motor_back, OUTPUT); // PIN 11 (PWM)
}

void run(int time) // 前进
{
    digitalWrite(Right_motor_go, HIGH); // 右电机前进
    digitalWrite(Right_motor_back, LOW);
    analogWrite(Right_motor_go, 200); //PWM比例0~255调速，左右轮差异略增减
    analogWrite(Right_motor_back, 0);
    digitalWrite(Left_motor_go, LOW); // 左电机前进
    digitalWrite(Left_motor_back, HIGH);
    analogWrite(Left_motor_go, 0); //PWM比例0~255调速，左右轮差异略增减
    analogWrite(Left_motor_back, 200);
}

void loop()
{
    delay(500);
    run(10); //前进
}