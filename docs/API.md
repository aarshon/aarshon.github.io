# API Application Programming Interface

The HMI Subsystem API enables seamless UART-based communication with other subsystems using a structured daisy-chain protocol. This ensures reliable data transmission between the ESP32-WROOM and other modules while preventing conflicts or message loss. The message structure follows a 64-byte format with defined prefixes, suffixes, sender/receiver IDs, and data payloads.

## UART Message Structure

| Byte #  | Field          | Description |
|---------|--------------|-------------|
| 0-1     | **0x41 0x5A** | **Start Bytes (Message Prefix)** |
| 2       | **Send ID**   | Sender’s unique subsystem ID |
| 3       | **Receive ID** | Target recipient’s subsystem ID |
| 4-61    | **Message Data** | Up to **58 bytes** of payload |
| 62-63   | **0x59 0x42** | **Stop Bytes (Message Suffix)** |


### Error Handling
If prefix bytes are corrupted, the system rejects the message and requests retransmission.
If stop bytes are missing, a timeout triggers data recovery.

## UART Message Types Table

| Type  | Description | Data Format |
|-------|----------------------------------------------|----------------|
| 0x01  | Sensor Data (wind, temp, humidity, pressure) | 4x `uint16_t` |
| 0x02  | Move Motor (motor ID, angle) | `uint8_t, uint8_t` |
| 0x03  | Set Alignment Frequency (sec) | `uint16_t` |
| 0x04  | Subsystem Status (ID, code) | `uint8_t, uint8_t` |
| 0x05  | Error Message (string) | `char[57]` |
| 0x06  | Local Weather Data (type, value) | `uint8_t, uint16_t` |

### Example Message (Sensor Data)

0x41 0x5A | 0x02 (Sender) | 0xFF (Broadcast) | 0x01 | 30 00 | 25 00 | 60 00 | 1013 00 | 0x59 0x42  
(Sensor Data: Wind = 30 km/h, Temp = 25°C, Humidity = 60%, Pressure = 1013 hPa)



