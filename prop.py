#ใส่ prop ให้ใบหน้า

import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🧢 AI ใส่หมวก / แว่น / หูแมว บนใบหน้า")

uploaded_file = st.file_uploader("📸 อัปโหลดภาพใบหน้า", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]

        # เลือก accessory
        accessory_option = st.selectbox("เลือกของตกแต่ง", ["หมวก", "แว่นตา", "หูแมว"])
        accessory_path = f"assets/{accessory_option}.png"
        accessory = Image.open(accessory_path).convert("RGBA")

        # ปรับขนาด accessory ให้พอดีกับใบหน้า
        accessory_width = w
        accessory_height = int(accessory.height * (accessory_width / accessory.width))
        accessory = accessory.resize((accessory_width, accessory_height))

        # วาง accessory บนใบหน้า
        img_pil = Image.fromarray(img).convert("RGBA")
        if accessory_option == "หมวก":
            position = (x, y - accessory_height + 20)
        elif accessory_option == "แว่นตา":
            position = (x, y + int(h / 100))
        else:  # หูแมว
            position = (x, y - accessory_height + 35)
        img_pil.paste(accessory, position, mask=accessory)

        st.image(img_pil, caption="🎉 ภาพที่ตกแต่งแล้ว", use_container_width=True)

        # ดาวน์โหลดภาพ
        from io import BytesIO
        buf = BytesIO()
        img_pil.save(buf, format="PNG")
        st.download_button("📥 ดาวน์โหลดภาพ", data=buf.getvalue(), file_name="decorated_image.png", mime="image/png")
    else:
        st.warning("ไม่พบใบหน้าในภาพ กรุณาอัปโหลดภาพใหม่")
st.info ("made by Thanuchsit Somnuk")        
