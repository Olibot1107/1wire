import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.002

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)

def send_byte(byte):
    for _ in range(3):
        GPIO.output(DATA_PIN, 1)
        time.sleep(BIT_DELAY)
        GPIO.output(DATA_PIN, 0)
        time.sleep(BIT_DELAY)
    
    GPIO.output(DATA_PIN, 1)
    time.sleep(BIT_DELAY)
    
    for i in range(8):
        GPIO.output(DATA_PIN, (byte >> i) & 1)
        time.sleep(BIT_DELAY)
    
    GPIO.output(DATA_PIN, 0)
    time.sleep(BIT_DELAY * 2)

# Send known test bytes
print("Sending test pattern...")
send_byte(ord('A'))  # 65 = 0b01000001
send_byte(0)
print("Sent: A (bits should be [1,0,0,0,0,0,1,0])")

GPIO.cleanup()