# --- Giai đoạn 1: Xây dựng Môi trường ---
# Bắt đầu từ một Python image chính thức, gọn nhẹ
FROM python:3.9-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# --- Giai đoạn 2: Cài đặt Thư viện ---
# Sao chép tệp requirements.txt vào trước
# Tận dụng cơ chế cache của Docker: nếu tệp này không đổi, Docker sẽ không chạy lại bước này
COPY requirements.txt .

# Chạy lệnh pip để cài đặt tất cả các thư viện cần thiết
# --no-cache-dir giúp giảm kích thước của image
RUN pip install --no-cache-dir -r requirements.txt

# --- Giai đoạn 3: Sao chép Mã nguồn ---
# Sao chép toàn bộ mã nguồn của dự án vào thư mục làm việc trong container
COPY . .

# --- Giai đoạn 4: Cấu hình và Chạy ---
# Mở cổng 8501 để có thể truy cập ứng dụng Streamlit từ bên ngoài container
EXPOSE 8501

# Thiết lập biến môi trường để Streamlit chạy ở chế độ headless (không mở trình duyệt)
ENV STREAMLIT_SERVER_HEADLESS=true

# Lệnh sẽ được thực thi khi container khởi động
# Chạy ứng dụng Streamlit và cho phép truy cập từ mọi địa chỉ mạng
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

