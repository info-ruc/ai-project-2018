#include <TraceApp.h>//物体识别库
int Left_motor=8;     //左电机(IN3) 输出0  前进   输出1 后退
int Left_motor_pwm=9;     //左电机PWM调速
int Right_motor_pwm=10;    // 右电机PWM调速
int Right_motor=11;    // 右电机后退(IN1)  输出0  前进   输出1 后退

TraceApp obj(Serial, 9600); //蓝牙和电脑串口波特率（物体识别专用）
void setup() {
  obj.begin(); //初始化,注意:后面不需要再用Serial.begin()!

  pinMode(Left_motor,OUTPUT); // PIN 8 8脚无PWM功能
  pinMode(Left_motor_pwm,OUTPUT); // PIN 9 (PWM)
  pinMode(Right_motor_pwm,OUTPUT);// PIN 10 (PWM) 
  pinMode(Right_motor,OUTPUT);// PIN 11 (PWM)
}




/********前进子函数**************/
void  run(int PWM_L,int PWM_R)                         
{ 
   digitalWrite(Right_motor,LOW);  // 右电机前进
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机前进     
  analogWrite(Right_motor_pwm,PWM_R);//PWM比例0~255调速，左右轮差异略增减
  
  
  digitalWrite(Left_motor,LOW);  // 左电机前进
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,PWM_L);//PWM比例0~255调速，左右轮差异略增减
}

/********后退函数**************/
void  back(int PWM_L,int PWM_R)                    
{ 
   digitalWrite(Right_motor,HIGH);  // 右电机后退
  digitalWrite(Right_motor_pwm,HIGH);  // 右电机前进     
  analogWrite(Right_motor_pwm,PWM_R);//PWM比例0~255调速，左右轮差异略增减
  
  
  digitalWrite(Left_motor,HIGH);  // 左电机后退
  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM     
  analogWrite(Left_motor_pwm,PWM_L);//PWM比例0~255调速，左右轮差异略增减
}

/*********停止函数**************/
void brake()                              
{  
   digitalWrite(Right_motor_pwm,HIGH);  // 右电机PWM 调速输出0      
  analogWrite(Right_motor_pwm,0);//PWM比例0~255调速，左右轮差异略增减

  digitalWrite(Left_motor_pwm,HIGH);  //左电机PWM 调速输出0          
  analogWrite(Left_motor_pwm,0);//PWM比例0~255调速，左右轮差异略增减
}






int x,y;
void follow(){
  obj.routine();//物体识别；尽可能让这一句频繁运行
  if (obj.valid())
  {
  	x=obj.getX();//x坐标
     y=obj.getY();//y坐标
    //int t=obj.getT(); //物体大小

    int yc=y-174;//y偏移差值
    int xc=x-124;//x偏移差值
    
    xc=abs(xc);//x差值绝对值
    yc=abs(yc);//t差值绝对值
    int big_pwm=0;
	int small_pwm=0;
    big_pwm=yc*2+xc*1.7;//较大的pwm   
    small_pwm=yc*2-xc*1.7;//较小的pwm 
    big_pwm=constrain(big_pwm,0,180);//限制PWM
    small_pwm=constrain(small_pwm,0,180);//限制PWM
    
    if((x>70)&&(x<225)&&(y<75)){  //正前方 
    	run(150,150);
	}
	if((x>70)&&(x<225)&&(y>261)){  //正后方 
    	back(150,150);
	}
    if(x<130 && y<156){            //右上角 
    	run(big_pwm,small_pwm);
	}
	if(x>130 && y<156){           //左上角 
		run(small_pwm,big_pwm);
	}
	if(x<130 && y>156){           //右下角 
		back(small_pwm,big_pwm);
	}
	if(x>130 && y>156){           //左下角 
		back(big_pwm,small_pwm);
	}
  }
}






void loop() {
  obj.routine();//物体识别；尽可能让这一句频繁运行
  follow();
}


