from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
import mysql.connector

@contextmanager
def koneksi():
    config = ConfigParser(interpolation=None)
    path = Path(__file__).resolve().with_name("config.ini")
    if not path.is_file():
        raise ValueError("File konfigurasi tidak ditemukan.")
    config.read(path, encoding="utf-8")
    if not config.has_section("mysql"):
        raise ValueError("Bagian [mysql] tidak ditemukan pada config.ini.")
    c = config["mysql"]
    db = mysql.connector.connect(
        host=c.get("host", "127.0.0.1"), port=c.getint("port", 3306),
        user=c.get("user", ""), password=c.get("password", ""),
        database=c.get("database", "db_penggajian_modul5"),
        charset="utf8mb4", connection_timeout=5, autocommit=False,
        use_pure=True,
    )
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()