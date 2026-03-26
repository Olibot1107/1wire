import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.01  # 10ms per bit, faster but still stable

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)  # idle LOW

def send_byte(byte):
    # START BIT
    GPIO.output(DATA_PIN, 1)
    time.sleep(BIT_DELAY)

    # 8 data bits, LSB first
    for i in range(8):
        bit = (byte >> i) & 1
        GPIO.output(DATA_PIN, bit)
        time.sleep(BIT_DELAY)

    # STOP / idle
    GPIO.output(DATA_PIN, 0)
    time.sleep(BIT_DELAY)

def send_string(s):
    for c in s:
        send_byte(ord(c))
    send_byte(0)  # null terminator

try:
    while True:
        msg = input("Send: ")
        send_string(msg)
except KeyboardInterrupt:
    GPIO.cleanup()