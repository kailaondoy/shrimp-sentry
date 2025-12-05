import streamlit as st
from streamlit_push_notifications import send_push

st.set_page_config(
    page_title="Shrimp Sentry",
    page_icon="🦐",
    layout="centered",
)

st.write("# 🦐 Welcome to Shrimp Sentry!")
st.image("https://www.wikihow.com/images/thumb/7/7d/Shrimp-Posture-Step-1.jpg/v4-728px-Shrimp-Posture-Step-1.jpg", width="stretch")
st.write("")
with st.container(border=True):
    st.markdown(
        """
        Welcome! This is a simple app to demonstrate pose estimation using YOLOv11 Pose.
        
        This app runs in the background and sends you push notifications when it detects shrimp posture.
        You can choose to check your screen distance or spine angle.
        🔗 [What is shrimp posture?](https://www.wikihow.com/Shrimp-Posture)
        
        🌿 Maintain good posture for a healthier lifestyle!
        """
    )
    st.info("Please allow camera and notification permissions for the best experience.")

st.write("### 🔎 Choose Detection Mode")

col1, col2 = st.columns(2, border=True)

with col1:
    st.markdown(
        """
        ### 💻 Screen Distance
        
        This mode monitors your posture from the front to help you keep a safe screen distance.
        """
        )
    if st.button("Try Screen Distance"):
        st.switch_page("front.py")

with col2:
    st.markdown(
        """
        ### 🦴 Spine Angle
        
        This mode monitors your posture from the side to help you maintain a straight back.
        """
        )
    if st.button("Try Spine Angle"):
        st.switch_page("side.py")

