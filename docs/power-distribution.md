
# Power Distribution & Budget Analysis

To estimate the power requirements of our embedded system, we conducted a detailed analysis of each component's current consumption to ensure that our power supply and protective elements, such as the 1.5A fuse, are appropriately rated.

Starting with the ESP32-S3 WROOM microcontroller, it typically draws approximately 23.88 mA during active operation. In deep sleep mode, the current consumption can drop to around 8.14 µA, depending on configuration and board design.

The 0.96-inch I²C OLED display's current draw is contingent on the number of pixels illuminated. Under typical usage, it consumes about 20 mA.

The 4×4 membrane keypad, particularly the mLink variant, has an idle current consumption of approximately 4.5 mA.

The AP63203WU-7 is a synchronous buck converter capable of delivering up to 2 A of continuous output current. Its quiescent current is notably low, around 22 µA, making it efficient for our application.
 
- ESP32-S3 WROOM: 23.88 mA
- OLED Display: 20 mA
- Keypad: 4.5 mA

Totaling approximately 48.38 mA. To account for potential current spikes and ensure a safety margin, we consider a peak current draw of around 100 mA.

Given that our system is protected by a 1.5A fuse, this provides ample headroom above our estimated peak current, ensuring both safety and reliability. The AP63203WU-7 regulator's capacity to handle up to 2 A further reinforces the adequacy of our power design.

In conclusion, our power budget analysis confirms that the selected components and protective measures are well-suited for the system's operational requirements, providing both efficiency and safety.
