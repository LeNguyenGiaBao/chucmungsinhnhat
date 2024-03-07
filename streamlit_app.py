from datetime import datetime

import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper

from utils import read_event_config

cropped_img = None
config_event = None
st.set_page_config(page_title="Chúc Mừng Sinh Nhật", page_icon="🎂", layout="wide")

# header
_, col, _ = st.columns([1, 4, 1])
with col:
    st.markdown(
        '<h1 style="text-align: center;">Chúc Mừng Sinh Nhật 🎉 🎂</h1>',
        unsafe_allow_html=True,
    )


# functional button
left_column, right_column = st.columns(2)
with left_column:
    event = st.selectbox("Template", ("template_1", ""))
    if event:
        config_event = read_event_config(event)

with right_column:
    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"]
    )

# body
st.markdown("---")
original_image_block, result_image_block = st.columns(2)

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    if img:
        st.session_state["original_image"] = img
        with original_image_block:
            cropped_img = st_cropper(
                img,
                realtime_update=True,
                box_color='#74ee15',
                aspect_ratio=None,
            )

if cropped_img:
    cropped_img = cropped_img.resize((config_event["width"], config_event["height"]))
    mockup_image = Image.open(config_event["image_path"])
    result_image = mockup_image.copy()
    result_image.paste(cropped_img, (config_event["x"], config_event["y"]))
    st.session_state["result_image"] = result_image
    with result_image_block:
        st.image(result_image)

if "result_image" in st.session_state:
    now = datetime.now()
    current_time = now.strftime("%y_%m_%d_%H_%M_%S")
    result_path = "{}.jpg".format(current_time)
    result_image = st.session_state["result_image"]
    result_image.save(result_path)
    with open(result_path, "rb") as f:
        with right_column:
            download_button = st.download_button(
                label="Download Image",
                data=f,
                file_name="./{}.jpg".format(event),
                mime="image/jpeg",
            )
