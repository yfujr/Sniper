import requests
import random
import string
import threading
import time
from queue import Queue

# Configuration
THREADS = 28                  # Optimal for Roblox rate limits
TIMEOUT = 2.5                 # Seconds before request times out
OUTPUT_FILE = "4char_gems.txt"
BIRTHDAY = "2000-01-01"       # Default birthday for validation

# High-value 4-char patterns (C=consonant, v=vowel, n=number)
PATTERNS = [
    'CvCn',  # e.g. "Doge1" (Best success rate)
    'nCvC',  # e.g. "7Pie"
    'CCnn',  # e.g. "ZX42" (Most available)
    'CnCn',  # e.g. "A1B2" (Good for alts)
]

# Thread-safe objects
queue = Queue()
found = []
lock = threading.Lock()
consonants = 'bcdfghjklmnpqrstvwxyz'
vowels = 'aeiou'
numbers = '123456789'

def generate_4char():
    pattern = random.choice(PATTERNS)
    name = []
    for char in pattern:
        if char == 'C':
            name.append(random.choice(consonants))
        elif char == 'v':
            name.append(random.choice(vowels))
        elif char == 'n':
            name.append(random.choice(numbers))
    return ''.join(name)

def check_name(name):
    url = f"https://auth.roblox.com/v1/usernames/validate?request.username={name}&request.birthday={BIRTHDAY}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.json().get("code") == 0:
            with lock:
                found.append(name)
                with open(OUTPUT_FILE, 'a') as f:
                    f.write(f"{name}\n")
            print(f"\033[92m[✔️] {name}\033[0m")
            return True
        print(f"\033[91m[✖] {name}\033[0m", end='\r', flush=True)
    except Exception as e:
        pass
    return False

def worker():
    while True:
        name = queue.get()
        check_name(name)
        queue.task_done()

if __name__ == "__main__":
    # Start threads
    for _ in range(THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    print(f"\033[1m🔥 Scanning for 4-character gems (Patterns: {', '.join(PATTERNS)})\033[0m")
    
    try:
        while True:
            if queue.qsize() < THREADS * 3:
                queue.put(generate_4char())
            else:
                time.sleep(0.01)
            
            # Display stats every 30 seconds
            if time.time() % 30 < 0.1 and found:
                print(f"\n\033[1m💎 Found {len(found)} | Last: {found[-1]}\033[0m\n")

    except KeyboardInterrupt:
        print(f"\n\033[1m✅ Saved {len(found)} premium names to {OUTPUT_FILE}\033[0m")
        if found:
            print("Top finds:", ', '.join(found[-5:]))
