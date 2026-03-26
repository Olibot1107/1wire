import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.002  # Start VERY slow (2ms)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)

def send_byte(byte):
    # Long preamble to help receiver sync
    for _ in range(3):
        GPIO.output(DATA_PIN, 1)
        time.sleep(BIT_DELAY)
        GPIO.output(DATA_PIN, 0)
        time.sleep(BIT_DELAY)
    
    # START BIT (always 1)
    GPIO.output(DATA_PIN, 1)
    time.sleep(BIT_DELAY)
    
    # 8 data bits LSB first
    for i in range(8):
        GPIO.output(DATA_PIN, (byte >> i) & 1)
        time.sleep(BIT_DELAY)
    
    # STOP BIT (always 0)
    GPIO.output(DATA_PIN, 0)
    time.sleep(BIT_DELAY * 2)  # Extra gap between bytes

def send_string(s):
    print(f"Sending: {repr(s)}")
    for c in s:
        send_byte(ord(c))
        print(f"  Sent: '{c}' ({ord(c)})")
    send_byte(0)
    print("  Sent: NULL (0)")

print("=== SENDER ===")
print(f"BIT_DELAY = {BIT_DELAY}")
try:
    while True:
        msg = input("\nSend: ")
        if msg:
            send_string(msg)
except KeyboardInterrupt:
    GPIO.cleanup()