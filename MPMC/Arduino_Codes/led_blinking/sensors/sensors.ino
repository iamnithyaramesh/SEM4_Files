#define ledPin 6
#define sensorPin 13

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
  pinMode(sensorPin,INPUT);
  digitalWrite(ledPin,LOW);
  

}

void loop() {
  Serial.print('Analog output');
  Serial.analogWrite(readsensor());
  delay(200);

  // put your main code here, to run repeatedly:

}

int readsensor(){int sensorValue=analogRead(sensorPin);
int outputValue=map(sensorValue,0,1023,255,0);
analogWrite(ledPin,outputValue);
return outputValue;

const int pingPin=6;
const int echoPin=7;

void setup(){
  Serial.begin(9600);
}
  
void loop(){
  pinMode(pingPin,OUTPUT);
  digitalWrite(pingPin,LOW);
  delay(2);
  digitalWrite(pingPin,HIGH);
  delay(10);
  digitalWrite(pingPin,LOW);
  pinMode(echoPin,INPUT);
  duration=pulseIn(echoPin,HIGH);
  sensorValue=microsecondstoInches(long duration);
  Serial.println(sensorValue);
  delay(100);

long microsecondstoInches(long microseconds){
  return microseconds/74/2;
  
}
  
  
const int pir=7;

void setup(){
  pinMode(pir,INPUT);
  Serial.begin(9600);
  delay(2000);
}

void loop(){
  int status=digitalRead(pir,HIGH);

  if (status==HIGH);{
      Serial.println('Motion detected');}
  else
      {Serial.println('No motion');}
  
    
}
  
}


int obstaclePin=9;
int hasobstacle=LOW
void setup(){
  pinMode(obstaclePin,INPUT);
  Serial.begin(9600);
}

void loop(){int hasobstacle=digitalRead(obstaclePin,HIGH);

if (hasobstacle==HIGH);{
  Serial.println('Obstacle detected');}
else{Serial.prinln('Nothing found');}

  
}

}
  
}
