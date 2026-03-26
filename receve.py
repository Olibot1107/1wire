import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.0001  # MUST match sender exactly!

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_byte():
    # Wait for start bit (LOW to HIGH)
    while GPIO.input(DATA_PIN) == 0:
        pass
    
    # KEY FIX: Wait exactly 1.5 bit periods to center on first data bit
    time.sleep(BIT_DELAY * 1.5)
    
    value = 0
    for i in range(8):
        bit = GPIO.input(DATA_PIN)
        value |= (bit << i)
        time.sleep(BIT_DELAY)  # Move to next bit
    
    # Wait for stop bit
    time.sleep(BIT_DELAY)
    
    return value

def read_string():
    s = ""
    while True:
        byte = read_byte()
        if byte == 0:
            break
        if 32 <= byte < 127:  # Printable ASCII only
            s += chr(byte)
        else:
            s += f"[{byte}]"  # Show non-printable as number
    return s

print("Receiver listening...")
try:
    while True:
        msg = read_string()
        print(f"Received: {msg}")
except KeyboardInterrupt:
    GPIO.cleanup()