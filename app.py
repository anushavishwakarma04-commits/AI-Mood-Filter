import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="AI Mood Filter", layout="centered")

st.title("🎨 Real-Time AI Mood Filter")
st.write("Upload an image and adjust the 'Mood' sliders to see instant changes.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV format
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # 2. Sidebar Controls (The "Real-Time" Triggers)
    st.sidebar.header("Filter Settings")
    brightness = st.sidebar.slider("Brightness", -100, 100, 0)
    contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0)
    vintage = st.sidebar.slider("Vintage (Warmth)", 0, 100, 0)
    sharpness = st.sidebar.checkbox("AI Sharpness Boost")

    # 3. Processing Logic
    # Apply Brightness & Contrast
    processed_img = cv2.convertScaleAbs(img_array, alpha=contrast, beta=brightness)

    # Apply "Vintage" Mood (Adding a warm yellow/orange tint)
    if vintage > 0:
        # Increase Red and Green channels slightly to create warmth
        processed_img[:, :, 0] = cv2.add(processed_img[:, :, 0], vintage) # Red
        processed_img[:, :, 1] = cv2.add(processed_img[:, :, 1], int(vintage/2)) # Green

    # Apply AI Sharpness (Unsharp Masking)
    if sharpness:
        gaussian_blur = cv2.GaussianBlur(processed_img, (7, 7), 2)
        processed_img = cv2.addWeighted(processed_img, 1.5, gaussian_blur, -0.5, 0)

    # 4. Display Result
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)
    with col2:
        st.subheader("Filtered")
        st.image(processed_img, use_container_width=True)

    # 5. Download Button (Fixed)
    import io
    
    # Processed image ko memory mein save karne ke liye (Download ke liye)
    result_pil = Image.fromarray(processed_img)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Filtered Image",
        data=byte_im,
        file_name="mood_filter.png",
        mime="image/png"
    )