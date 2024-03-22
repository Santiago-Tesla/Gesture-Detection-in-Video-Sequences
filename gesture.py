import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2
import mediapipe as mp
import numpy as np
import time

# Buffer class to store a list of values over a specified time window
class BufferList:
    def __init__(self, buffer_time, default_value=0):
        self.buffer = [default_value for _ in range(buffer_time)]

    def push(self, value):
        self.buffer.pop(0)
        self.buffer.append(value)

    def max(self):
        return max(self.buffer)

    def min(self):
        buffer = [value for value in self.buffer if value]
        if buffer:
            return min(buffer)
        return 0

# Input video file name
file_name = "input1.mp4"

# MediaPipe initialization
mp_pose = mp.solutions.pose

# Landmarks to track for gesture detection
selected_landmarks = [23, 24]

# Buffer parameters
buffer_time = 80
center_y = BufferList(buffer_time)
center_y_up = BufferList(buffer_time)
center_y_down = BufferList(buffer_time)
center_y_pref_flip = BufferList(buffer_time)
center_y_flip = BufferList(buffer_time)

# Initializations
cy_max = 100
cy_min = 100
flip_flag = 250
prev_flip_flag = 250
count = 0

# Open video file
cap = cv2.VideoCapture(file_name)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    file_name.replace(".mp4", "_output.mp4"),
    fourcc,
    20.0,
    (int(cap.get(3)), int(cap.get(4))),
)

# Record the time of the last count update
last_count_update = time.time()

# Main loop to process video frames
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Get image dimensions
        image_height, image_width, _ = image.shape

        # Convert image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process pose estimation
        results = pose.process(image_rgb)

        # Convert image back to BGR
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = [
                (lm.x * image_width, lm.y * image_height)
                for i, lm in enumerate(results.pose_landmarks.landmark)
                if i in selected_landmarks
            ]
            cx = int(np.mean([x[0] for x in landmarks]))
            cy = int(np.mean([x[1] for x in landmarks]))

            landmarks = [
                (lm.x * image_width, lm.y * image_height)
                for i, lm in enumerate(results.pose_landmarks.landmark)
                if i in [11, 12]
            ]
            cy_shoulder_hip = cy - int(np.mean([x[1] for x in landmarks]))
        else:
            cx = 0
            cy = 0
            cy_shoulder_hip = 0

        # Smooth out data using buffer lists
        cy = int((cy + center_y.buffer[-1]) / 2)
        center_y.push(cy)

        cy_max = 0.5 * cy_max + 0.5 * center_y.max()
        center_y_up.push(cy_max)

        cy_min = 0.5 * cy_min + 0.5 * center_y.min()
        center_y_down.push(cy_min)

        prev_flip_flag = flip_flag
        center_y_pref_flip.push(prev_flip_flag)

        # Gesture detection logic
        dy = cy_max - cy_min
        if dy > 0.4 * cy_shoulder_hip:
            if cy > cy_max - 0.55 * dy and flip_flag == 150:
                flip_flag = 250
            if 0 < cy < cy_min + 0.35 * dy and flip_flag == 250:
                flip_flag = 150
        center_y_flip.push(flip_flag)

        # Update count if gesture detected
        if prev_flip_flag < flip_flag:
            count = count + 1
            last_count_update = time.time()  # Update the time of the last count update

        # Display "DETECTED" text if gesture detected within last 1 second
        if time.time() - last_count_update <= 1:
            cv2.putText(
                image,
                "DETECTED",
                (int(image_width * 0.8), int(image_height * 0.1)),  # Adjusted coordinates
                cv2.FONT_HERSHEY_SIMPLEX,
                2,  # Font scale
                (0, 255, 0),  # Color (green)
                3,  # Thickness
            )

        # Display the annotated image
        cv2.imshow("MediaPipe Pose", image)
        out.write(image)

        # Exit loop if 'Esc' key is pressed
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release video capture and writer objects
cap.release()
out.release()
cv2.destroyAllWindows()
