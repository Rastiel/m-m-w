#!/bin/bash

echo "🔄 Kodlar GitHub'dan çekiliyor..."
git pull origin main || { echo "❌ Git pull başarısız"; exit 1; }

echo "🐳 Docker imajı oluşturuluyor (cache'siz)..."
docker build --no-cache -t m-m-w . || { echo "❌ Docker build başarısız"; exit 1; }

echo "🛑 Eski container durduruluyor (varsa)..."
docker stop m-m-w || true

echo "🧹 Eski container siliniyor (varsa)..."
docker rm m-m-w || true

echo "🚀 Yeni container başlatılıyor..."
docker run -d -p 10000:10000 --env-file .env --name m-m-w m-m-w || { echo "❌ Docker run başarısız"; exit 1; }

echo "✅ Başarıyla güncellendi ve çalışıyor."
