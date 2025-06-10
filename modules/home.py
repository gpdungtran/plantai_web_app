import streamlit as st
import requests
import io
import base64
from modules import feedback # Import module feedback
from modules import diagnose
# Removed unused imports: from datetime import datetime, import os

def save_true(username, img_str, disease_response, torf):
    feedback.save_feedback(username, img_str, disease_response, torf)
    st.success("🎉 Cảm ơn bạn đã phản hồi!")

def save_false(username, img_str, disease_response, torf):
    feedback.save_feedback(username, img_str, disease_response, torf)
    st.success("🎉 Cảm ơn bạn đã phản hồi!")


def show_home(username):
    from PIL import Image

    # Cấu hình giao diện Streamlit
    st.markdown("📱 Bạn có thể chụp **một** bức ảnh hoặc tải lên **một** hình ảnh của chiếc lá trên cây trồng bạn muốn kiểm tra bằng cách bấm vào nút **Browse files**, rồi chọn hình ảnh bạn muốn tải lên")
    st.markdown("Sau đó tên chủng loài cây và các loại bệnh được dự đoán cùng xác suất chính xác của chúng sẽ được **xuất hiện trên màn hình**, chú ý nhé!!")

    # Upload ảnh
    uploaded_file = st.file_uploader("📤 Upload leaf image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="🖼️ Uploaded Leaf Image", use_container_width=True)

        if st.button("🔍 Dự đoán bệnh"):
            # Chuyển ảnh sang dạng base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # ---------- STEP 1: Phân loại loại cây ----------
            st.subheader("🧬 Nhận diện loại lá cây...")
            # 👉 THAY bằng workflow đúng và API KEY đúng nếu cần
            leaf_type_url = "https://serverless.roboflow.com/infer/workflows/i30/leaf-type"  
            leaf_type_key = "Sq8AwQQ64AZEGfvmjn03"  

            leaf_payload = {
                "api_key": leaf_type_key,
                "inputs": {
                    "image": {
                        "type": "base64",
                        "value": img_str
                    }
                }
            }

            leaf_response_raw = requests.post(leaf_type_url, json=leaf_payload)
            leaf_result = leaf_response_raw.json()
            
            try:
                # Lấy dữ liệu từ cấu trúc JSON của Roboflow Workflow
                # Đảm bảo an toàn khi truy cập các khóa lồng nhau
                prediction_data = leaf_result.get('outputs', [{}])[0].get('predictions', {})
                prediction_list = prediction_data.get('predictions', [])

                if not prediction_list:
                    st.error("❌ Không xác định được loại cây. Hãy thử lại với ảnh rõ hơn.")
                    st.stop()

                # Lấy class có độ tin cậy cao nhất
                top_class_pred = sorted(prediction_list, key=lambda x: x['confidence'], reverse=True)[0]
                top_class = top_class_pred['class']
                leaf_type = top_class.split("_")[0]  # ví dụ: 'coffee_leaf_healthy' -> 'coffee'

                st.success(f"📗 Loại lá: **{leaf_type.upper()}**")

            except Exception as e:
                st.error("❌ Không xác định được loại cây. Hãy thử lại với ảnh rõ hơn hoặc kiểm tra API key/URL.")
                st.exception(e) # Hiển thị chi tiết lỗi để debug
                st.stop()

            # ---------- STEP 2: Dự đoán bệnh theo loại cây ----------
            st.subheader("🦠 Phát hiện bệnh...")

            # Cấu hình API cho từng loại cây
            api_config = {
                "durian": {
                    "url": "https://serverless.roboflow.com/infer/workflows/i30/durian-deseases-detection",
                    "key": "Sq8AwQQ64AZEGfvmjn03"
                },
                "lemon": {
                    "url": "https://serverless.roboflow.com/infer/workflows/i30/lemon-deseases-detection",
                    "key": "Sq8AwQQ64AZEGfvmjn03"
                },
                "coffee": {
                    "url": "https://serverless.roboflow.com/infer/workflows/i30/coffee-deseases-detection",
                    "key": "Sq8AwQQ64AZEGfvmjn03"
                }
            }
            
            if leaf_type not in api_config:
                st.error(f"❌ Chưa hỗ trợ bệnh cho loại cây: **{leaf_type.upper()}**")
                st.stop()

            disease_payload = {
                "api_key": api_config[leaf_type]['key'],
                "inputs": {
                    "image": {
                        "type": "base64",
                        "value": img_str
                    }
                }
            }

            disease_response_raw = requests.post(api_config[leaf_type]['url'], json=disease_payload)
            disease_response = disease_response_raw.json()
            
            try:
                # Lấy dữ liệu từ cấu trúc JSON của Roboflow Workflow
                # Đảm bảo an toàn khi truy cập các khóa lồng nhau
                preds = disease_response.get('outputs', [{}])[0].get('predictions', {}).get('predictions', [])
                
                if preds:
                    st.subheader("📌 Các bệnh được phát hiện trên lá:")
                    # Hiển thị từng bệnh và độ tin cậy
                    for pred in preds:
                        disease_class = pred['class']
                        confidence = pred['confidence']
                        st.markdown(f"✅ **{disease_class}** ({confidence*100:.2f}%)")
                        diagnose.show_disease_info(disease_class)
                    st.markdown("---") # Đường kẻ phân cách
                    st.subheader("❓ Kết quả có chính xác không?")
                    
                    # Nút phản hồi cho trường hợp có bệnh
                    
                else:
                    st.info("ℹ️ Không phát hiện được bệnh trên lá này.")
                    st.markdown("---")
                    st.subheader("❓ Kết quả có chính xác không?")
                    # Nút phản hồi cho trường hợp không có bệnh
                    

            except Exception as e:
                st.error("⚠️ Lỗi khi xử lý kết quả nhận diện bệnh. Vui lòng kiểm tra lại cấu hình API.")
                st.exception(e) # Hiển thị chi tiết lỗi để debug


            col1, col2 = st.columns(2)
            col1.button(
                "👍 Đúng",
                key="correct_btn",
                on_click=save_true,                              # <-- pass function, no ()
                args=(
                    st.session_state.get("username", "anon"),
                    img_str,
                    disease_response,
                    True
                )
            )

            col2.button(
                "👎 Sai (có bệnh)",
                key="no_disease_incorrect_btn",
                on_click=save_false,                             # <-- pass function, no ()
                args=(
                    st.session_state.get("username", "anon"),
                    img_str,
                    disease_response,
                    False
                )
            )
