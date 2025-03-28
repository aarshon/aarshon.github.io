# API Application Programming Interface

The HMI Subsystem API enables seamless UART-based communication with other subsystems using a structured daisy-chain protocol. This ensures reliable data transmission between the ESP32-WROOM and other modules while preventing conflicts or message loss. The message structure follows a 64-byte format with defined prefixes, suffixes, sender/receiver IDs, and data payloads.

## UART Message Structure

-----

|              | Byte 1      | Byte 2         | Byte 3–4        |
|--------------|-------------|----------------|-----------------|
| **Variable** | msg_type    | command_code   | command_value   |
| **Type**     | uint8_t     | uint8_t        | uint16_t        |
| **Min Value**| 2           | 0              | 0               |
| **Max Value**| 2           | 255            | 65535           |
| **Example**  | 2           | 1              | 100             |

- **msg_type = 2** (example) means "User Command" from the HMI.
- **command_code** could represent which user action was triggered (e.g., 1 = up button, 2 = down button, 10 = new setpoint, etc.).
- **command_value** is the numeric parameter (e.g., 100 = setpoint = 100, or 45 = brightness, etc.).

----

|              | Byte 1      | Bytes 2–58         |
|--------------|-------------|--------------------|
| **Variable** | msg_type    | display_msg        |
| **Type**     | uint8_t     | char array (uint8_t) |
| **Min Value**| 3           | char[1]            |
| **Max Value**| 3           | char[57] (null-terminated) |
| **Example**  | 3           | "HELLO USER"       |

- **msg_type = 3** means a "Display Update Request."
- **display_msg** is a character array (up to 57 bytes). Could be zero-terminated if needed.

----
## Sensor Broadcast Data

|              | Byte 1      | Byte 2        | Bytes 3–4      |
|--------------|-------------|---------------|----------------|
| **Variable** | msg_type    | sensor_num    | sensor_val     |
| **Type**     | uint8_t     | uint8_t       | uint16_t       |
| **Example**  | 1           | 3 (humidity)  | 45             |

- The HMI reads **sensor_num** and **sensor_val** from the incoming packet, then updates the local display or logs the data.


## Subsystem error code

|              | Byte 1      | Byte 2     |
|--------------|-------------|------------|
| **Variable** | msg_type    | err_code   |
| **Type**     | uint8_t     | uint8_t    |
| **Example**  | 4           | 1          |

- The HMI displays or records an appropriate message (e.g., "Error Code 1: Overload").

## Subsystem error message

|              | Byte 1      | Bytes 2–58         |
|--------------|-------------|--------------------|
| **Variable** | msg_type    | err_msg            |
| **Type**     | uint8_t     | char array (uint8_t) |
| **Min Value**| 5           | char[1]            |
| **Max Value**| 5           | char[57] (null-terminated) |
| **Example**  | 5           | "sensor 1 read error" |

- The HMI might display **"sensor 1 read error"** on a local screen or beep to alert the user.

### Team Send Addresses:

Aarshon HMI : 0x07
Ian Sensor: 0x12
Alex Motor: 0x69
KD MQTT: 0x11





