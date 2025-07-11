import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from dotenv import load_dotenv

# Tải các biến môi trường từ tệp .env
load_dotenv() 

# Lấy thông tin cấu hình TRỰC TIẾP từ biến môi trường
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Kiểm tra xem các biến có tồn tại không
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    # Sử dụng st.error để hiển thị thông báo lỗi trên giao diện
    st.error("Lỗi cấu hình CSDL: Một hoặc nhiều biến môi trường bị thiếu. Hãy kiểm tra lại tệp .env của bạn.")
    # Dừng ứng dụng nếu thiếu cấu hình
    st.stop()

# Xây dựng URL kết nối CSDL
SQLALCHEMY_DATABASE_URL = (
    f"singlestoredb://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Tạo SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()