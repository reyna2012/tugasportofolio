import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'reyna_secret_porto')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Warn jika menggunakan SECRET_KEY default di production
    if FLASK_ENV == 'production' and SECRET_KEY == 'reyna_secret_porto':
        print("⚠️  WARNING: Using default SECRET_KEY in production! Set SECRET_KEY environment variable.")

    # TiDB
    TIDB_HOST     = os.getenv('TIDB_HOST')
    TIDB_PORT     = int(os.getenv('TIDB_PORT', 4000))
    TIDB_USER     = os.getenv('TIDB_USER')
    TIDB_PASSWORD = os.getenv('TIDB_PASSWORD')
    TIDB_DB       = os.getenv('TIDB_DB', 'db_porto')

    # Pastikan path SSL CA aman
    raw_ca = os.getenv('TIDB_SSL_CA')
    if raw_ca:
        TIDB_SSL_CA = raw_ca.replace("\\", "/")  # ganti backslash jadi slash
    else:
        TIDB_SSL_CA = None

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY    = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    # Resend
    RESEND_API_KEY    = os.getenv('RESEND_API_KEY')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    RESEND_TO_EMAIL   = os.getenv('RESEND_TO_EMAIL')

    # Admin
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

