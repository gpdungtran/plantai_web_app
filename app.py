import streamlit as st
import requests
from PIL import Image
import io
import base64
import matplotlib.pyplot as plt

# Streamlit UI configuration
st.set_page_config(page_title="Leaf Disease Classifier", layout="centered")
st.title("🌿 Leaf Disease Detection")
st.markdown("📱 You can **capture a photo** using your phone or upload an existing leaf image for disease detection.")

# Function to display image with fake bounding box and label
def show_prediction(image, label, confidence):
    fig, ax = plt.subplots()
    ax.imshow(image)

    # Draw a red rectangle around the full image to mimic a bounding box
    width, height = image.size
    ax.add_patch(plt.Rectangle((0, 0), width, height, edgecolor='red', facecolor='none', linewidth=3))

    # Add label and confidence at the top-left
    ax.text(5, 5, f"{label} {confidence:.0f}%", fontsize=12,
            bbox=dict(facecolor='red', alpha=0.8), color='white')

    ax.axis('off')
    st.pyplot(fig)

# Upload image
uploaded_file = st.file_uploader("📤 Upload a leaf image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    #st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)
    st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)

    if st.button("🔍 Predict Disease"):
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Roboflow API details
        api_url = "https://serverless.roboflow.com/infer/workflows/plant-ai-h5szi/custom-workflow-3"
        api_key = "gHkcX1drhNq5c51rwOBA"  # ← Replace this with your actual API key

        payload = {
            "api_key": api_key,
            "inputs": {
                "image": {
                    "type": "base64",
                    "value": img_str
                }
            }
        }

        # Send request
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result = response.json()
            predictions = result.get("predictions", [])
            if predictions:
                pred = predictions[0]
                label = pred["class"]
                confidence = pred["confidence"] * 100
                show_prediction(image, label, confidence)
            else:
                st.warning("⚠️ No prediction returned.")
        else:
            st.error(f"❌ API Error: {response.status_code} - {response.text}")

