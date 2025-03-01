
# Power Distribution , I2C Allocation & Budget Analysis

### Power Input (12 V/15 A source):
The HMI board draws only a fraction of the 15 A available. The generous adapter rating ensures plenty of headroom – the adapter will run well below its capacity, which is beneficial for thermal and reliability reasons. The main consumers on the HMI board are the PIC microcontroller, the LCD, and the backlight (and any small current from the keypad pull-ups or indicator LEDs). The PIC18F47Q10 at 3.3 V/64 MHz typically draws about ~5–15 mA in active operation (plus any current on its I/O pins, which is minimal for logic signals). The EA DOGM204W-A LCD controller (SSD1803A) is very low-power, drawing approximately 250 µA in full operation (not including backlight)

If the LCD uses a backlight, that can be a larger contributor – for example, a white LED backlight on this display might consume up to 30 mA at 3.3 V (with appropriate resistor for ~2.1 V LED drop). The 4×4 keypad is passive and consumes essentially 0 mA except during key scans; even then, current flows only briefly through the internal pull-ups and a pressed switch (a few hundreds of µA per keypress). Thus, under normal conditions, the total 3.3 V load current is on the order of <50 mA (PIC + LCD logic) without backlight, or ~50–80 mA with backlight on. This translates to a power draw of roughly 0.165–0.26 W from the 3.3 V rail. 

### Buck Regulator (AP63203) Performance:
With an output of 3.3 V at (say) 80 mA, the AP63203 will draw about
24mA from the 24V supply (we're assuming 90% efficiency at light load). This is a very light load for both the regulator and the adapter thus I am not really worried about enocuntering with any issues with the buck regulator as well.
##

Overall, the power budget is well within safe limits. The regulator and supply have plenty of overhead. All components operate in their linear range without stressing. The board’s 3.3 V rail is rock solid for the MCU and peripherals, and the 12 V distribution is capable of supplying other modules in the weather station (for example, a rain gauge or wind motor, if connected, up to the adapter’s limit). Thermal imaging of the board at full load (with backlight and a dummy 500 mA load on 3.3 V) showed only the regulator warm (~40 °C) and no hotspots on traces. Thus, from a power perspective, the design is robust and reliable for long-term operation.

# I²C Device Address Table

| **I²C Device** | **7-bit Address** | **Notes** | 
| --- | --- | --- | 
| **EA DOGM204W-A LCD (SSD1803A controller)**   | 0x3C or 0x3D   |The device internally responds to write commands at this address for text data and commands.| 


****** more to be added here ***

## 4x4 Keypad:
 We know that the keypad is not an I²C device and thus has no I²C address. It uses direct GPIO pins. here we connect the keypad directly to the PIC GPIO, eliminating our need for an address!
 
