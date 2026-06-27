import os
import sqlite3

from config import Config

try:
    import pymysql
except ImportError:  # pragma: no cover - optional dependency
    pymysql = None


class SQLiteCursor:
    def __init__(self, connection):
        self._connection = connection
        self._cursor = connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()

    def execute(self, query, params=None):
        if params is None:
            params = ()
        if not isinstance(params, (tuple, list)):
            params = (params,)
        sql = query.replace('%s', '?')
        return self._cursor.execute(sql, params)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()


class SQLiteConnection:
    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row

    def cursor(self):
        return SQLiteCursor(self._connection)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()


def _initialize_sqlite(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profil (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                judul_profesi TEXT,
                deskripsi TEXT,
                foto_url TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_skill TEXT NOT NULL,
                tingkat_keahlian TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                perusahaan TEXT NOT NULL,
                posisi TEXT NOT NULL,
                tahun TEXT,
                deskripsi TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_proyek TEXT NOT NULL,
                deskripsi TEXT,
                link_proyek TEXT,
                gambar_url TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pengirim TEXT NOT NULL,
                email_pengirim TEXT NOT NULL,
                isi_pesan TEXT NOT NULL,
                tanggal_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("SELECT COUNT(*) AS total FROM admin WHERE username = ?", ('admin',))
        if cursor.fetchone()['total'] == 0:
            cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'admin123'))

        connection.commit()


def _initialize_mysql(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profil (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                judul_profesi VARCHAR(100),
                deskripsi TEXT,
                foto_url VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_skill VARCHAR(50) NOT NULL,
                tingkat_keahlian VARCHAR(50)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experience (
                id INT AUTO_INCREMENT PRIMARY KEY,
                perusahaan VARCHAR(100) NOT NULL,
                posisi VARCHAR(100) NOT NULL,
                tahun VARCHAR(50),
                deskripsi TEXT
            )
        """)
        try:
            cursor.execute("ALTER TABLE experience MODIFY COLUMN tahun VARCHAR(50)")
        except Exception:
            pass
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_proyek VARCHAR(100) NOT NULL,
                deskripsi TEXT,
                link_proyek VARCHAR(255),
                gambar_url VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_pengirim VARCHAR(100) NOT NULL,
                email_pengirim VARCHAR(100) NOT NULL,
                isi_pesan TEXT NOT NULL,
                tanggal_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("SELECT COUNT(*) AS total FROM admin WHERE username = %s", ('admin',))
        if cursor.fetchone()['total'] == 0:
            cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", ('admin', 'admin123'))

        connection.commit()


def get_db_connection():
    if Config.DB_HOST and Config.DB_USER and Config.DB_PASSWORD and pymysql is not None:
        try:
            connection = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=2
            )
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}`")
            connection.commit()
            connection.select_db(Config.DB_NAME)
            _initialize_mysql(connection)
            return connection
        except Exception as exc:  # pragma: no cover - fallback path
            print(f'Gagal tersambung ke TiDB Cloud: {exc}')

    db_path = os.environ.get('SQLITE_DB_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'portfolio.db'))
    connection = SQLiteConnection(db_path)
    _initialize_sqlite(connection)
    return connection