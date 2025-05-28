import streamlit as st
import requests
from PIL import Image
import io
import base64

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Leaf Disease Detector", layout="centered")
st.title("🌿 Leaf Disease Detection App")
st.markdown("📱 **Bạn có thể chụp ảnh lá cây trực tiếp bằng điện thoại** hoặc chọn ảnh có sẵn để kiểm tra bệnh.")

# Upload ảnh
uploaded_file = st.file_uploader("📤 Upload leaf image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Leaf Image", use_container_width=True)

    if st.button("🔍 Dự đoán bệnh"):
        # Chuyển ảnh sang dạng base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Gửi ảnh đến Roboflow API
        api_url = "https://serverless.roboflow.com/infer/workflows/plant-ai-h5szi/custom-workflow-3"
        api_key = "gHkcX1drhNq5c51rwOBA"  # 🔐 THAY bằng API Key của bạn

        payload = {
            "api_key": api_key,
            "inputs": {
                "image": {
                    "type": "base64",
                    "value": img_str
                }
            }
        }

        # Gửi request
        response = requests.post(api_url, json=payload)
        print(response.json())
        result = response.json()

        try:
            result = response.json()
            prediction_data = result['outputs'][0]['predictions']
            prediction_list = prediction_data['predictions']  # danh sách các dự đoán

            if prediction_list and len(prediction_list) > 0:
                top_class = prediction_data['top']
                confidence = prediction_data['confidence']
                st.success(f"🩺 Bệnh được phát hiện: **{top_class}** (Độ tin cậy: **{confidence*100:.2f}%**)")
            else:
                st.warning("👨‍⚕️ Không phát hiện được bệnh nào. Vui lòng thử lại với ảnh rõ nét hơn.")

        except Exception as e:
            st.error("Lỗi khi phân tích kết quả phản hồi từ API.")
            st.text(f"Chi tiết lỗi: {e}")

