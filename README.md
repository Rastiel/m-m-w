# m-m-w (messenger-meta-webhook)

Facebook Messenger için geliştirilen basit bir Flask tabanlı webhook servisidir. Docker ile konteynerize edilmiştir.

## 🔧 Kurulum

```bash
git clone https://github.com/Rastiel/m-m-w.git
cd m-m-w
docker build -t m-m-w .
docker run -d -p 10000:10000 --env-file .env m-m-w
```

## 📬 Webhook Doğrulama

Webhook URL: `http://<sunucu-ip>:10000/`  
Doğrulama Token: `.env` dosyasındaki `VERIFY_TOKEN` değeri

## 📂 Ortam Değişkeni

`.env` dosyası oluşturulmalı ve içine şu değer yazılmalı:

```env
VERIFY_TOKEN=rastiel_token
```

## 📦 Geliştirici: [@Rastiel](https://github.com/Rastiel)
