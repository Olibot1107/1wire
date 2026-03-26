import RPi.GPIO as GPIO
import time

DATA_PIN = 17      # Wire 1
DATA_PIN_INV = 27  # Wire 2
BIT_DELAY = 0.00005  # 50µs = 20 kbps (tune this!)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(DATA_PIN_INV, GPIO.OUT)

# Start idle
GPIO.output(DATA_PIN, 0)
GPIO.output(DATA_PIN_INV, 0)

def send_byte(byte):
    # START BIT (both high for differential)
    GPIO.output(DATA_PIN, 1)
    GPIO.output(DATA_PIN_INV, 0)
    time.sleep(BIT_DELAY)
    
    # 8 data bits, LSB first
    for i in range(8):
        bit = (byte >> i) & 1
        GPIO.output(DATA_PIN, bit)
        GPIO.output(DATA_PIN_INV, 1 - bit)  # inverted
        time.sleep(BIT_DELAY)
    
    # STOP BIT (return to idle)
    GPIO.output(DATA_PIN, 0)
    GPIO.output(DATA_PIN_INV, 0)
    time.sleep(BIT_DELAY)

def send_string(s):
    for c in s:
        send_byte(ord(c))
    send_byte(0)  # null terminator

print("Sender ready. Type messages:")
try:
    while True:
        msg = input("Send: ")
        send_string(msg)
        print(f"Sent: {msg}")
except KeyboardInterrupt:
    GPIO.cleanup()