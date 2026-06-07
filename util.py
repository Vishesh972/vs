import asyncio
import os

NUMBERS_FILE = "sanskar.txt"
USED_FILE = "used_nums.txt"

lock = asyncio.Lock()

all_numbers = []
used_numbers = set()
current_index = 0

def format_number(num: str) -> str:
    # Split into groups of 3 (like 549 908 977)
    return " ".join([num[i:i+3] for i in range(0, len(num), 3)])

def load_data():
    global all_numbers, used_numbers

    # Load all numbers
    with open(NUMBERS_FILE, "r") as f:
        all_numbers = [line.strip() for line in f if line.strip()]

    # Load used numbers
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r") as f:
            used_numbers = set(line.strip() for line in f if line.strip())
    else:
        open(USED_FILE, "w").close()

    print(f"✅ Loaded {len(all_numbers)} numbers")
    print(f"🔒 {len(used_numbers)} already used")
load_data()

async def get_number():
    global current_index, used_numbers

    async with lock:
        while current_index < len(all_numbers):
            num = all_numbers[current_index]
            current_index += 1

            if num not in used_numbers:
                return num
                formatted = format_number(num)
                print(f"📱 New number: {formatted}")
                return formatted

        # All numbers exhausted - reset and restart
        print("🔄 All numbers used! Restarting from 0...")
        if os.path.exists(USED_FILE):
            os.remove(USED_FILE)
            print(f"🗑️  Deleted {USED_FILE}")
        
        current_index = 0
        used_numbers = set()
        
        # Now loop again to get the first number from the reset list
        num = all_numbers[current_index]
        current_index += 1
        return num


async def mark_used(num: str):
    async with lock:
        raw_num = num.replace(" ", "")

        if raw_num in used_numbers:
            return

        used_numbers.add(raw_num)

        with open(USED_FILE, "a") as f:
            f.write(raw_num + "\n")  

        print(f"🔒 Marked used: {raw_num}")

async def main():
    for i in range(8):
        k = await get_number()
        print(k)
        await mark_used(k)  
if __name__=='__main__':
    asyncio.run(main())