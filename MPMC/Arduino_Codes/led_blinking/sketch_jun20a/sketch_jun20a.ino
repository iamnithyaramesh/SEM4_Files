const int sensorPin 13;

void setup()
{
  Serial.begin(9600);
  pinMode(sensorPin,INPUT);
}

void loop(){
  Serial.print('Output from the sensor');
  Serial.analogWrite(readsensor());
  delay(2000);
}

int readsensor(){int sensorValue=analogRead(sensorPin);
int outputValue=sensorValue/100;
return outputValue;


const int pingPin=6;
const int echoPin=7;

void setup(){
  Serial.begin(9600);
  
}

void loop(){
  pinMode(pingPin,OUTPUT);
  digitalWrite(pingPin ,LOW);
  delay(2000);
  digitalWrite(pingPin,HIGH);
  delay(2000);
  digitialWrite(pingPin,LOW);
  pinMode(echoPin,INPUT);
  duration=pulseIn(echoPin,HIGH);
  sensorValue=microsecondstoInches(long duration);
  Serial.println(sensorValue);
  delay(1000)
  
}

long microsecondstoInches(long microseconds){
  return microseconds/74/2;
  
}

const int pirPin=7;

void setup(){
  pinMode(pir,INPUT);
  Serial.begin(9600);
  delay(2000);
}

void loop(){
  int status=digitalRead(pirPin,HIGH);
  if (status=='HIGH'){
    Serial.println('Detected');}
   else:
   {Serial.println('not detected');}
   
  }
}

int obstaclePin=9;
int hasObstacle=LOW;

void setup(){
  pinMode(obstaclePin,INPUT);
  Serial.begin(9600);
  delay(1000);
}

void loop(){int hasobstacle=digitalRead(obstaclePin,HIGH);

if (hasobstacle==HIGH);{
  Serial.println('Object detected');}
  
 else:
 {Serial.println('No object found);}
}
  
}
