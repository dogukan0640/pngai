import time
import schedule
from data_logger import collect_data
from telegram_notifier import send_telegram_message

def job():
    collect_data()

def start():
    send_telegram_message("📡 Render AI Bot Başladı.")
    schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    start()
