
String Start;
String Stop;
String Steps;
String Dwell_Time;

float A;
float B;
float t;
int s;

String Mode;
String incomingByte; // for incoming serial data
String a;
String digit;
String b;
String output;
String d=", ";
int pin[38]={3,2,7,6,5,4,11,10,9,8,25,24,23,22,29,28,27,26,33,32,31,30,37,36,35,34,41,40,39,38,45,44,43,42,49,48,47,46};
int PWMpin = 12;
int pw;
String power;
int m=0;
int n=5;
String freq;
int ard;
int str;

char user_input;

void setup() {
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    attachInterrupt(2,single_sweep,RISING);
    Serial.println("Arduino Initialized!");
}

void loop() {
  while(Serial.available()>0){
    Start=Serial.readStringUntil('#');
    Stop=Serial.readStringUntil('#');
    Steps=Serial.readStringUntil('#');
    Dwell_Time=Serial.readStringUntil('#');

    //single_sweep();
  }
}


void single_sweep() {    
    A=Start.toFloat();
    B=Stop.toFloat();
    s=Steps.toInt();
    t=Dwell_Time.toFloat();
    
    String c[s+2];
    for (int k=0;k<s+2;k++){
         freq=String((k-2)*(B-A)/(s-1) + A);
         //Serial.println(freq);
         incomingByte = freq;
         a="";b="";output="";

         for (int i=0;i<10;i++){
              digit = String(incomingByte[i]);
              //Serial.println(digit);
              a=String(digit.toInt(),BIN);
              if (a.length()==3){
                  a=String(0,BIN)+a;}
              if (a.length()==2){
                  a=String(0,BIN)+String(0,BIN)+a;}
              if (a.length()==  1){
                  a=String(0,BIN)+String(0,BIN)+String(0,BIN)+a;}
               b+=a;
              }
              
         c[k]=b;
    }
     for (int k=0;k<s+2;k++){
         for (int i=0;i<38;i++){
              if (c[k][i+2]=='0'){digitalWrite(pin[i],HIGH);}
              else{digitalWrite(pin[i],LOW);}
             }
         digitalWrite(13,HIGH);
         delayMicroseconds(1000*t/2);
         digitalWrite(13,LOW);
         delayMicroseconds(1000*t/2 - 321);

     }

}


            


