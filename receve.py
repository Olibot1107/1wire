import RPi.GPIO as GPIO
import time

DATA_PIN = 17      # Wire 1
DATA_PIN_INV = 27  # Wire 2
BIT_DELAY = 0.00005  # Must match sender!

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_PIN_INV, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_bit():
    """Differential read - compares both wires"""
    a = GPIO.input(DATA_PIN)
    b = GPIO.input(DATA_PIN_INV)
    # If differential: a should be opposite of b
    # Return the dominant signal
    return 1 if a > b else 0

def read_byte():
    # Wait for start bit (DATA=1, INV=0)
    while True:
        if GPIO.input(DATA_PIN) == 1 and GPIO.input(DATA_PIN_INV) == 0:
            break
    
    time.sleep(BIT_DELAY * 1.5)  # Move to middle of first data bit
    
    value = 0
    for i in range(8):
        bit = read_bit()
        value |= (bit << i)
        time.sleep(BIT_DELAY)
    
    # Wait for stop bit
    time.sleep(BIT_DELAY)
    
    return value

def read_string():
    s = ""
    while True:
        byte = read_byte()
        if byte == 0:
            break
        s += chr(byte)
    return s

print("Receiver listening...")
try:
    while True:
        msg = read_string()
        print(f"Received: {msg}")
except KeyboardInterrupt:
    GPIO.cleanup()