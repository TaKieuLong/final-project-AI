import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from typing import List, Optional
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from io import BytesIO
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise Exception("Chưa thiết lập HUGGINGFACE_API_KEY trong file .env")


app = FastAPI(title="E-commerce AI Integrated API")

# Cấu hình CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load mô hình MobileNet của TensorFlow
model = MobileNet(weights='imagenet')

@app.post("/classify_image")
async def classify_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents)).convert("RGB")
        img = img.resize((224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]
        results = [{"label": label, "description": desc, "confidence": float(conf)} 
                   for (label, desc, conf) in predictions]
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý ảnh: {str(e)}")

@app.post("/analyze_review")
async def analyze_review(request: dict):

    review = request.get("review")  
    if not review:
        raise HTTPException(status_code=400, detail="Thiếu nội dung review")

    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": review}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Lỗi API Hugging Face: {response.text}")

    result = response.json()
    return {"analysis": result}

class RecommendationRequest(BaseModel):
    user_id: int
    interactions: List[int] 

# Giả lập cơ sở dữ liệu sản phẩm
products_db = [
    {"id": 1, "name": "Product A", "price": 100.0, "description": "Mô tả sản phẩm A"},
    {"id": 2, "name": "Product B", "price": 150.0, "description": "Mô tả sản phẩm B"},
    {"id": 3, "name": "Product C", "price": 200.0, "description": "Mô tả sản phẩm C"},
    {"id": 4, "name": "Product D", "price": 250.0, "description": "Mô tả sản phẩm D"},
    {"id": 5, "name": "Product E", "price": 300.0, "description": "Mô tả sản phẩm E"},
]

@app.post("/recommend_products")
async def recommend_products(request: RecommendationRequest):

    interacted_ids = set(request.interactions)

    recommended = [p for p in products_db if p["id"] not in interacted_ids]

    if not recommended:
        recommended = products_db
    return {"user_id": request.user_id, "recommendations": recommended}

# --- Sản phẩm (Products) ---
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    description: Optional[str] = None

@app.get("/products")
async def get_products():
    return {"products": products_db}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return product

@app.post("/products")
async def create_product(product: Product):
    product.id = len(products_db) + 1
    products_db.append(product.dict())
    return {"message": "Sản phẩm đã được tạo", "product": product}

class InteractionRequest(BaseModel):
    user_id: int
    product_id: int
    action: str

@app.post("/user_interaction")
async def record_interaction(request: InteractionRequest):
    return {
        "message": f"Đã ghi nhận hành động '{request.action}' cho sản phẩm {request.product_id} của người dùng {request.user_id}"
    }

# --- Người dùng (Users) ---
users_db = []

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str

@app.get("/users")
async def get_users():
    return {"users": users_db}

@app.post("/users")
async def create_user(user: User):
    user.id = len(users_db) + 1
    users_db.append(user.dict())
    return {"message": "Người dùng đã được tạo", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
