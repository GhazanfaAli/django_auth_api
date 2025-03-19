#!/bin/bash



echo "🚀 Starting build project..."

# Navigate to the project directory (update as needed)
python 3.10 -m pip install -r requirements.txt

# Activate the virtual environment
echo "🔹 Activating virtual environment..."
source /home/hpubundu/phone/Django_Rest/venv/bin/activate



# Apply database migrations
echo "🗄️ Applying migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear
