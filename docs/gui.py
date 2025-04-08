###############################################
# LCD + Keypad + Multi-page UI Example (ESP32)
# MicroPython reference code
###############################################
import time
from machine import Pin, I2C, UART

# ---------- USER CONSTANTS/CONFIG ----------
# Adjust these as needed for your hardware
LCD_I2C_ADDR = 0x3D          # Example address (DOGM might be 0x3E or 0x7C)
I2C_FREQ     = 100000        # 100 kHz, some modules can do 400k, check datasheet

# For a 4x4 matrix keypad
KEYPAD_ROWS  = [19, 18, 5, 4]    # Example row pins
KEYPAD_COLS  = [23, 2, 17, 16]   # Example col pins (don’t reuse I2C pins!)
KEYPAD_MAP   = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

# UART pins (example)
# Note: The ESP32 hardware UARTs vary; double-check your device’s documentation
UART_TX_PIN = 14
UART_RX_PIN = 13
UART_BAUD   = 9600

# ---------- GLOBALS ----------
current_page = 0
last_key     = None
temp_value   = 0
humid_value  = 0
wind_speed   = 0
msg_buffer   = b''  # buffer for partial UART reads

# ---------- INIT PERIPHERALS ----------

# 1) I2C for LCD
i2c = I2C(
    1,                  # I2C bus ID (ESP32 default: 0 or 1)
    scl=Pin(22),        # SCL pin
    sda=Pin(21),        # SDA pin
    freq=I2C_FREQ
)

# 2) Setup keypad pins
row_pins = [Pin(r, Pin.IN, Pin.PULL_UP) for r in KEYPAD_ROWS]
col_pins = [Pin(c, Pin.OUT) for c in KEYPAD_COLS]

# 3) Setup UART
uart = UART(2, baudrate=UART_BAUD, tx=UART_TX_PIN, rx=UART_RX_PIN)

# ---------- HELPER FUNCTIONS ----------

def lcd_write_command(cmd):
    """
    Sends a command byte to the LCD over I2C.
    Many modules require sending a "control byte"
    before the command. For example, 0x00 might indicate 'command mode'.
    Check your LCD's datasheet.
    """
    # Adjust the control byte if needed by your LCD. This is an example:
    CONTROL_CMD = 0x00
    i2c.writeto(LCD_I2C_ADDR, bytes([CONTROL_CMD, cmd]))

def lcd_write_data(dat):
    """
    Sends a data byte to the LCD over I2C.
    Typically, a control byte of 0x40 (or similar) means 'data mode'.
    """
    CONTROL_DATA = 0x40
    i2c.writeto(LCD_I2C_ADDR, bytes([CONTROL_DATA, dat]))

def lcd_init():
    """
    Initialize the LCD display (HD44780-like sequence).
    Adjust as per your display's datasheet.
    """
    time.sleep_ms(50)  # Wait for power up
    # Example init (for typical HD44780). DOGM might differ.
    lcd_write_command(0x38)  # 8-bit, 2-line, 5x8
    time.sleep_ms(5)
    lcd_write_command(0x38)
    time.sleep_ms(5)
    lcd_write_command(0x38)
    time.sleep_ms(5)
    lcd_write_command(0x08)  # display off
    lcd_clear()
    lcd_write_command(0x06)  # entry mode: increment cursor, no shift
    lcd_write_command(0x0C)  # display on, cursor off
    time.sleep_ms(5)

def lcd_clear():
    """
    Clear display command (0x01). Wait a bit because it takes time.
    """
    lcd_write_command(0x01)
    time.sleep_ms(2)

def lcd_goto_xy(col, row):
    """
    Set DDRAM address to position cursor at (col, row).
    For a 20x4 or 16x2 HD44780-like display, addresses vary by row.
    E.g. row0 starts 0x00, row1 starts 0x40, row2 is 0x14, row3 is 0x54.
    DOGM might differ. Adjust as needed.
    """
    # Example for 20x4 or 16x2
    row_offsets = [0x00, 0x40, 0x14, 0x54]
    addr = row_offsets[row] + col
    lcd_write_command(0x80 | addr)

