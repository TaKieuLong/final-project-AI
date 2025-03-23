# 🛒 Tích hợp AI cho E-commerce

Dự án này là một ứng dụng backend FastAPI tích hợp các khả năng AI vào nền tảng thương mại điện tử. Nó cung cấp tính năng phân loại hình ảnh, phân tích cảm xúc cho đánh giá và đề xuất sản phẩm.

## 🌐 Demo Trực tuyến

Ứng dụng được triển khai trên Railway và có thể truy cập tại:
[https://final-project-ai-production.up.railway.app](https://final-project-ai-production.up.railway.app)

## ✨ Tính năng

- **🖼️ Phân loại Hình ảnh**: Nhận diện sản phẩm trong hình ảnh được tải lên sử dụng mô hình MobileNet
- **📝 Phân tích Đánh giá**: Phân tích cảm xúc trên đánh giá sản phẩm sử dụng mô hình DistilBERT của HuggingFace
- **🎯 Đề xuất Sản phẩm**: Hệ thống đề xuất sản phẩm đơn giản dựa trên tương tác của người dùng
- **🔄 API E-commerce**: Các thao tác CRUD cơ bản cho sản phẩm và người dùng

## 🔧 Công nghệ sử dụng

- **⚡ FastAPI**: Framework web hiệu suất cao để xây dựng API
- **🧠 TensorFlow/Keras**: Cho phân loại hình ảnh với MobileNet
- **🤗 HuggingFace**: Khả năng NLP cho phân tích cảm xúc
- **🖌️ Python Pillow**: Xử lý hình ảnh
- **🚀 Uvicorn**: Máy chủ ASGI để chạy ứng dụng FastAPI

## 🚦 Bắt đầu

### 📋 Yêu cầu

- Python 3.8+
- pip (Trình cài đặt gói Python)

### 📥 Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/final-project-AI.git
   cd final-project-AI
   ```

2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install fastapi uvicorn tensorflow pillow python-dotenv requests
   ```

3. Thiết lập biến môi trường:
   Tạo file `.env` trong thư mục gốc với nội dung:
   ```
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   ```

### 🏃‍♂️ Chạy cục bộ

Khởi động máy chủ:
```bash
uvicorn app:app --reload
```

API sẽ khả dụng tại `http://localhost:8000`

### 🔌 Các Endpoint

#### 🖼️ Phân loại Hình ảnh
```
POST /classify_image
```
Tải lên hình ảnh để nhận kết quả phân loại sử dụng MobileNet.

#### 📝 Phân tích Đánh giá
```
POST /analyze_review
```
Phân tích cảm xúc của đánh giá sản phẩm.

#### 🎯 Đề xuất Sản phẩm
```
POST /recommend_products
```
Nhận đề xuất sản phẩm dựa trên lịch sử tương tác của người dùng.

#### 📦 Sản phẩm
```
GET /products - Liệt kê tất cả sản phẩm
GET /products/{product_id} - Lấy thông tin một sản phẩm cụ thể
POST /products - Tạo sản phẩm mới
```

#### 👥 Người dùng
```
GET /users - Liệt kê tất cả người dùng
POST /users - Tạo người dùng mới
```

#### 👆 Tương tác Người dùng
```
POST /user_interaction - Ghi lại tương tác của người dùng với sản phẩm
```

## 🚢 Triển khai

Ứng dụng được cấu hình để triển khai trên Railway sử dụng `Procfile` đã cung cấp:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

## 📜 Giấy phép

Dự án này được cấp phép theo Giấy phép MIT.
