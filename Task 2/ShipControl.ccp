// C++ code
//
#include <Adafruit_LiquidCrystal.h>

//Time keeping
unsigned long Time = 0;
int TimeSinceIncident = -1;


int AnchorState = 0;
int isStorm = 0;
int isWrecked = 0;
int isCharibydis = 0;

Adafruit_LiquidCrystal lcd_1(0);

const int AnchorPin = 11;
const int LED_Pin = 12;
const int BuzzerPin = 2;
const int PhotoresPin  = A0;
const int UltraTrig = 6;
const int UltraEcho = 5;

// Helper function to calculate distance in centimeters; Tinkercad does not have newping library? :(
long getDistance() 
{
  digitalWrite(UltraTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(UltraTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(UltraTrig, LOW);
  
  long duration = pulseIn(UltraEcho, HIGH);
  long distanceCm = duration * 0.034 / 2; // Time of flight conversion to cm
  return distanceCm;
}





void setup()
{
  lcd_1.begin(16, 2);
  pinMode(AnchorPin, INPUT);
  pinMode(LED_Pin, OUTPUT);
  pinMode(BuzzerPin, OUTPUT);
  pinMode(PhotoresPin, INPUT);
  pinMode(UltraTrig, OUTPUT);
  pinMode(UltraEcho, INPUT);
  Serial.begin(9600);

  lcd_1.print("OPEN SEA");
  AnchorState = 0;
}

void loop()
{
  Time = millis();
  if (digitalRead(AnchorPin) == HIGH) {
    Anchor();//Toggles anchor (i.e if up -> it goes down; & vice versa)

    while (digitalRead(AnchorPin) == HIGH) {   //Wait till button released
      delay(1); 
    }

  }
  
  if (AnchorState == 0)                                 //If achor is up, checking for possible env debuffs
  {
    
    //Handling Storm
  	if (analogRead(PhotoresPin) < 927 && !(isCharibydis))
    {
    	Storm(false); //Storm is called
    }
    else if (isStorm == 1) {Storm(true);}
    
    //Handling Charibydis
    if (getDistance() < 100  &&  !(isStorm))
    {
      Serial.println(getDistance());
    	Charibydis(false);  //Charibydis is called
    }
    else if (isCharibydis == 1) {Charibydis(true);}
  }
  
  else                                                  //If achor is down, Clearing debuffs
  {
    if (isStorm == 1) {Storm(true);} //Storm is Terminated
    if (isCharibydis == 1) {Charibydis(true);} //Charibydis is Terminated 
  
  }
 
  lcd_1.setCursor(0, 0); //Reset LCD cursor
  delay(30);             // Wait for 30 millisecond(s)
}





//Anchor toggle
void Anchor()
{
	if (AnchorState == 0)
    {
      lcd_1.clear();
      lcd_1.print("ANCHOR DROPPED");
      Serial.println("ANCHOR DROPPED");
      AnchorState = 1;
    }
  else if (AnchorState == 1)
    {
      lcd_1.clear();
      lcd_1.print("OPEN SEA");
      Serial.println("OPEN SEA");
      AnchorState = 0;
    }
  	
}




void Charibydis(bool Terminate)
{
	if (Terminate)
    {
    	isCharibydis = 0;
      TimeSinceIncident = -1;
    	digitalWrite(BuzzerPin, LOW);
      
     	lcd_1.clear();
    	lcd_1.print("OPEN SEA");
    	Serial.println("OPEN SEA");      
     	return;
    }
  
  	//Ensure Charibydis State
  	isCharibydis = 1;
  	digitalWrite(BuzzerPin, HIGH);
  	if (TimeSinceIncident == -1)
    {
		  TimeSinceIncident = Time;
    }
  	
    //LCD update
  	lcd_1.clear();
    lcd_1.print("CHARYBDIS");  //Prints Charibydis again everytime, but looks good like a blinking feature so it is a feature not a bug
    Serial.println("CHARYBDIS");
  	
  	//Wreking if in storm for 5 sec	
  	if (millis() - TimeSinceIncident >= 5000)
    {
      TimeSinceIncident = -1;
    	Wreked();
    }
}




void Storm(bool Terminate)
{	
  	//Terminate Storm State
  	if (Terminate)
    {
    	isStorm = 0;
      	TimeSinceIncident = -1;
      	digitalWrite(LED_Pin, LOW);
      	
      	lcd_1.clear();
    	lcd_1.print("OPEN SEA");
    	Serial.println("OPEN SEA");      
      	return;
    }
  
  	//Ensure Storm State
  	isStorm = 1;
  
  	if (TimeSinceIncident == -1)
    {
		TimeSinceIncident = Time;
    }
  	
  	//LCD update
  	lcd_1.clear();
    lcd_1.print("STORM");  //Prints storm again everytime, printing in  the above 'if Time.. == -1' should make it not blink
    Serial.println("STORM");
  	
  	//LED blinking
  	if (Time%30 < 15)
    {
    	digitalWrite(LED_Pin, HIGH);
    }
  	else {digitalWrite(LED_Pin, LOW);}
  	
  	
  
  	//Wreking if in storm for 5 sec	
  	if (millis() - TimeSinceIncident >= 5000)
    {
      	TimeSinceIncident = -1;
    	Wreked();
    }
  
  	
  	
}



void Wreked()
{
	isWrecked  = 1;
  	lcd_1.clear();
    lcd_1.print("WREKED ");
    Serial.println("WREKED");
    digitalWrite(BuzzerPin, HIGH);
  	while (1)
    {
      digitalWrite(LED_Pin, HIGH);
      delay(15);
      digitalWrite(LED_Pin, LOW);
      delay(15);
    }
}

