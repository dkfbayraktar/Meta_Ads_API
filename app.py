# Flask sunucusunu başlatır ve Meta Ads verilerini günlük ve saatlik olarak çeken endpoint'leri yönetir.
# Bu dosya çalıştırıldığında gerekli veri klasörleri otomatik olarak oluşturulur

from flask import Flask, jsonify
from meta_api import fetch_hourly_insights, fetch_ad_level_insights
from config import TOKEN_ID
import datetime
import os

app = Flask(__name__)

# Klasörleri oluştur (ilk çalıştırmada kontrol)
os.makedirs("data/daily", exist_ok=True)
os.makedirs("data/hourly", exist_ok=True)

# Eğer klasörler GitHub'da da takip edilsin isteniyorsa, .gitkeep dosyaları ekle
open("data/daily/.gitkeep", "a").close()
open("data/hourly/.gitkeep", "a").close()

@app.route("/daily-insights", methods=["GET"])
def daily_insights():
    # Bir önceki günün tarihini al
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).date().isoformat()
    # Veri çekimi artık ad-level olarak yapılacak
    data = fetch_ad_level_insights(TOKEN_ID, date=yesterday)

    # Dosya kaydet
    file_path = f"data/daily/{yesterday}.json"
    with open(file_path, "w") as f:
        import json
        json.dump(data, f, indent=2)

    return jsonify({"status": "success", "date": yesterday, "records": len(data)})


@app.route("/hourly-insights", methods=["GET"])
def hourly_insights():
    # Bir önceki günün tarihini al
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).date().isoformat()
    # Veri çekimi
    data = fetch_hourly_insights(TOKEN_ID, date=yesterday)

    # Dosya kaydet
    file_path = f"data/hourly/{yesterday}.json"
    with open(file_path, "w") as f:
        import json
        json.dump(data, f, indent=2)

    return jsonify({"status": "success", "date": yesterday, "records": len(data)})


if __name__ == "__main__":
    app.run(debug=True, port=5002)