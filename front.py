import cv2
import time
import numpy as np
import streamlit as st
from ultralytics import YOLO
from streamlit_push_notifications import send_push

model = YOLO("yolo11n-pose.pt")

st.set_page_config(
    page_title="Shrimp Sentry - Screen Distance",
    page_icon="🦐",
    layout="centered",
)

NOTIFICATION_COOLDOWN = int(st.session_state.get("cooldown", 10))
DISTANCE_THRESHOLD = int(st.session_state.get("distance", 100))
run = False

st.write("# 🦐 Screen Distance Mode")

with st.container(border=True):
    st.markdown(
        """       
        * This mode monitors your posture from the front to help you keep a safe screen distance.  
        * Please place your camera so it can see your face clearly.  
        * Adjust the parameters and flip the switch below to get started!
        """
        )
    st.text_input(
        "Notification Cooldown (default 10 seconds)",
        "10",
        key="cooldown",
    )
    st.text_input(
        "Warning Screen Distance (default 100 pixels)",
        "100",
        key="distance",
    )
    run = st.toggle('Run Shrimp Sentry')

FRAME_IMAGE = st.image([])
FRAME_STATUS = st.empty()

with st.spinner("Loading..."):
    cap = cv2.VideoCapture(0)

last_notification_time = 0

if run:
    send_push(
        title="🦐 Shrimp Sentry Activated!",
        body="You'll receive alerts like this when bad posture is detected. Stay safe and maintain good posture!",
        icon_path="",
        sound_path="good.mp3",
        only_when_on_other_tab=False
    )

def calculate_distance(p1, p2):
    """Calculates the distance between two points p1 and p2"""
    return np.linalg.norm(p1 - p2)

def bad_posture(keypoints):
    """Determines if the user is too close to the screen based on eye separation"""
    
    if keypoints is None or keypoints.shape[0] < 3:
        return False
    
    kpts = keypoints.cpu().numpy() if hasattr(keypoints, 'cpu') else keypoints
    
    left_eye = kpts[1]
    right_eye = kpts[2]
    
    return calculate_distance(left_eye, right_eye) > DISTANCE_THRESHOLD

while run:
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to grab frame")
        break

    results = model(frame)
    annotated_frame = results[0].plot(boxes=False)
    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    FRAME_IMAGE.image(annotated_frame, width="stretch")
    
    if results[0].keypoints is not None:
        if bad_posture(results[0].keypoints.xy[0]):
            FRAME_STATUS.warning("🦐 Bad posture detected! Sit up straight.")
            current_time = time.time()
            if current_time - last_notification_time > NOTIFICATION_COOLDOWN:
                send_push(
                    title="🦐 Shrimp Alert!",
                    body=" Bad posture detected! Sit up straight.",
                    icon_path="",
                    sound_path="bad.mp3",
                    only_when_on_other_tab=False
                    )
                last_notification_time = current_time
        else:
            FRAME_STATUS.success("🧘 Good posture! Keep it up.")
    
cap.release()