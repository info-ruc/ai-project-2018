#include <LiquidCrystal.h> 
int Echo = A1;  
int Trig =A0;  

int Front_Distance = 0;
int Left_Distance = 0;
int Right_Distance = 0;

int Left_motor=8;     
int Left_motor_pwm=9;     

int Right_motor_pwm=10;   
int Right_motor=11;    

int key=A2;

const int SensorRight_2 = 5;    
const int SensorLeft_2 = 6;    

int SR_2;    
int SL_2;   


int servopin=2;
int myangle;
int pulsewidth;
int val;

void setup()
{
  Serial.begin(9600);     // 初始化串口
  //初始化电机驱动IO为输出方式
   pinMode(Left_motor,OUTPUT); 
  pinMode(Left_motor_pwm,OUTPUT); 
  pinMode(Right_motor_pwm,OUTPUT);
  pinMode(Right_motor,OUTPUT);
  pinMode(key,INPUT);
  pinMode(Echo, INPUT);    
  pinMode(Trig, OUTPUT);   
  pinMode(servopin,OUTPUT);
}

void run()     // 前进
{
  digitalWrite(Right_motor,LOW); 
  digitalWrite(Right_motor_pwm,HIGH); 
  analogWrite(Right_motor_pwm,150);
  
  digitalWrite(Left_motor,LOW);  
  digitalWrite(Left_motor_pwm,HIGH);  
  analogWrite(Left_motor_pwm,150);
}

void brake()  //刹车，停车
{
  digitalWrite(Right_motor_pwm,LOW);  
  analogWrite(Right_motor_pwm,0);

  digitalWrite(Left_motor_pwm,LOW);  
  analogWrite(Left_motor_pwm,0);
}

void left()          
{
  digitalWrite(Right_motor,LOW);  
  digitalWrite(Right_motor_pwm,HIGH);
  analogWrite(Right_motor_pwm,150);
  
  
  digitalWrite(Left_motor,LOW);  
  digitalWrite(Left_motor_pwm,LOW);
  analogWrite(Left_motor_pwm,0);
}

void spin_left(int time)       
{
  digitalWrite(Right_motor,LOW);  
  digitalWrite(Right_motor_pwm,HIGH); 
  analogWrite(Right_motor_pwm,150);
  
  digitalWrite(Left_motor,HIGH);  
  digitalWrite(Left_motor_pwm,HIGH);  
  analogWrite(Left_motor_pwm,150);
  delay(time * 100);      
}

void right()
{
  digitalWrite(Right_motor,LOW);  
  digitalWrite(Right_motor_pwm,LOW); 
  analogWrite(Right_motor_pwm,0);
  digitalWrite(Left_motor,LOW);   
  digitalWrite(Left_motor_pwm,HIGH); 
  analogWrite(Left_motor_pwm,150);
}

void spin_right(int time)    
{
   digitalWrite(Right_motor,HIGH);  
  digitalWrite(Right_motor_pwm,HIGH);
  analogWrite(Right_motor_pwm,150);
  
  
  digitalWrite(Left_motor,LOW);   
  digitalWrite(Left_motor_pwm,HIGH); 
  analogWrite(Left_motor_pwm,150);
  delay(time * 100); 
}

void back()          //后退
{
  digitalWrite(Right_motor,HIGH);  
  digitalWrite(Right_motor_pwm,HIGH);
  analogWrite(Right_motor_pwm,150);
  
  
  digitalWrite(Left_motor,HIGH);  
  digitalWrite(Left_motor_pwm,HIGH);
  analogWrite(Left_motor_pwm,150);

}


void keysacn()
{
  int val;
  val=digitalRead(key);
  while(!digitalRead(key))
  {
    val=digitalRead(key);
  }
  while(digitalRead(key))
  {
    delay(10);  
    val=digitalRead(key);
    if(val==HIGH) 
    {
      
      while(!digitalRead(key)){  
      } 
    } 
  }  
  
}

float Distance_test()   
{
  digitalWrite(Trig, LOW); 
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig, LOW); 
  float Fdistance = pulseIn(Echo, HIGH);
  Fdistance= Fdistance/58;     
  return Fdistance;
}  


void servopulse(int servopin,int myangle)
{
  pulsewidth=(myangle*11)+500;
  digitalWrite(servopin,HIGH);
  delayMicroseconds(pulsewidth);
  digitalWrite(servopin,LOW);
  delay(20-(pulsewidth*0.001));
}

void front_detection()
{
  
  for(int i=0;i<=5;i++) 
  {
    servopulse(servopin,90);
  }
  Front_Distance = Distance_test();
 
}

void left_detection()
{
  for(int i=0;i<=15;i++) 
  {
    servopulse(servopin,175);//模拟产生PWM
  }
  Left_Distance = Distance_test();
}

void right_detection()
{
  for(int i=0;i<=15;i++) 
  {
    servopulse(servopin,5);
  }
  Right_Distance = Distance_test();
}

void loop()
{
  keysacn();    
  while(1){
    
    int a = random(11,13);
    
     SR_2 = digitalRead(SensorRight_2);
    SL_2 = digitalRead(SensorLeft_2);
    if (SL_2 == HIGH && SR_2==HIGH)
      {
        run();   

      }
    else if (SL_2 == HIGH && SR_2 == LOW){// 右边探测到有障碍物，有信号返回，向左转 
         brake();
         delay(300);
         back();
         delay(400);
         left();
         delay(500); 
    }
    else if (SR_2 == HIGH && SL_2 == LOW) {//左边探测到有障碍物，有信号返回，向右转  
         brake();
         delay(300);
         back();
         delay(400);
         right();
         delay(500); 
    }
    
    else 
    {
         brake();
         delay(300);
         back();
         delay(400);
         
         if(a%2 == 0){
         left();
         delay(500); 
         }
         else{
           right();
           delay(500); 
         }
    }
      

    
    front_detection();
    if(Front_Distance < 30)
    {
      brake();
      delay(200);
      back();
      delay(200);
      brake();
      delay(200);
      left_detection();
      right_detection();
      if((Left_Distance < 30 ) &&( Right_Distance < 30 ))
        if(a%2 == 0){
           spin_left(0.7);
         }
         else{
           spin_right(0.7);
          
         }
      else if(Left_Distance > Right_Distance)
      {      
        left();
        delay(300);
        brake();
        delay(100);
      }
      else
      {
        right();
        delay(300);
        brake();
        delay(100);
      }
    }
    else
    {
      run(); 
    }
  } 
}
