#!/bin/bash

echo "🚀 Starting build project..."

# Ensure the script is run from the correct directory
cd /home/hpubundu/phone/Django_Rest/auth_api2 || { echo "❌ Project directory not found!"; exit 1; }

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found! Creating one..."
  python3.10 -m venv venv
fi

# Activate the virtual environment
echo "🔹 Activating virtual environment..."
source venv/bin/activate || { echo "❌ Failed to activate virtual environment!"; exit 1; }

# Install dependencies
if [ -f "requirements.txt" ]; then
  echo "📦 Installing dependencies..."
  python3.10 -m pip install --upgrade pip
  python3.10 -m pip install -r requirements.txt
else
  echo "⚠️ requirements.txt not found! Skipping dependency installation."
fi

# Apply database migrations
if [ -f "manage.py" ]; then
  echo "🗄️ Applying migrations..."
  python3.10 manage.py makemigrations --noinput
  python3.10 manage.py migrate --noinput

  # Collect static files
  echo "📁 Collecting static files..."
  python3.10 manage.py collectstatic --noinput --clear
else
  echo "❌ manage.py not found! Please check the project directory."
  exit 1
fi

echo "✅ Build process completed!"
