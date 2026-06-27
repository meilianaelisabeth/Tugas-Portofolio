import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('FLASK_SECRET_KEY') or 'dev-key-ganti-nanti'

    DB_HOST = (os.environ.get('DB_HOST') or os.environ.get('TIDB_HOST') or '').strip() or None
    DB_USER = (os.environ.get('DB_USER') or os.environ.get('TIDB_USER') or '').strip() or None
    DB_PASSWORD = (os.environ.get('DB_PASSWORD') or os.environ.get('TIDB_PASSWORD') or '').strip() or None
    DB_NAME = (os.environ.get('DB_NAME') or os.environ.get('TIDB_DATABASE') or 'portofolio').strip() or 'portofolio'
    DB_PORT = int((os.environ.get('DB_PORT') or os.environ.get('TIDB_PORT') or '4000').strip())

    CLOUDINARY_URL = (os.environ.get('CLOUDINARY_URL') or '').strip()
    if CLOUDINARY_URL.startswith('CLOUDINARY_URL='):
        CLOUDINARY_URL = CLOUDINARY_URL.split('=', 1)[1]
    if not CLOUDINARY_URL:
        cloud_name = (os.environ.get('CLOUDINARY_CLOUD_NAME') or '').strip()
        api_key = (os.environ.get('CLOUDINARY_API_KEY') or '').strip()
        api_secret = (os.environ.get('CLOUDINARY_API_SECRET') or '').strip()
        if cloud_name and api_key and api_secret:
            CLOUDINARY_URL = f'cloudinary://{api_key}:{api_secret}@{cloud_name}'
        else:
            CLOUDINARY_URL = 'cloudinary://demo:demo@demo'
            # Konfigurasi API Resend untuk Pengiriman Email Tugas
# Konfigurasi API Resend untuk Pengiriman Email Tugas
    RESEND_API_KEY = (os.environ.get('RESEND_API_KEY') or '').strip() or None