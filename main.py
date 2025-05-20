import time
import schedule
from data_logger import collect_data
from predictor import make_prediction
from telegram_notifier import send_telegram_message

def job():
    collect_data()
    prediction = make_prediction()
    send_telegram_message(f"🤖 Tahmin: {prediction}")

def start():
    send_telegram_message("📡 Render AI Bot Başladı.")
    schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    start()
