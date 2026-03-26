import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.001  # MUST match sender exactly!

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_byte():
    # Wait for start bit (0 -> 1 transition)
    timeout = time.time() + 3
    while GPIO.input(DATA_PIN) == 0:
        if time.time() > timeout:
            return None
    
    # Caught rising edge - this is our sync point
    start = time.perf_counter()
    
    # Sample in the MIDDLE of each bit
    # First data bit is at 1.5 * BIT_DELAY from start
    value = 0
    for i in range(8):
        sample_time = start + ((i + 1.5) * BIT_DELAY)
        
        # Wait until sample time
        while time.perf_counter() < sample_time:
            pass
        
        # Read bit
        if GPIO.input(DATA_PIN):
            value |= (1 << i)
    
    return value

def read_string():
    s = ""
    while True:
        byte = read_byte()
        if byte is None or byte == 0:
            break
        s += chr(byte)
    return s

print("RECEIVER listening...")
try:
    while True:
        msg = read_string()
        if msg:
            print(f"✓ '{msg}'")
        time.sleep(0.05)
except KeyboardInterrupt:
    GPIO.cleanup()