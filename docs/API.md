# API Application Programming Interface

The HMI Subsystem API enables seamless UART-based communication with other subsystems using a structured daisy-chain protocol. This ensures reliable data transmission between the ESP32-WROOM and other modules while preventing conflicts or message loss. The message structure follows a 64-byte format with defined prefixes, suffixes, sender/receiver IDs, and data payloads.

## Team Member IDs

Name    | Subsystem | Address | Char Add
--------|-----------|-------- |---------
Aarshon | HMI       | `0x61`  |  'a'
Alex    | Motor     | `0x63`  |  'c'
Ian     | Sensor    | `0x69`  |  'i'
KD      | Websocket | `0x6B`  |  'k'

Ian Sensor:  [API DATASHEET](https://tortoise6323.github.io/Tortoise6323/api/)  
Alex Motor:  [API DATASHEET](https://alex-co04.github.io/Alex_Comeaux.io/API/)  
KD MQTT:  [API DATASHEET](https://kdashora.github.io/kushagrad.github.io/API/)    



## Messages Sent and Received by HMI:

### A. Message the HMI Sends:

- ##### User Command:
**(Msg_type = '2') to: Alex ('c'), Ian ('i') or KD ('k)**


Byte(s)  | Variable  | Data Type | Min    |  Max | Example      |
-------- |-----------|--------   |--------| ---- | ------       | 
1   | msg_type           | `char`     |  `2` | `2`     | `2`    | 
2   | command_code       | `uint8_t`  |  `1` | `255`   | `1=UP` |
3-4 | command_value      | `uint16_t` |  `0` | `65535` | `100`  |

- ##### Display Update Request:
**(Msg_type = '3') to: Self (Aarshon: 'a')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example      |
-------- |-----------|--------   |--------| ---- | ------       | 
1        | msg_type           | `char`     |  `3` | `3`     | `3`    | 
2-58     | display_msg       | `char[57]`  |  `1` | `57`   | `hello user` |


### B. Message the HMI Receives:

- ##### Sensor Broadcast: 

**(Msg_type = '1'): From: Ian('i), Broadcast('X')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example         |
-------- |-----------|--------   |--------| ---- | ------          | 
1   | msg_type        | `char`     |  `1` | `1`     | `1`          | 
2   | sensor_num      | `uint8_t`  |  `1` | `4`   | `3 = Humidity` |
3-4 | sensor_val      | `uint16_t` |  `0` | `1300` | `45`          |

- ##### Subsystem Error Code:

**(Msg_Type = '4'), From: Alex ('c'), Ian ('i'), KD ('k) or Broadcast ('X')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example                |
-------- |-----------|--------   |--------| ---- | ------                 | 
1        | msg_type           | `char`     |  `4`| `4`   | `4`            | 
2        | display_msg        | `uint8_t`  |  `0` | `5`  | `1 = Overload` |

- ##### Subsystem Error Message:

**(Msg_Type = '5'), From: Alex ('c'), Ian ('i'), KD ('k) or Broadcast ('X')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example                |
-------- |-----------|--------   |--------| ---- | ------                 | 
1        | msg_type  | `char`     |  `5`| `5`   | `5`            | 
2-58     | err-msg  | `char[57]`    | `1`   | `57`   | `Sensor 1 Read Error` |

## Frame Structure Summary:

 Byte Index |           Description              | Value Example |
 -----------|------------------------------------|---------------|
 [0]        | Start Byte 1                       |      'A'      |
 [1]        | Start Byte 2                       |      'Z'      |
 [2]        | Sender ID                          |      'a'      |
 [3]        | Receiver ID                        | 'i','c',etc.  |
 [4]        | msg_type                           |  `1` - `5`    |
 [5-n]      | Data / Message / Payload           |    Varies     |
 [n+1]      | End Byte 1                         |      'Y'      |
 [n+2]      | End Byte 2                         |      'B'      | 


 # BELOW THIS IS THE OLD ONE, ONLY REFERENCE I WILL DELETE
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

Aarshon HMI :  






