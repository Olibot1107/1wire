import RPi.GPIO as GPIO
import time

DATA_PIN = 17
TICK_INTERVAL = 0.001  # 1ms per tick (1000 ticks/sec)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.output(DATA_PIN, 0)

def send_letter(char):
    """
    Send a letter using count encoding:
    - Send 1s to count up (a=1, b=2, c=3... z=26, space=27)
    - Send 0 to submit the letter
    """
    if char == ' ':
        count = 27
    else:
        count = ord(char.lower()) - ord('a') + 1  # a=1, b=2, etc.
    
    print(f"  '{char}' = {count} ticks")
    
    # Precise timing using perf_counter
    start_time = time.perf_counter()
    
    # Send 'count' number of 1s
    for i in range(count):
        GPIO.output(DATA_PIN, 1)
        
        # Wait until next tick
        next_tick = start_time + ((i + 1) * TICK_INTERVAL)
        while time.perf_counter() < next_tick:
            pass
    
    # Send 0 to submit
    GPIO.output(DATA_PIN, 0)
    next_tick = start_time + ((count + 1) * TICK_INTERVAL)
    while time.perf_counter() < next_tick:
        pass

def send_message(msg):
    print(f"\nSending: '{msg}'")
    for char in msg:
        if char.isalpha() or char == ' ':
            send_letter(char)
    
    # End of message: send 0 twice (no letter)
    print("  [END]")
    GPIO.output(DATA_PIN, 0)
    time.sleep(TICK_INTERVAL * 2)

print("=== CLOCK-SYNCED SENDER ===")
print(f"Tick interval: {TICK_INTERVAL*1000}ms")
print("Encoding: a=1 tick, b=2 ticks... z=26 ticks, space=27 ticks")
print()

try:
    while True:
        msg = input("Send: ")
        if msg:
            send_message(msg)
except KeyboardInterrupt:
    GPIO.cleanup()