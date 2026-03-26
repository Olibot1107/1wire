import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.002  # MUST match sender!

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def wait_for_start():
    """Wait for the preamble pattern then start bit"""
    # Look for rising edge (preamble)
    while GPIO.input(DATA_PIN) == 1:
        pass
    while GPIO.input(DATA_PIN) == 0:
        pass
    # Now we're at a rising edge - this is our sync point
    return time.perf_counter()

def read_byte():
    # Sync on rising edge
    start_time = wait_for_start()
    
    # We're at the START of the start bit
    # Wait 1.5 bit times to get to MIDDLE of first data bit
    target = start_time + (BIT_DELAY * 1.5)
    while time.perf_counter() < target:
        pass
    
    # Read 8 data bits
    value = 0
    bits = []
    for i in range(8):
        bit = GPIO.input(DATA_PIN)
        bits.append(bit)
        value |= (bit << i)
        
        # Wait exactly one bit time
        target += BIT_DELAY
        while time.perf_counter() < target:
            pass
    
    print(f"  Bits: {bits} = {value:3d} = '{chr(value) if 32<=value<127 else '?'}'")
    return value

def read_string():
    s = ""
    print("Reading string...")
    while True:
        byte = read_byte()
        if byte == 0:
            break
        s += chr(byte)
    return s

print("=== RECEIVER ===")
print(f"BIT_DELAY = {BIT_DELAY}")
print(f"Pin state: {GPIO.input(DATA_PIN)} (should be 0)\n")

try:
    while True:
        msg = read_string()
        print(f"\n✓ RECEIVED: '{msg}'\n")
except KeyboardInterrupt:
    GPIO.cleanup()