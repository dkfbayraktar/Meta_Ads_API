# /export-excel endpoint'i: Belirtilen filtrelerle ad-level JSON verisini Excel'e çevirir ve dışa aktarır

import os
import json
import pandas as pd
from flask import Flask, request, send_file
from datetime import datetime

app = Flask(__name__)

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

    # Export klasörünü oluştur
    export_dir = "export"
    os.makedirs(export_dir, exist_ok=True)

    # Dosya adını belirle
    filename = f"filtered_{date}_{datetime.now().strftime('%H%M%S')}.xlsx"
    output_path = os.path.join(export_dir, filename)

    # Excel'e yaz
    df.to_excel(output_path, index=False)

    # Dosyayı gönder
    return send_file(output_path, as_attachment=True)

# Bu modül ayrı bir sunucu olarak çalıştırılacaksa:
# if __name__ == "__main__":
#     app.run(debug=True, port=5003)
