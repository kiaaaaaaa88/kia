from passlib.context import CryptContext
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_pg_connection():
    # Menggunakan variabel lingkungan untuk URL koneksi PostgreSQL
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
    return conn

# Inisialisasi CryptContext untuk hashing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Meng-hash password
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifikasi password dengan hash
    return pwd_context.verify(plain_password, hashed_password)
