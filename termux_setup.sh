#!/data/data/com.termux/files/usr/bin/bash

echo "🔄 Updating Termux..."
pkg update -y
pkg upgrade -y

echo "📦 Installing system dependencies..."
pkg install -y \
python \
git \
ffmpeg \
libjpeg-turbo \
zlib \
freetype \
clang \
make \
cmake \
libffi \
openssl

echo "⬆️ Upgrading pip tools..."
pip install --upgrade pip setuptools wheel

echo "🐍 Installing Python requirements..."
pip install -r requirements.txt --no-cache-dir

echo "✅ Termux setup completed successfully"
