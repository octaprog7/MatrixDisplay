# MAX7219
MicroPython module for work with MAX7219 led matrix 8x8 display.

Just connect your matrix display board to Arduino, ESP or any other board with MicroPython firmware.

Supply voltage display board from 4.0 to 5.0 volts! Use five wires to connect (SPI bus).

1. +VCC (Supply voltage)
2. GND
3. COPI/SDO - Controller Out, Peripheral In
4. SCK - Serial Clock
5. CS - chip select

## Connection diagram

If your microcontroller is powered by 5 volts, then you do not need a Level Shifter.
If your microcontroller is powered by 3.3 volts, then you will need (!) a Level Shifter.
Please see: https://www.raspberrypi-spy.co.uk/2018/09/using-a-level-shifter-with-the-raspberry-pi-gpio/

Warning!
The operation of a microcontroller powered by a voltage of 3.3 Volts with a matrix indicator operating from 5.0 Volts can damage the MCU!

### Arduino Nano RP2040 Connect with RP2040 Board 
    MCU board			Level Shifter		Display
    -------------------------------------------------------------------
    D13 (SCK)  board pin	LV1<->HV1	    SCK display pin
    D11 (COPI) board pin	LV2<->HV2	    DIN display pin
    D10 (CS)   board pun	LV3<->HV3	    CS display pin
    +3.3 V board pin	LV pin
    +5 V board pin		HV pin
    +5 V board pin		                        +5V display pin
    GND board pin		GND Level Shifter pin	GND display pin

Don't forget to short the SJ1 jumper on the underside of the MCU board! Please
see Nano RP2040 Connect schematic: https://content.arduino.cc/assets/ABX00053-schematics.pdf

## Upload
Upload MicroPython firmware to the NANO(ESP, etc) board, and then files: main.py, mtrx_disp.py and sensor_pack folder. 
Then open main.py in your IDE and run it.

# Pictures
## IDE
![alt text](https://github.com/octaprog7/MatrixDisplay/blob/master/ide7219.png)
## Breadboard
![alt text](https://github.com/octaprog7/MatrixDisplay/blob/master/mx7219board.jpg)

## Video
Link to video: https://www.youtube.com/watch?v=X4qcNem8NmY

