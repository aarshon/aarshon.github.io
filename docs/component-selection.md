# Component Selection

## Introduction
For our embedded systems design project, we're developing an interactive weather station designed to engage K-12 students with real-time environmental data. Our goal is to create a learning experience where students can easily navigate through different weather modules- like temperature, humidity, solar power and battery status- using a simple keypad driven interface.

## Criteria

To ensure reliable operation, the HMI system requires a stable power supply, necessitating the integration of a voltage regulator. The PIC18F47Q10 microcontroller, selected for its low power consumption and direct compatibility with 5V peripherals, manages the user inputs and LCD output. The 16x2 I2C LCD is chosen for its low power usage and simple text display, while the 4x4 membrane keypad provides an efficient user interface for navigating through different data modules.  

The power system is a critical aspect of this design, as the microcontroller and peripherals require a stable 5V power supply. A linear voltage regulator (AMS1117-5.0) is selected for its low noise and ease of integration, ensuring consistent voltage to the LCD and keypad without fluctuations. The power budget analysis confirms that the selected regulator meets the current demands of the system while maintaining efficiency​.  

Additionally, the project incorporates a switching voltage regulator as part of a dedicated power supply lab requirement. This LM2575T-3.3G switching regulator is being developed to improve power efficiency, particularly for potential expansion into low-power wireless communication modules. The voltage regulator design process includes selecting appropriate inductors, capacitors, and diodes to ensure stable operation under varying load conditions​.

This systematic component selection ensures the HMI module is power-efficient, durable, and user-friendly, meeting both educational and engineering design constraints.
# Components
## Microcontroller
### Option 1
| **Option** | **Pros** | **Cons** | **Unit Cost & Link** |
| --- | --- | --- | --- |
| **PIC18F47Q10** (Final Choice)  | Low power, optimized for standalone HMI  |No WiFi/Bluetooth | $5.40 (DigiKey)(https://www.digikey.com/en/products/detail/microchip-technology/PIC18F47Q10-I-P/10187785)
| |  Supports I2C for LCD and GPIO for Keypad |Limited RAM compared to ESP32
| | Reliable MPLAB XC8 & MCC support  |
| | 5V operation (compatible with LCD & keypad)|

### Option 2
| **Option** | **Pros** | **Cons** | **Unit Cost & Link** |
| --- | --- | --- | --- |
| **PIC18F45K50**   | USB support  |Lacks built-in MCC Harmony compatibility | $6.40 (DigiKey)(https://www.digikey.com/en/products/detail/microchip-technology/PIC18F45K50-I-PT/3671506)
| |   More ADC channels   |May require more external circuitry
| | Slightly cheaper than PIC18F47Q10  |

### Option 3
| **Option** | **Pros** | **Cons** | **Unit Cost & Link** |
| --- | --- | --- | --- |
|    **ESP32-S3-WROOM-1**   | Built-in WiFi/Bluetooth  |3.3V logic (incompatible with some peripherals) | $3.40 (DigiKey)(https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3-WROOM-1-N8/15200089)
| |   Faster CPU & more RAM   |Higher power consumption
| | Integrated hardware acceleration  | More complex firmware development

## Final Selection: PIC18F47Q10
#### Rationale:

- Low power operation suitable for an HMI system.
- 5V compatibility ensures direct connection with LCD and keypad.
- Sufficient GPIO and I2C support for efficient module control.
- Microchip MCC integration simplifies firmware development.

## Keypad Selection:
The keypad serves as the primary navigation and input interface for the HMI.
### Option 1
| **Option** | **Pros** | **Cons** | **Unit Cost & Link** |
| --- | --- | --- | --- |
| **Membrane 4x4 Keypad** (Final Choice)  | Thin, lightweight, flexible  |Less tactile feedback | $5.95 (DigiKey)(https://www.digikey.com/en/products/detail/adafruit-industries-llc/3844/9561536)
|**Part Number:** 1528-2672-ND |  Easy to mount on an enclosure |Can wear out over time
| | Low power consumption  |

### Option 2
| **Option** | **Pros** | **Cons** | **Unit Cost & Link** |
| --- | --- | --- | --- |
| **SWITCH JOYSTICK ANALOG 50V**   | Switch is small, making it ideal for compact PCB layouts and space-constrained applications.  |Typically rated for low current (e.g., 50mA–500mA), which may not be suitable for switching higher-power loads directly.  | $2.96 (DigiKey)(https://www.digikey.com/en/products/detail/c-k/THB001P/11687191)
|**Part Number:** 108-THB001P-ND |  Provides a clear, tactile response for button presses. |It will eventually degrade over time with heavy usage.
| | Suitable for frequent use in embedded systems.  | Requires external components (e.g., pull-down resistors or debouncing circuits) 

### Option 3
| **Option** | **Pros** | **Cons** | **Unit Cost & Link** |
| --- | --- | --- | --- |
| **Tactile Pushbutton Array (Custom)**   | Fully customizable button layout  |Requires additional wiring and PCB routing | $5.95 (DigiKey)(https://www.digikey.com/en/products/detail/e-switch/TL3315NF160Q/1870395)
|**Part Number:** TL3315NF160Q |  Strong feedback |Can increase PCB complexity

## Final Selection: Membrane 4x4 Keypad
### Rationale:

- Low power consumption is ideal for embedded applications.
- Compact & lightweight for HMI panel mounting.
- Easier integration using GPIO-based matrix scanning.

## Conclusion
Summarize the document here.
```


