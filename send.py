import RPi.GPIO as GPIO
import time

DATA_PIN = 17  # Physical pin 11
BIT_DELAY = 0.000005  # 5µs = 200 kbps! Start here, can go faster

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)  # idle LOW

def send_byte(byte):
    # START BIT
    GPIO.output(DATA_PIN, 1)
    time.sleep(BIT_DELAY)
    
    # 8 data bits, LSB first
    for i in range(8):
        GPIO.output(DATA_PIN, (byte >> i) & 1)
        time.sleep(BIT_DELAY)
    
    # STOP BIT
    GPIO.output(DATA_PIN, 0)
    time.sleep(BIT_DELAY)

def send_string(s):
    for c in s:
        send_byte(ord(c))
    send_byte(0)  # null terminator

print("Sender ready (GPIO 17)")
try:
    while True:
        msg = input("Send: ")
        send_string(msg)
        print(f"✓ Sent: {msg}")
except KeyboardInterrupt:
    GPIO.cleanup()