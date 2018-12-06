// #define STOP 0             // 0  0
// #define FORWARD 1          // 1  1
// #define BACKWARD 2         //-1 -1
// #define TURNLEFT 3         // 0  1
// #define TURNRIGHT 4        // 1  0
// #define ROTATELEFT 5       // 0 -1
// #define ROTATERIGHT 6      //-1  0
// #define SPINCLOCK 7        // 1 -1
// #define SPINCOUNTERCLOCK 8 //-1  1

#define STOP 48             //30h       // 0  0
#define FORWARD 49          //31h       // 1  1
#define BACKWARD 50         //32h       //-1 -1
#define TURNLEFT 51         //33h       // 0  1
#define TURNRIGHT 52        //34h       // 1  0
#define ROTATELEFT 53       //35h       // 0 -1
#define ROTATERIGHT 54      //36h       //-1  0
#define SPINCLOCK 55        //37h       // 1 -1
#define SPINCOUNTERCLOCK 56 //38h       //-1  1

const int LeftMotorBack = 8;
const int LeftMotorGo = 9;
const int RightMotorGo = 10;
const int RightMotorBack = 11;

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(LeftMotorGo, OUTPUT);
    pinMode(LeftMotorBack, OUTPUT);
    pinMode(RightMotorGo, OUTPUT);
    pinMode(RightMotorBack, OUTPUT);
}

void loop()
{
    // put your main code here, to run repeatedly:
    //usart read
    if (Serial.available() > 0)
    {
        int cmd = Serial.read(); //读取蓝牙模块发送到串口的数据
        Serial.println(cmd);
        motorRun(cmd);
    }
}

void motorRun(int cmd)
{
    switch (cmd)
    {
    case FORWARD:
        //1 1 左轮和右轮都前进
        Serial.println("FORWARD"); //输出状态
        digitalWrite(LeftMotorGo, HIGH);
        digitalWrite(LeftMotorBack, LOW);
        digitalWrite(RightMotorGo, HIGH);
        digitalWrite(RightMotorBack, LOW);
        break;
    case BACKWARD:
        //-1 -1 左轮和右轮都后退
        Serial.println("BACKWARD"); //输出状态
        digitalWrite(LeftMotorGo, LOW);
        digitalWrite(LeftMotorBack, HIGH);
        digitalWrite(RightMotorGo, LOW);
        digitalWrite(RightMotorBack, HIGH);
        break;
    case TURNLEFT:
        //0 1 左轮不动，右轮前进
        Serial.println("TURN  LEFT"); //输出状态
        digitalWrite(LeftMotorGo, LOW);
        digitalWrite(LeftMotorBack, LOW);
        digitalWrite(RightMotorGo, HIGH);
        digitalWrite(RightMotorBack, LOW);
        break;
    case TURNRIGHT:
        //1 0 左轮前进，右轮不动
        Serial.println("TURN  RIGHT"); //输出状态
        digitalWrite(LeftMotorGo, HIGH);
        digitalWrite(LeftMotorBack, LOW);
        digitalWrite(RightMotorGo, LOW);
        digitalWrite(RightMotorBack, LOW);
        break;
    case ROTATELEFT:
        //0 -1 左轮不动，右轮后退
        Serial.println("ROTATE LEFT"); //输出状态
        digitalWrite(LeftMotorGo, LOW);
        digitalWrite(LeftMotorBack, LOW);
        digitalWrite(RightMotorGo, LOW);
        digitalWrite(RightMotorBack, HIGH);
        break;
    case ROTATERIGHT:
        //-1 0 左轮后退，右轮不动
        Serial.println("ROTATE  RIGHT"); //输出状态
        digitalWrite(LeftMotorGo, LOW);
        digitalWrite(LeftMotorBack, HIGH);
        digitalWrite(RightMotorGo, LOW);
        digitalWrite(RightMotorBack, LOW);
        break;
    case SPINCLOCK:
        //1 -1 左轮前进，右轮后退
        Serial.println("SPIN CLOCKWISE"); //输出状态
        digitalWrite(LeftMotorGo, HIGH);
        digitalWrite(LeftMotorBack, LOW);
        digitalWrite(RightMotorGo, LOW);
        digitalWrite(RightMotorBack, HIGH);
        break;
    case SPINCOUNTERCLOCK:
        //-1 1 左轮后退，右轮前进
        Serial.println("SPIN COUNTERCLOCKWISE"); //输出状态
        digitalWrite(LeftMotorGo, LOW);
        digitalWrite(LeftMotorBack, HIGH);
        digitalWrite(RightMotorGo, HIGH);
        digitalWrite(RightMotorBack, LOW);
        break;
    default:
        //0 0 左轮和右轮都不动
        Serial.println("STOP"); //输出状态
        digitalWrite(LeftMotorGo, LOW);
        digitalWrite(LeftMotorBack, LOW);
        digitalWrite(RightMotorGo, LOW);
        digitalWrite(RightMotorBack, LOW);
    }
}
