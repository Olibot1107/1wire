import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.001  # 1ms per bit - very stable

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)

def send_byte(byte):
    # Sync to precise clock
    start = time.perf_counter()
    tick = 0
    
    # START BIT (1)
    GPIO.output(DATA_PIN, 1)
    tick += 1
    while time.perf_counter() < start + (tick * BIT_DELAY):
        pass
    
    # 8 DATA BITS (LSB first)
    for i in range(8):
        bit = (byte >> i) & 1
        GPIO.output(DATA_PIN, bit)
        tick += 1
        while time.perf_counter() < start + (tick * BIT_DELAY):
            pass
    
    # STOP BIT (0)
    GPIO.output(DATA_PIN, 0)
    tick += 1
    while time.perf_counter() < start + (tick * BIT_DELAY):
        pass

def send_string(s):
    print(f"Sending: '{s}'")
    for c in s:
        send_byte(ord(c))
    send_byte(0)  # NULL terminator
    time.sleep(0.1)

print("SENDER ready")
try:
    while True:
        msg = input("\nSend: ")
        if msg:
            send_string(msg)
except KeyboardInterrupt:
    GPIO.cleanup()