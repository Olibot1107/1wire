import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.002

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_byte():
    # Wait for start bit LOW→HIGH
    timeout = time.time() + 10
    while GPIO.input(DATA_PIN) == 0:
        if time.time() > timeout:
            return None
    
    # We just detected rising edge of start bit
    # Sample in the MIDDLE of each bit
    start = time.perf_counter()
    
    # Wait to middle of FIRST data bit (1.5 bit periods from start)
    target = start + (BIT_DELAY * 1.5)
    while time.perf_counter() < target:
        pass
    
    # Read 8 data bits
    value = 0
    bits = []
    for i in range(8):
        bit = GPIO.input(DATA_PIN)
        bits.append(bit)
        value |= (bit << i)
        
        # Move to middle of next bit
        target += BIT_DELAY
        while time.perf_counter() < target:
            pass
    
    # Verify it's a real byte
    if value == 0:
        print(f"  NULL")
    else:
        print(f"  {bits} = {value:3d} = '{chr(value)}'")
    
    # Wait for stop bit
    target += BIT_DELAY
    while time.perf_counter() < target:
        pass
    
    return value

def read_string():
    s = ""
    print("Waiting for message...")
    while True:
        byte = read_byte()
        if byte is None:
            return None
        if byte == 0:
            break
        s += chr(byte)
    return s

print("=== RECEIVER ===")
print("Listening...\n")

try:
    while True:
        msg = read_string()
        if msg:
            print(f"\n>>> '{msg}'\n")
except KeyboardInterrupt:
    GPIO.cleanup()