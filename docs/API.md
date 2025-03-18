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

| Start Bytes | Sender | Broadcast | Message type | Wind speed | Temperature | Humidity | Pressure | Stop Bytes |
|---|---|---|---|---|---|---|---|---|
0x41 0x5A | 0x02 (Sender) | 0xFF (Broadcast) | 0x01 | 30 00 | 25 00 | 60 00 | 1013 00 | 0x59 0x42


### Handling a Message Sent to the Wrong System or Unrecognized Data

1. **0x41 0x5A** - Start bytes
2. ***0x04** - Motor Controller is the sender
3. **0x02** - ESP32 (HMI) is the recipient
4. **0x99** - Unknown message type (Invalid Command)
5. **AA BB CC DD EE** - Random unknown data
6. **0x59 | 0x42** - Stop bytes


### Invalid Character Received & Error Handling

---
1.   **0x41 0x5A** → Start Byte  
2. **0x02** → ESP32
3. **0x03** → Weather Sensor
4. **0x05** → "CORRUPTED MESSAGE: RESEND"
5. **0x59 0x42** → End Byte
---

1. 0x41 0x3F → First start byte is correct (0x41), but second start byte is incorrect (0x3F instead of 0x5A)
2. The ESP32 detects corruption and ignores the message.

#### What happens?

1. The ESP32 sets CTS (Clear-To-Send) HIGH to request retransmission from the sender.
2. It does not process or display the corrupted data.

