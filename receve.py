import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.01  # match sender

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_byte():
    # wait for start bit
    while GPIO.input(DATA_PIN) == 0:
        pass
    time.sleep(BIT_DELAY * 1.5)  # middle of first bit

    value = 0
    for i in range(8):
        bit = GPIO.input(DATA_PIN)
        value |= (bit << i)
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

print("Listening...")
try:
    while True:
        msg = read_string()
        print("Received:", msg)
except KeyboardInterrupt:
    GPIO.cleanup()