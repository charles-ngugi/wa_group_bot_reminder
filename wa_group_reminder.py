import pywhatkit as kit
import schedule
import time
from datetime import datetime
import os

# CONFIG
GROUP_NAME = "MY LITTLE OFFICE"  #Replace with exact group name
MESSAGE = "🔔 Monthly Reminder: Don't forget to make your Savings deposits!" # Replace with custom message
SEND_HOUR = 12  # 24-hour format
SEND_MINUTE = 00

def send_group_reminder():
    today = datetime.now()
    print(f"[{today.strftime('%Y-%m-%d %H:%M:%S')}] Checking if today is in range...")
    if 12 <= today.day <= 15:
        print(f"[INFO] Today is {today.day}, in range. Preparing to send message to '{GROUP_NAME}'")
        
        try:
            # Optional: Check or delete old DB file if it exists
            db_file = os.path.expanduser("~/PyWhatKit_DB.txt")
            if os.path.exists(db_file) and not os.access(db_file, os.W_OK):
                print(f"[WARN] Cannot write to {db_file}. Attempting to delete...")
                os.remove(db_file)

            kit.sendwhatmsg_to_group_instantly(
                f"{GROUP_NAME}",
                MESSAGE,
                wait_time=20,  # Increase to allow WhatsApp Web to load fully
                tab_close=False  # Keep tab open to see what happens
            )
            print("[SUCCESS] Message sent.")
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
    else:
        print(f"[INFO] Today ({today.day}) is outside range. Skipping.")

# Schedule daily run
schedule.every().day.at(f"{SEND_HOUR:02d}:{SEND_MINUTE:02d}").do(send_group_reminder)

print("[BOOT] Reminder bot started. Waiting to send messages...")

while True:
    schedule.run_pending()
    time.sleep(60)
