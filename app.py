# Flask sunucusunu başlatır ve Meta Ads verilerini günlük ve saatlik olarak çeken endpoint'leri yönetir.

from flask import Flask, jsonify, request, send_file
from utils.meta_api import fetch_hourly_insights, fetch_ad_level_insights
from config import TOKEN_ID
import datetime
import os
import json
import pandas as pd

app = Flask(__name__)

# Klasörleri oluştur (ilk çalıştırmada kontrol)
os.makedirs("data/daily", exist_ok=True)
os.makedirs("data/hourly", exist_ok=True)
os.makedirs("export", exist_ok=True)

@app.route("/daily-insights", methods=["GET"])
def daily_insights():
    # Bir önceki günün tarihini al
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).date().isoformat()
    # Veri çekimi artık ad-level olarak yapılacak
    data = fetch_ad_level_insights(TOKEN_ID, date=yesterday)

    # Dosya kaydet
    file_path = f"data/daily/{yesterday}.json"
    with open(file_path, "w") as f:
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
        json.dump(data, f, indent=2)

    return jsonify({"status": "success", "date": yesterday, "records": len(data)})


@app.route("/export-excel", methods=["GET"])
def export_excel():
    # Parametreleri al
    date = request.args.get("date")  # örnek: 2025-05-16
    country = request.args.get("country")
    gender = request.args.get("gender")
    age = request.args.get("age")

    if not date:
        return {"error": "date parametresi zorunludur. Örnek: /export-excel?date=2025-05-16"}, 400

    # Dosya yolunu belirle
    file_path = f"data/daily/{date}.json"
    if not os.path.exists(file_path):
        return {"error": f"Belirtilen tarih için veri bulunamadı: {file_path}"}, 404

    # JSON verisini oku
    with open(file_path, "r") as f:
        raw_data = json.load(f)

    # DataFrame'e çevir
    df = pd.DataFrame(raw_data)

    # Filtre uygula
    if country:
        df = df[df["country"] == country]
    if gender:
        df = df[df["gender"] == gender]
    if age:
        df = df[df["age"] == age]

    # Dosya adını belirle
    filename = f"filtered_{date}_{datetime.datetime.now().strftime('%H%M%S')}.xlsx"
    output_path = os.path.join("export", filename)

    # Excel'e yaz
    df.to_excel(output_path, index=False)

    # Dosyayı gönder
    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
