# Gesture-Detection-in-Video-Sequences

### Data Processing:
The data processing stage involves preparing the input video frames for analysis. Here's how it's done in the provided code:

1. **Reading Video Frames**: The code reads each frame of the input video file using OpenCV's `VideoCapture` object.
2. **Converting Color Space**: Each frame is converted from BGR to RGB color space to match the format required by the MediaPipe Pose model.
3. **Pose Estimation**: The MediaPipe Pose model is utilized to estimate human poses in each frame.
4. **Landmark Extraction**: Landmarks are extracted from the pose estimation results, specifically landmarks corresponding to the selected body parts, such as shoulders and hips.
5. **Data Aggregation**: The code calculates relevant features from the extracted landmarks, such as the centroid and the difference between shoulder and hip positions.
6. **Data Buffering**: A buffer list is used to smooth out fluctuations in the calculated features over time, making the analysis more robust.

### Model Selection/Development:
The pose detection model used in this code is the MediaPipe Pose model, provided by the `mediapipe` library. This model is chosen for its accuracy and efficiency in detecting human poses in real-time. It offers a pre-trained model that can detect various key landmarks on the human body, making it suitable for gesture recognition tasks.

### Detection Algorithm:
The detection algorithm in this code aims to identify a specific gesture based on the relative positions of certain body landmarks over time. Here's how it works:

1. **Feature Calculation**: Relevant features, such as the centroid and the difference between shoulder and hip positions, are calculated from the pose landmarks.
2. **Data Smoothing**: The calculated features are smoothed using buffer lists to reduce noise and improve stability.
3. **Gesture Detection Logic**: Based on predefined criteria, such as the position of the centroid and the difference between shoulder and hip positions, the algorithm determines whether a specific gesture is being performed.
4. **Thresholding and Flag Management**: Threshold values and flags are used to track changes in gesture state over time, ensuring accurate detection.

### Annotation:

1. **Dynamic Text Display**: The annotation mechanism dynamically displays the text "DETECTED" on video frames where the desired gesture is detected.
  
2. **Temporal Control**: To ensure that the annotation appears only when the action is ongoing, a temporal control mechanism is employed. Specifically, if one second hasn't passed since the last update indicating gesture detection, the text is displayed on the video frame.

3. **Time Window**: The time window for displaying the annotation is precisely set to one second. This duration can be adjusted based on the specific requirements of the application or analysis.

4. **Update Trigger**: Each time the gesture is detected, the timestamp of the detection event is recorded. Subsequently, when processing subsequent frames, the code checks whether one second has passed since the last detection event.

5. **Conditional Display**: If the time elapsed since the last detection event is within the defined time window (one second), the "DETECTED" text is overlaid onto the video frame. Otherwise, no annotation is displayed, indicating that the gesture is not currently being performed.

6. **Clear Visibility**: The text is positioned strategically, typically at the top-right corner of the video frame, ensuring clear visibility without obstructing the content.

7. **Font Size and Style**: To enhance visibility and emphasis, the text is displayed in a larger font size and in bold, making it clearly distinguishable against the background.

8. **Dynamic Feedback**: This dynamic annotation provides real-time feedback to the viewer, indicating when the desired gesture is being executed without the need for manual inspection or analysis of the video stream.
