import json
import time
import os
import requests 
from datetime import datetime
from config import VERSION, INTERVAL, LOG_TO_TELEGRAM_BOT_TOKEN, LOG_TO_TELEGRAM_CHAT_ID
from myagent.collector import Collector

def send_file_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{LOG_TO_TELEGRAM_BOT_TOKEN}/sendDocument"
    try: 
        with open(file_path, 'rb') as f:
            files = {'document': f}
            payload = {'chat_id': LOG_TO_TELEGRAM_CHAT_ID, 'caption': f"Scan Report: {os.path.basename(file_path)}"}
            requests.post(url, files=files, data=payload, timeout=(5, 10))
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def main():
    print(f"--- Starting Agent Version {VERSION} ---")
    collector = Collector()

    try:
        while True:
            print("Collecting data...")
            report_data = collector.collect_info()
            
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            filename = f"scan_{timestamp}.json"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4, ensure_ascii=False)
            
            print(f"Scan completed. Report saved to {filename}.")
            
            print("Sending to Telegram...")
            send_file_to_telegram(filename)
            
            print(f"Next scan in {INTERVAL}...")
            time.sleep(INTERVAL.total_seconds())

    except KeyboardInterrupt:
        print("\nAgent stopped by user.")

if __name__ == "__main__":
    main()