def lcd_puts(string):
    """
    Write an entire string at the current cursor position.
    """
    for ch in string:
        lcd_write_data(ord(ch))

def scan_keypad():
    """
    Returns the first pressed key, or None if no key is pressed.
    Simple approach: drive each column LOW, read each row for 0.
    """
    for c_idx, c_pin in enumerate(col_pins):
        # Drive one column low, others high
        for cc in col_pins:
            cc.value(1)
        c_pin.value(0)

        # Check rows
        for r_idx, r_pin in enumerate(row_pins):
            if r_pin.value() == 0:
                return KEYPAD_MAP[r_idx][c_idx]
    return None

def show_page0():
    lcd_clear()
    lcd_goto_xy(0,0)
    lcd_puts("** Weather Station **")
    lcd_goto_xy(0,1)
    lcd_puts("Press A to Next Page")

def show_page1():
    # Example: display temperature/humidity from global variables
    lcd_clear()
    lcd_goto_xy(0,0)
    lcd_puts("Temp: {}C Hum: {}%".format(temp_value, humid_value))
    lcd_goto_xy(0,1)
    lcd_puts("Press B for Next")

def show_page2():
    # Example: display wind speed
    lcd_clear()
    lcd_goto_xy(0,0)
    lcd_puts("Wind Speed: {} m/s".format(wind_speed))
    lcd_goto_xy(0,1)
    lcd_puts("Press # for Home")

pages = [show_page0, show_page1, show_page2]

def draw_current_page():
    """
    Helper to call the correct function based on current_page.
    """
    pages[current_page]()

# ---------- UART HANDLING EXAMPLE ----------
def process_uart_data(byte_data):
    """
    Example: parse incoming data from other boards
    Suppose the data structure is [MessageType, ValueLo, ValueHi]
    You’d adapt to your real protocol, using your team's spec!
    """
    global temp_value, humid_value, wind_speed
    # Example: interpret the first byte as messageType
    msg_type = byte_data[0]
    if msg_type == 0x10:
        # Temperature
        val = byte_data[1] | (byte_data[2] << 8)  # 16-bit
        temp_value = val
    elif msg_type == 0x11:
        # Humidity
        val = byte_data[1] | (byte_data[2] << 8)
        humid_value = val
    elif msg_type == 0x12:
        # Wind Speed
        val = byte_data[1] | (byte_data[2] << 8)
        wind_speed = val
    else:
        # Unknown message type
        pass

# ---------- MAIN ----------
def main():
    lcd_init()
    draw_current_page()

    global current_page, msg_buffer

    while True:
        # 1) Keypad
        key = scan_keypad()
        if key is not None:
            # Simple state machine
            if key == 'A':  # next page
                current_page = (current_page + 1) % len(pages)
                draw_current_page()
            elif key == 'B':  # next again
                current_page = (current_page + 1) % len(pages)
                draw_current_page()
            elif key == '#':  # go home
                current_page = 0
                draw_current_page()
            # Add more logic for other keys as needed

        # 2) Check UART
        if uart.any():
            # read available bytes
            incoming = uart.read()  # or .read(uart.any()) for partial
            if incoming:
                # For a simple protocol, we might accumulate in msg_buffer
                msg_buffer += incoming
                # parse
                # If your protocol is known length, parse in chunks:
                while len(msg_buffer) >= 3:  # e.g. we expect 3 bytes
                    chunk = msg_buffer[:3]
                    process_uart_data(chunk)
                    msg_buffer = msg_buffer[3:]
                # if your protocol has a bigger size or more complex framing, 
                # you’d handle that differently.

        # 3) Maybe update the display if new data arrived
        #    (For now, we only refresh on page changes. 
        #     But you could do partial updates too.)

        time.sleep_ms(100)  # small delay to avoid busy-loop

# ---------- RUN ----------
main()






