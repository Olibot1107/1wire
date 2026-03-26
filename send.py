import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.0001  # 100µs per bit

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)

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
    send_byte(0)

print("Sender ready")
try:
    while True:
        msg = input("Send: ")
        if msg:
            send_string(msg)
            print(f"Sent: {msg}")
except KeyboardInterrupt:
    GPIO.cleanup()