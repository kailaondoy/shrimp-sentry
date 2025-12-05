# 🦐 Shrimp Sentry

A Real-Time Posture Monitoring App Using YOLOv11 Pose + Streamlit

## Overview

Shrimp Sentry is a real-time computer vision application that detects unhealthy posture (jokingly referred to as “shrimping”) using pose-estimation. The system uses YOLOv11 Pose to monitor either:

- **Screen Distance (Front View)**
- **Spine Angle (Side View)**

When poor posture is detected, the app sends **push notifications** to encourage users to correct their posture.

The system runs fully in-browser through Streamlit, requires only a webcam, and provides adjustable detection thresholds.

## Features

- Real-time pose estimation using **YOLOv11n-Pose**
- Push notifications for posture warnings
- Two detection modes:

  - **Screen Distance Mode** (front-facing camera)
  - **Spine Angle Mode** (side-facing camera)

- Adjustable thresholds and cooldown timers
- Live camera preview with annotated skeleton
- Simple multi-page Streamlit interface

## Installation

### Requirements

- Streamlit
- OpenCV
- Ultralytics
- NumPy

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run streamlit_app.py
```

## Usage Guide

### 1. Home Page

Choose between:

- **Screen Distance Mode**
- **Spine Angle Mode**

Allow **camera** and **browser notification** permissions.

### 2. Screen Distance Mode

- Uses YOLOv11 Pose to detect eye coordinates
- Computes the distance between the eyes
- If the user is too close to the screen, triggers a warning

Adjustable settings:

- Notification cooldown
- Distance threshold

### 3. Spine Angle Mode

- Uses YOLOv11 Pose to detect eye coordinates
- Computes the angle between hip and shoulder keypoints
- If the user's back is slouching, triggers a warning

Adjustable settings:

- Notification cooldown
- Angle threshold

## Model Details

**YOLO11n-Pose** is a CNN object detection model used for real-time keypoint detection.
The model outputs 17 keypoints per person.
Currently the app uses the eyes, shoulders and hips keypoints to estimate posture.

- **Model:** YOLO11n-Pose (pretrained)
- **Source:** [Ultralytics](https://docs.ultralytics.com/tasks/pose/)
- **Task:** Keypoint detection
- **Reason for selection:**

  - High FPS on CPU
  - Stable skeleton keypoints
  - Easy Streamlit integration

- **Model Architecture**

  - Model Size (parameters): 2.9 Million
  - Computational Cost (FLOPs): 7.4 Billion

- **Performance Metrics:**

  - Trained on [COCO](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/coco.yaml) Pose Dataset
  - Accuracy (mAP@50-95): 50.0%
  - Accuracy (mAP@50): 81.0%
  - CPU Inference Speed (ONNX): 52.4±0.5 ms (approx. 19 FPS)

Since a pretrained model is used, no training or dataset collection was required.

## Limitations

- Requires good lighting and low occlusion for accurate detection
- Might be too heavy to use in the background with resource intensive work

## Future Improvements

- Calibration system instead of user input
- More posture types (neck tilt, shoulder alignment, etc.)

## References

YOLO Streamlit Integration: https://medium.com/@codeaigo/building-an-object-detection-app-with-yolov8-and-streamlit-d3aa416f7b6a

Keypoint Handling: https://github.com/NitinCVOrbit/-AI-Push-Up-Counter-Using-YOLOv8-Pose-Estimation/tree/main

Push Notifications: https://github.com/yunisguliyev/streamlit-notifications
