# Python 3.11 sürümünün küçük boyutlu resmi imajını baz alıyoruz
FROM python:3.11-slim

# Uygulama çalışacağı dizin: /app
WORKDIR /app

# Python çıktılarının tamponlanmadan direkt gösterilmesini sağlar (loglar anlık görünür)
ENV PYTHONUNBUFFERED=TRUE

# Tüm proje dosyalarını bulunduğun dizinden container içindeki /app klasörüne kopyala
COPY . .

# requirements.txt içindeki bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı Gunicorn ile başlat
# --bind: Hangi IP ve portta dinlenecek (0.0.0.0:10000)
# --log-syslog: Logları syslog üzerinden yaz (container log'ları ile entegre)
# --capture-output: stdout/stderr çıktıları da log olarak yakalanır
# --access-logfile -: HTTP erişim loglarını terminale (stdout) yaz
# app:app → "app.py" içindeki "app" adlı Flask uygulamasını çalıştır
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--log-syslog", "--capture-output", "--access-logfile", "-", "app:app"]
