import cv2
import time
import numpy as np
import streamlit as st
from ultralytics import YOLO
from streamlit_push_notifications import send_push

model = YOLO("yolo11n-pose.pt")

st.set_page_config(
    page_title="Shrimp Sentry - Spine Angle",
    page_icon="🦐",
    layout="centered",
)

NOTIFICATION_COOLDOWN = int(st.session_state.get("cooldown", 10))
ANGLE_THRESHOLD = int(st.session_state.get("angle", 10))
st.write("# 🦐 Spine Angle Mode")

with st.container(border=True):
    st.markdown(
        """       
        * This mode monitors your posture from the side to help you maintain a straight back.  
        * Please place your camera so it can see the your hips and shoulders clearly.  
        * Adjust the parameters and flip the switch below to get started!
        """
        )
    st.text_input(
        "Notification Cooldown (default 10 seconds)",
        "10",
        key="cooldown",
    )
    st.text_input(
        "Warning Back Angle (default 10 degrees)",
        "10",
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

def calculate_angle(p1, p2, p3):
    """Calculates the angle at point p2 formed by points p1 and p3"""
    v1 = p1 - p2
    v2 = p3 - p2
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
    
    return angle

def bad_posture(keypoints):
    """Determines if the user is slouching based on keypoints"""
    
    if keypoints is None or keypoints.shape[0] < 13:
        return False
    
    kpts = keypoints.cpu().numpy() if hasattr(keypoints, 'cpu') else keypoints
    
    left_shoulder = kpts[5]
    right_shoulder = kpts[6]
    left_hip = kpts[11]
    right_hip = kpts[12]
    
    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    hip_midpoint = (left_hip + right_hip) / 2
    reference_point = np.array([hip_midpoint[0], hip_midpoint[1] - 1])
    
    return calculate_angle(shoulder_midpoint, hip_midpoint, reference_point) > ANGLE_THRESHOLD

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