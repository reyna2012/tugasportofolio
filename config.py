import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Flask configuration from environment variables."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Warn if using default SECRET_KEY in production
    if FLASK_ENV == 'production' and SECRET_KEY == 'dev-secret-change-in-production':
        print("⚠️  WARNING: Using default SECRET_KEY in production! Set SECRET_KEY env variable.")

    # ===== TiDB Database Configuration =====
    TIDB_HOST = os.getenv('TIDB_HOST')
    TIDB_PORT = int(os.getenv('TIDB_PORT', '4000'))
    TIDB_USER = os.getenv('TIDB_USER')
    TIDB_PASSWORD = os.getenv('TIDB_PASSWORD')
    TIDB_DB = os.getenv('TIDB_DB', 'portofolio_db')
    
    # SSL Certificate for TiDB
    raw_ca = os.getenv('TIDB_SSL_CA', '')
    if raw_ca and raw_ca.strip():
        TIDB_SSL_CA = raw_ca.replace("\\", "/")  # Convert backslash to forward slash
    else:
        TIDB_SSL_CA = None
    
    # Log TiDB config (without password)
    if TIDB_HOST:
        print(f"✅ TiDB configured: {TIDB_HOST}:{TIDB_PORT}/{TIDB_DB}")

    # ===== Cloudinary Configuration =====
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    
    if CLOUDINARY_CLOUD_NAME:
        print(f"✅ Cloudinary configured: {CLOUDINARY_CLOUD_NAME}")

    # ===== Resend Email Configuration =====
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    RESEND_TO_EMAIL = os.getenv('RESEND_TO_EMAIL')
    
    if RESEND_API_KEY:
        print(f"✅ Resend configured: {RESEND_FROM_EMAIL}")

    # ===== Admin Credentials =====
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Flask-specific configs
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @classmethod
    def get_db_config(cls):
        """Get database configuration as dictionary."""
        return {
            'host': cls.TIDB_HOST,
            'port': cls.TIDB_PORT,
            'user': cls.TIDB_USER,
            'password': cls.TIDB_PASSWORD,
            'database': cls.TIDB_DB,
            'ssl': {'ca': cls.TIDB_SSL_CA} if cls.TIDB_SSL_CA else {}
        }
