import os
import pymysql
from config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    """Create and return a database connection with error handling."""
    try:
        ca_path = Config.TIDB_SSL_CA
        ssl_params = {'ca': ca_path} if ca_path else None

        if not Config.TIDB_HOST:
            raise Exception("TIDB_HOST environment variable is not set")

        connection = pymysql.connect(
            host=Config.TIDB_HOST,
            port=Config.TIDB_PORT,
            user=Config.TIDB_USER,
            password=Config.TIDB_PASSWORD,
            database=Config.TIDB_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            ssl=ssl_params
        )
        return connection
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        raise


def init_db():
    """Initialize database tables and seed default portfolio data."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            # Create tables only if they don't exist (no DROP to preserve data)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    title VARCHAR(150),
                    bio TEXT,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    location VARCHAR(100),
                    github VARCHAR(200),
                    linkedin VARCHAR(200),
                    instagram VARCHAR(200),
                    photo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            # Add instagram column if it doesn't exist (for existing databases)
            cur.execute("SHOW COLUMNS FROM profiles LIKE 'instagram'")
            if not cur.fetchone():
                cur.execute("ALTER TABLE profiles ADD COLUMN instagram VARCHAR(200) AFTER linkedin")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50),
                    level INT DEFAULT 80,
                    icon VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    company VARCHAR(150) NOT NULL,
                    position VARCHAR(150) NOT NULL,
                    start_date VARCHAR(20),
                    end_date VARCHAR(20),
                    is_current TINYINT(1) DEFAULT 0,
                    description TEXT,
                    logo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    description TEXT,
                    tech_stack VARCHAR(300),
                    image_url VARCHAR(500),
                    demo_url VARCHAR(300),
                    repo_url VARCHAR(300),
                    is_featured TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    subject VARCHAR(200),
                    message TEXT NOT NULL,
                    is_read TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            cur.execute("SELECT COUNT(*) as cnt FROM profiles")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO profiles (name, title, bio, email, phone, location, github, linkedin, photo_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Shafa Reyna Nugrahani',
                    'Mahasiswa S1 Sistem Informasi',
                    'Saya adalah pengembang web yang senang membuat portofolio dan aplikasi yang nyaman digunakan.',
                    'shafareynana@gmail.com',
                    '+62 812-3456-7890',
                    'Salatiga, Indonesia',
                    'https://github.com',
                    'https://linkedin.com',
                    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=800&q=80'
                ))

            cur.execute("SELECT COUNT(*) as cnt FROM skills")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO skills (name, category, level, icon) VALUES
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """, (
                    'Python', 'Backend', 90, 'python',
                    'Flask', 'Backend', 85, 'flask',
                    'JavaScript', 'Frontend', 88, 'javascript',
                    'MySQL', 'Database', 80, 'mysql',
                    'Git', 'Tools', 82, 'git'
                ))

            cur.execute("SELECT COUNT(*) as cnt FROM experiences")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO experiences (company, position, start_date, end_date, is_current, description, logo_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s), (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Universitas Kristen Satya Wacana', 'Asisten Laboratorium', '2024', 'Sekarang', 1,
                    'Membantu praktikum dan mendukung kegiatan akademik.', 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=400&q=80',
                    'PT. Inovasi Digital', 'Web Developer Intern', '2023', '2024', 0,
                    'Mengembangkan halaman web sederhana dan memperbaiki bug aplikasi.', 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=400&q=80'
                ))

            cur.execute("SELECT COUNT(*) as cnt FROM projects")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO projects (title, description, tech_stack, image_url, demo_url, repo_url, is_featured)
                    VALUES (%s, %s, %s, %s, %s, %s, %s), (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Portfolio Website', 'Website portofolio interaktif berbasis Flask dan TiDB.', 'Python, Flask, HTML, CSS', 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80', 'https://example.com', 'https://github.com', 1,
                    'Sistem Informasi Akademik', 'Aplikasi sederhana untuk mengelola data akademik.', 'Python, Flask, MySQL', 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80', 'https://example.com', 'https://github.com', 0
                ))

        conn.commit()
    finally:
        conn.close()

def get_profiles():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM profiles")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting profiles: {e}")
        return []

def get_skills():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM skills")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting skills: {e}")
        return []

def get_projects():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM projects")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting projects: {e}")
        return []

def get_experience():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM experiences")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting experiences: {e}")
        return []
