import RPi.GPIO as GPIO
import time

DATA_PIN = 17  # Physical pin 11
BIT_DELAY = 0.000005  # Must match sender EXACTLY!

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_byte():
    # Wait for start bit (LOW → HIGH transition)
    while GPIO.input(DATA_PIN) == 0:
        pass
    
    time.sleep(BIT_DELAY * 1.5)  # Jump to middle of first data bit
    
    value = 0
    for i in range(8):
        if GPIO.input(DATA_PIN):
            value |= (1 << i)
        time.sleep(BIT_DELAY)
    
    time.sleep(BIT_DELAY)  # Skip stop bit
    return value

def read_string():
    s = ""
    while True:
        byte = read_byte()
        if byte == 0:
            break
        s += chr(byte)
    return s

print("Receiver listening (GPIO 17)...")
try:
    while True:
        msg = read_string()
        print(f"📩 Received: {msg}")
except KeyboardInterrupt:
    GPIO.cleanup()