# 🌸 Portofolio Web — Flask + TiDB + Cloudinary + Resend

Aplikasi web portofolio dinamis dengan backend Python/Flask, database TiDB, upload gambar Cloudinary, dan pengiriman email via Resend.

## Struktur Folder

```
tugas_portofolio/
├── Backend/
│   ├── admin/
│   │   ├── dashboard.py
│   │   ├── experience.py
│   │   ├── login.py
│   │   ├── profiles.py
│   │   ├── projects.py
│   │   ├── skills.py
│   │   ├── upload.py
│   │   └── contact.py
│   └── utama/
│       └── utama.py
├── Frontend/
│   ├── admin/
│   │   ├── css/
│   │   ├── js/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── experience.html
│   │   ├── login.html
│   │   ├── profiles.html
│   │   ├── projects.html
│   │   ├── skills.html
│   │   └── contacts.html
│   └── utama/
│       ├── css/style.css
│       ├── js/script.js
│       └── index.html
├── .env
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── database.sql
├── model.py
├── requirements.txt
└── README.md
```

## Setup & Instalasi

### 1. Clone / extract project

### 2. Buat virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi `.env`
Salin `.env.example` → `.env` dan isi semua nilai:
```
SECRET_KEY=ganti_dengan_random_string
TIDB_HOST=...
TIDB_USER=...
TIDB_PASSWORD=...
TIDB_DB=portofolio_db
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
RESEND_API_KEY=...
RESEND_FROM_EMAIL=onboarding@resend.dev
RESEND_TO_EMAIL=emailkamu@example.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 5. Import database
Jalankan `database.sql` di TiDB / MySQL:
```sql
source database.sql
```

### 6. Jalankan aplikasi
```bash
python app.py
```

Buka: http://localhost:5000

## Akses Admin
- URL: http://localhost:5000/admin/login
- Username: `admin`
- Password: `admin123`

## Layanan Eksternal
| Layanan | Fungsi | URL |
|---------|--------|-----|
| TiDB | Database MySQL-compatible cloud | https://tidbcloud.com |
| Cloudinary | Upload & hosting gambar | https://cloudinary.com |
| Resend | Pengiriman email transaksional | https://resend.com |
