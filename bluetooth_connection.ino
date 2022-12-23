//#include <SoftwareSerial.h>

#define bt_tx_pin 4 
#define bt_rx_pin 6 

SoftwareSerial bt_serial(bt_rx_pin, bt_tx_pin);

void setup()
{
    pinMode(bt_rx_pin, INPUT);
    pinMode(bt_tx_pin, OUTPUT);
    pinMode(bt_en_pin, OUTPUT);
    pinMode(bt_state_pin, OUTPUT);

    Serial.begin(9600);
    bt_serial.begin(38400);
}

void loop()
{

    if (bt_serial.available())
    {
        Serial.write(bt_serial.read());
    }

    if (Serial.available())
    {
        bt_serial.write(Serial.read());
    }
}
