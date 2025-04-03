# m-m-w (messenger-meta-webhook)

Facebook Messenger için geliştirilen basit bir Flask tabanlı webhook servisidir. Docker ile konteynerize edilmiştir.

## 🔧 Kurulum

```bash
git clone https://github.com/Rastiel/m-m-w.git
cd m-m-w
docker build -t m-m-w .
docker run -d -p 10000:10000 --env-file .env m-m-w
