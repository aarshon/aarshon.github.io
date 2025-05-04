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

**Description:** This message is sent from the HMI ('a') to other subsystems like Alex ('c'), Ian ('i'), or KD ('k') to trigger a specific action. The command_code defines the type of command (e.g., up, down, setpoint), and command_value provides any numeric parameter associated with the command.

- ##### Display Update Request:
**(Msg_type = '3') to: Self (Aarshon: 'a')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example      |
-------- |-----------|--------   |--------| ---- | ------       | 
1        | msg_type           | `char`     |  `3` | `3`     | `3`    | 
2-58     | display_msg       | `char[57]`  |  `1` | `57`   | `hello user` |

**Description:** Sent by the HMI to itself ('a'), this message requests a string be shown on the display. It can be used to confirm a command, show sensor status, or provide user feedback.

### B. Message the HMI Receives:

- ##### Sensor Broadcast: 

**(Msg_type = '1'): From: Ian('i), Broadcast('X')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example         |
-------- |-----------|--------   |--------| ---- | ------          | 
1   | msg_type        | `char`     |  `1` | `1`     | `1`          | 
2   | sensor_num      | `uint8_t`  |  `1` | `4`   | `3 = Humidity` |
3-4 | sensor_val      | `uint16_t` |  `0` | `1300` | `45`          |

**Description:** Sent from Ian’s sensor subsystem ('i') or as a broadcast ('X'), this message contains a sensor number and a corresponding value. The HMI reads this data and may display it or log it.

- ##### Subsystem Error Code:

**(Msg_Type = '4'), From: Alex ('c'), Ian ('i'), KD ('k) or Broadcast ('X')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example                |
-------- |-----------|--------   |--------| ---- | ------                 | 
1        | msg_type           | `char`     |  `4`| `4`   | `4`            | 
2        | display_msg        | `uint8_t`  |  `0` | `5`  | `1 = Overload` |

**Description:** Used by any subsystem to indicate a known error condition via a numeric code. The HMI will display or log the error based on the err_code received.

- ##### Subsystem Error Message:

**(Msg_Type = '5'), From: Alex ('c'), Ian ('i'), KD ('k) or Broadcast ('X')**

Byte(s)  | Variable  | Data Type | Min    |  Max | Example                |
-------- |-----------|--------   |--------| ---- | ------                 | 
1        | msg_type  | `char`     |  `5`| `5`   | `5`            | 
2-58     | err-msg  | `char[57]`    | `1`   | `57`   | `Sensor 1 Read Error` |

**Description:** This message communicates a descriptive error string (up to 57 characters). It provides a human-readable reason for system faults (e.g., “sensor 1 read error”) that the HMI can show or log.


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
