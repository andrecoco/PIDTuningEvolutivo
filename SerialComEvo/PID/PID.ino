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
float volt_ref = 1.1;
int numero_medidas;
double initial_temp = 51;

void setup()
{
  analogReference(INTERNAL); //1.1V
  delay(1000);
  Serial.begin(9600);
  
  //initialize the variables
  Input = get_temp(false);
  Setpoint = 75;
  counter = 0;
  
  setup_PID();
  
  //turn the PID on
  myPID.SetMode(AUTOMATIC);
}

void loop()
{
  Input = get_temp(false);
  myPID.Compute();
  analogWrite(PIN_OUTPUT, Output); //change lamp pot
  print_info();
  delay(500);
  counter++;
  if(counter >= numero_medidas){
    setup_PID();
    counter = 0;
  }
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

void get_arduino_params(){
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
      numero_medidas = String(strtok(NULL, ",")).toInt();
      /*//Serial.print("Kp=");
      //Serial.print(",");
      Serial.print(Kp);
      //Serial.print(" Ki=");
      Serial.print(",");
      Serial.print(Ki);
      //Serial.print(" Kd=");
      Serial.print(",");
      Serial.println(Kd);*/
      tuned = true;
    }
  }
  myPID.SetTunings(Kp, Ki, Kd);
}

float get_temp(bool media_movel){
  int n_temp_read = 1;
  double sum = 0;
  double medida;
  for(int i = 0; i < n_temp_read; i++){
    sum += analogRead(PIN_INPUT);
  }
  /*if(media_movel and 1 == 0){
    temp_array[0] = temp_array[1];
    temp_array[1] = temp_array[2];
    medida = 100 * (sum/n_temp_read) * volt_ref / 1024.0;
    temp_array[2] = medida;
    return (temp_array[0] + temp_array[1] + temp_array[2])/3;
  }*/
  return  100 * (sum/n_temp_read) * volt_ref / 1024.0;
}

void setup_PID(){
  get_arduino_params();
  
  //wait for the lamp to get to initial_temp if necessary
  analogWrite(PIN_OUTPUT, 120);
  while(Input < initial_temp){
    delay(200);
    Input = get_temp(false);
    //Serial.print("Esquentando... Temperatura=");
    //Serial.println(Input);
  }
  analogWrite(PIN_OUTPUT, 0);

  //wait for the lamp to cool down if necessary
  analogWrite(PIN_FAN, 200);
  while(Input > initial_temp){
    delay(200);
    Input = get_temp(false);
    //Serial.print("Esfriando... Temperatura=");
    //Serial.println(Input);
  }
  analogWrite(PIN_FAN, 0);
  
  //start the fan (disturb)
  // 50 - 255
  analogWrite(PIN_FAN, 120);
  //change_fan_speed();
}
