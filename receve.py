import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.002  # MUST match sender!

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_byte():
    # Wait for LOW state first (clear any noise)
    timeout = time.time() + 5
    while GPIO.input(DATA_PIN) == 1:
        if time.time() > timeout:
            return None
    
    # Now wait for rising edge (start bit)
    while GPIO.input(DATA_PIN) == 0:
        if time.time() > timeout:
            return None
    
    # RESYNC: We just caught the rising edge
    # Use time.perf_counter for precision
    sync_time = time.perf_counter()
    
    # Jump to middle of first data bit
    next_sample = sync_time + (BIT_DELAY * 1.5)
    
    # Read 8 bits with FIXED timing from sync point
    value = 0
    for i in range(8):
        # Wait until sample time
        while time.perf_counter() < next_sample:
            pass
        
        # Sample the bit
        if GPIO.input(DATA_PIN):
            value |= (1 << i)
        
        # Schedule next sample exactly 1 BIT_DELAY later
        next_sample += BIT_DELAY
    
    # Skip stop bit
    next_sample += BIT_DELAY
    while time.perf_counter() < next_sample:
        pass
    
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
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()