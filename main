import requests
import random
import string
import threading
import time
from queue import Queue

# Configuration
MIN_LENGTH = 3
MAX_LENGTH = 4
BIRTHDAY = "1999-04-20"  # Change if needed
OUTPUT_FILE = "valid_usernames.txt"
THREADS = 20  # Increase for faster checking (but don't go over 50)
TIMEOUT = 3  # Seconds before request times out

# Colors for terminal output
class colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"

# Thread-safe counter and file writing
found_counter = 0
lock = threading.Lock()
queue = Queue()

def generate_username():
    """Generate random 3-4 character username"""
    length = random.randint(MIN_LENGTH, MAX_LENGTH)
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def check_username(username):
    """Check if username is available"""
    url = f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday={BIRTHDAY}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get("code") == 0
    except:
        return False

def worker():
    """Thread worker function"""
    while True:
        username = queue.get()
        if check_username(username):
            with lock:
                with open(OUTPUT_FILE, "a") as f:
                    f.write(f"{username}\n")
                global found_counter
                found_counter += 1
                print(f"{colors.GREEN}[+] {username}{colors.END}")
        else:
            print(f"{colors.RED}[-] {username}{colors.END}")
        queue.task_done()

def main():
    print(f"{colors.BLUE}Starting Roblox Username Sniper{colors.END}")
    print(f"Checking {MIN_LENGTH}-{MAX_LENGTH} character usernames")
    print(f"Threads: {THREADS} | Output: {OUTPUT_FILE}")
    print("Press Ctrl+C to stop\n")

    # Create worker threads
    for _ in range(THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    try:
        while True:
            # Keep the queue full
            if queue.qsize() < THREADS * 2:
                queue.put(generate_username())
            else:
                time.sleep(0.01)
                
    except KeyboardInterrupt:
        print(f"\n{colors.YELLOW}Stopping... Found {found_counter} usernames{colors.END}")
        queue.join()  # Let threads finish

if __name__ == "__main__":
    main()
