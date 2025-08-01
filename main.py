import requests
import random
import string
import threading
import time
from queue import Queue

# Configuration
THREADS = 30                  # Max safe threads
TIMEOUT = 2                   # Seconds before timeout
OUTPUT_FILE = "4letter_combos.txt"

# Thread-safe setup
queue = Queue(maxsize=1000)
found = []
lock = threading.Lock()
running = True

def generate_combo():
    """Generates completely random 4-character combos"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(4))

def check_combo(combo):
    url = f"https://auth.roblox.com/v1/usernames/validate?request.username={combo}&request.birthday=2000-01-01"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.json().get("code") == 0:
            with lock:
                found.append(combo)
                with open(OUTPUT_FILE, 'a') as f:
                    f.write(f"{combo}\n")
            print(f"\033[92m[AVAILABLE] {combo}\033[0m")
            return True
        print(f"\033[91m[taken] {combo}\033[0m", end='\r', flush=True)
    except:
        pass
    return False

def worker():
    while running:
        try:
            combo = queue.get(timeout=1)
            check_combo(combo)
            queue.task_done()
            time.sleep(0.05)  # Critical to avoid blocks
        except:
            continue

def main():
    global running
    print("\033[1m🔥 BRUTE-FORCING ALL 4-CHAR COMBOS\033[0m")
    
    # Start threads
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)
    
    try:
        # Main producer loop
        while True:
            if queue.qsize() < THREADS * 10:
                queue.put(generate_combo())
            else:
                time.sleep(0.01)
            
            # Stats every minute
            if time.time() % 60 < 0.1 and found:
                print(f"\n\033[1m💎 Found: {len(found)} | Last: {found[-1]}\033[0m\n")
                
    except KeyboardInterrupt:
        running = False
        print("\n🛑 Stopping...")
        for t in threads:
            t.join(timeout=1)
        print(f"\033[1m✅ Saved {len(found)} combos to {OUTPUT_FILE}\033[0m")

if __name__ == "__main__":
    main()
