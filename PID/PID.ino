/********************************************************
 * PID Controller
 ********************************************************/

#include <PID_v1.h>

#define PIN_INPUT 0
#define PIN_OUTPUT 5
#define PIN_FAN 6

//Define Variables we'll be connecting to
double Setpoint, Input, Output;
double Kp = 1, Ki = 1, Kd = 1;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
int counter;

void setup()
{
  Serial.begin(9600);  
  
  //initialize the variables
  Input = analogRead(PIN_INPUT);
  Setpoint = 90;
  counter = 0;
  
  set_pid_tunings();
  
  //wait for the lamp to cool down
  analogWrite(PIN_FAN, 200);
  while(Input > 70){
    delay(1000);
    Input = analogRead(PIN_INPUT);
    //Serial.print("Esfriando... Temperatura=");
    //Serial.println(Input);
  }
  analogWrite(PIN_FAN, 0);

  //start the fan (disturb)
  // 50 - 255
  analogWrite(PIN_FAN, 100);
  change_fan_speed();
  
  //turn the PID on
  myPID.SetMode(AUTOMATIC);
}

void loop()
{
  Input = analogRead(PIN_INPUT);
  myPID.Compute();
  analogWrite(PIN_OUTPUT, Output); //change lamp pot
  counter++;
  if(counter > 30){ //30 ~ 3s
    counter = 0;
    change_fan_speed();
  }
  print_info();
  delay(500);
}

void print_info(){
  //Serial.print("Setpoint=");
  Serial.print(",");
  Serial.print(Setpoint);
  //Serial.print(" Temperatura=");
  Serial.print(",");
  Serial.print(Input);
  //Serial.print(" PotenciaLampada=");
  Serial.print(",");
  Serial.println(Output);
}

void change_fan_speed(){
  analogWrite(PIN_FAN, random(70, 200));
}

void set_pid_tunings(){
  bool tuned = false;
  while(!tuned){
    if (Serial.available() > 0) {
      String string_received = Serial.readStringUntil('\n');
      char data[256];
      char* data_r = data;
      string_received.toCharArray(data, 255);
      Kp = String(strtok(data, ",")).toDouble();
      Ki = String(strtok(NULL, ",")).toDouble();
      Kd = String(strtok(NULL, ",")).toDouble();
      //Serial.print("Kp=");
      Serial.print(",");
      Serial.print(Kp);
      //Serial.print(" Ki=");
      Serial.print(",");
      Serial.print(Ki);
      //Serial.print(" Kd=");
      Serial.print(",");
      Serial.println(Kd);
      tuned = true;
    }
  }
  myPID.SetTunings(Kp, Ki, Kd);
}
