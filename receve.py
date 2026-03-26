import RPi.GPIO as GPIO
import time

DATA_PIN = 17
TICK_INTERVAL = 0.001  # Must match sender!
TIMEOUT = 5.0  # 5 seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_letter():
    """
    Count the number of 1s before getting a 0
    Returns the letter based on count
    """
    count = 0
    start_time = time.perf_counter()
    tick_num = 0
    
    while True:
        # Check for timeout
        if time.perf_counter() - start_time > TIMEOUT:
            return None
        
        # Sample at precise intervals
        sample_time = start_time + (tick_num * TICK_INTERVAL)
        
        # Wait until sample time
        while time.perf_counter() < sample_time:
            pass
        
        # Read the bit
        bit = GPIO.input(DATA_PIN)
        
        if bit == 1:
            count += 1
        else:
            # Got a 0 - submit the letter
            if count == 0:
                # Double 0 = end of message
                return None
            elif count == 27:
                return ' '
            elif 1 <= count <= 26:
                letter = chr(ord('a') + count - 1)
                print(f"  {count} ticks = '{letter}'")
                return letter
            else:
                print(f"  Invalid count: {count}")
                return '?'
        
        tick_num += 1

def read_message():
    msg = ""
    print("Reading message...")
    
    while True:
        letter = read_letter()
        if letter is None:
            break
        msg += letter
    
    return msg

print("=== CLOCK-SYNCED RECEIVER ===")
print(f"Tick interval: {TICK_INTERVAL*1000}ms")
print("Listening...\n")

try:
    while True:
        msg = read_message()
        if msg:
            print(f"\n✓ RECEIVED: '{msg}'\n")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()