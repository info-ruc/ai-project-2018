/*
    智能小车超声波避障实验
*/

const int Echo = A1; // Echo 回声脚(P2.0)
const int Trig = A0; // Trig 触发脚(P2.1)

int Distance;

const int Left_motor_go = 8;   //左电机前进(IN1)
const int Left_motor_back = 9; //左电机后退(IN2)

const int Right_motor_go = 10;   // 右电机前进(IN3)
const int Right_motor_back = 11; // 右电机后退(IN4)

const int key = A2;  //定义按键 A2 接口
const int beep = A3; //定义蜂鸣器 A3 接口

void setup()
{
    Serial.begin(9600); // 初始化串口
    //初始化电机驱动IO为输出方式
    pinMode(Left_motor_go, OUTPUT);    // PIN 8 (PWM)
    pinMode(Left_motor_back, OUTPUT);  // PIN 9 (PWM)
    pinMode(Right_motor_go, OUTPUT);   // PIN 10 (PWM)
    pinMode(Right_motor_back, OUTPUT); // PIN 11 (PWM)
    pinMode(key, INPUT);               //定义按键接口为输入接口
    pinMode(beep, OUTPUT);
    //初始化超声波引脚
    pinMode(Echo, INPUT);  // 定义超声波输入脚
    pinMode(Trig, OUTPUT); // 定义超声波输出脚
}
/**************    智能小车的基本动作   *************/

void run()
{                                       // 前进
    digitalWrite(Right_motor_go, HIGH); // 右电机前进
    digitalWrite(Right_motor_back, LOW);
    analogWrite(Right_motor_go, 150); //0~255调速，左右轮差异略增减
    analogWrite(Right_motor_back, 0);
    digitalWrite(Left_motor_go, LOW); // 左电机前进
    digitalWrite(Left_motor_back, HIGH);
    analogWrite(Left_motor_go, 0); //PWM比例0~255调速，左右轮差异略增减
    analogWrite(Left_motor_back, 150);
}

void brake(int time)
{ //刹车，停车
    digitalWrite(Right_motor_go, LOW);
    digitalWrite(Right_motor_back, LOW);
    digitalWrite(Left_motor_go, LOW);
    digitalWrite(Left_motor_back, LOW);
    delay(time * 100); //执行时间，可以调整
}

//左转(左轮不动，右轮前进)
void left()
{
    digitalWrite(Right_motor_go, HIGH); // 右电机前进
    digitalWrite(Right_motor_back, LOW);
    analogWrite(Right_motor_go, 200);
    analogWrite(Right_motor_back, 0); //PWM比例0~255调速
    digitalWrite(Left_motor_go, LOW); //左轮后退
    digitalWrite(Left_motor_back, LOW);
    analogWrite(Left_motor_go, 0);
    analogWrite(Left_motor_back, 0); //PWM比例0~255调速
    //delay(time * 100);	//执行时间，可以调整
}

//左转(左轮后退，右轮前进)
void spin_left(int time)
{
    digitalWrite(Right_motor_go, HIGH); // 右电机前进
    digitalWrite(Right_motor_back, LOW);
    analogWrite(Right_motor_go, 200);
    analogWrite(Right_motor_back, 0);  //PWM比例0~255调速
    digitalWrite(Left_motor_go, HIGH); //左轮后退
    digitalWrite(Left_motor_back, LOW);
    analogWrite(Left_motor_go, 200);
    analogWrite(Left_motor_back, 0); //PWM比例0~255调速
    delay(time * 100);               //执行时间，可以调整
}

void right(int time)
{
    digitalWrite(Right_motor_go, LOW); //右电机后退
    digitalWrite(Right_motor_back, LOW);
    analogWrite(Right_motor_go, 0);
    analogWrite(Right_motor_back, 0); //PWM比例0~255调速
    digitalWrite(Left_motor_go, LOW); //左电机前进
    digitalWrite(Left_motor_back, HIGH);
    analogWrite(Left_motor_go, 0);
    analogWrite(Left_motor_back, 150); //PWM比例0~255调速
    delay(time * 100);                 //执行时间，可以调整
}

//右转(右轮后退，左轮前进)
void spin_right(int time)
{
    digitalWrite(Right_motor_go, LOW); //右电机后退
    digitalWrite(Right_motor_back, HIGH);
    analogWrite(Right_motor_go, 0);
    analogWrite(Right_motor_back, 200); //PWM比例0~255调速
    digitalWrite(Left_motor_go, LOW);   //左电机前进
    digitalWrite(Left_motor_back, HIGH);
    analogWrite(Left_motor_go, 0);
    analogWrite(Left_motor_back, 200); //PWM比例0~255调速
    delay(time * 100);                 //执行时间，可以调整
}

//后退
void back(int time)
{
    digitalWrite(Right_motor_go, LOW); //右轮后退
    digitalWrite(Right_motor_back, HIGH);
    analogWrite(Right_motor_go, 0);
    analogWrite(Right_motor_back, 200); //PWM比例0~255调速
    digitalWrite(Left_motor_go, HIGH);  //左轮后退
    digitalWrite(Left_motor_back, LOW);
    analogWrite(Left_motor_go, 200);
    analogWrite(Left_motor_back, 0); //PWM比例0~255调速
    delay(time * 100);               //执行时间，可以调整
}

//按键扫描
void keysacn()
{
    int val;
    val = digitalRead(key);   //读取数字7 口电平值赋给val
    while (!digitalRead(key)) //当按键没被按下时，一直循环
    {
        val = digitalRead(key); //此句可省略，可让循环跑空
    }
    while (digitalRead(key)) //当按键被按下时
    {
        delay(10);              //延时10ms
        val = digitalRead(key); //读取数字7 口电平值赋给val
        if (val == HIGH)        //第二次判断按键是否被按下
        {
            digitalWrite(beep, HIGH);    //蜂鸣器响
            while (!digitalRead(key))    //判断按键是否被松开
                digitalWrite(beep, LOW); //蜂鸣器停止
        }
        else
            digitalWrite(beep, LOW); //蜂鸣器停止
    }
}

float Distance_test() // 测量小车前方最近障碍物的距离
{
    digitalWrite(Trig, LOW); // 给触发脚低电平2μs
    delayMicroseconds(2);
    digitalWrite(Trig, HIGH); // 给触发脚高电平10μs
    delayMicroseconds(10);
    digitalWrite(Trig, LOW);  // 持续给触发脚低电
    float Total_time = pulseIn(Echo, HIGH);     // 读取回声脚接收到高电平的总时间(单位：微秒)。
    float Actual_distance = Total_time / 58;    // 计算实际障碍物的距离（单位：厘米）。
    Serial.print("Distance:");       //输出距离（单位：厘米）。
    Serial.print(Actual_distance);   //显示距离（单位：厘米）。
    return Actual_distance;
}

void loop()
{
    keysacn(); //调用按键扫描函数，当按键没被按下时处于忙等待状态；当按键被按下时，跳出死循环开始超声波避障。
    while (1)
    {
        Distance = Distance_test(); //调用测距函数测量前方最近障碍物的距离
        if (Distance < 10)          //当前方的障碍物的距离小于某个阈值时，开始后退并向右转一个角度
        {
            back(2);
            right(1);                 //右转
            digitalWrite(beep, HIGH); //蜂鸣器响起
            brake(1);                 //停车
        }
        else
        {
            run(); //无障碍物，直行
            digitalWrite(beep, LOW);
        }
    }
}
