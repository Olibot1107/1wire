import RPi.GPIO as GPIO
import time

DATA_PIN = 17
BIT_DELAY = 0.002

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def wait_for_start():
    while GPIO.input(DATA_PIN) == 1:
        pass
    while GPIO.input(DATA_PIN) == 0:
        pass
    return time.perf_counter()

def read_byte(offset_multiplier):
    start_time = wait_for_start()
    
    # Try different offsets
    target = start_time + (BIT_DELAY * offset_multiplier)
    while time.perf_counter() < target:
        pass
    
    value = 0
    bits = []
    for i in range(8):
        bit = GPIO.input(DATA_PIN)
        bits.append(bit)
        value |= (bit << i)
        
        target += BIT_DELAY
        while time.perf_counter() < target:
            pass
    
    print(f"  Offset {offset_multiplier}: {bits} = {value:3d} = '{chr(value) if 32<=value<127 else '?'}'")
    return value

print("Testing different timing offsets...")
print("Expected for 'A': [1,0,0,0,0,0,1,0] = 65")
print()

# Test different offsets
for offset in [1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0]:
    print(f"\nTrying offset {offset}:")
    read_byte(offset)
    read_byte(offset)  # Read the null byte too
    time.sleep(0.5)
    print("Press Ctrl+C and re-run sender for next test")
    input("Press Enter to try next offset...")

GPIO.cleanup()