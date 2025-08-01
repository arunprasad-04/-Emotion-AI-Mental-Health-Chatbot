import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
from emotion_storage import save_emotion_to_json

# Load pre-trained face detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load the trained emotion recognition model
model = load_model("emotion_model.h5")

# Define emotion labels
emotion_labels = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale (for better face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                h, w, c = frame.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)  
    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = gray[y:y + h, x:x + w]

        # Resize the face to match the model input
        resized_face = cv2.resize(face_roi, (48, 48))
        resized_face = np.expand_dims(resized_face, axis=0)
        resized_face = np.expand_dims(resized_face, axis=-1)  # Add channel dimension
        resized_face = resized_face / 255.0  # Normalize pixel values

        # Predict emotion
        predictions = model.predict(resized_face)
        max_index = np.argmax(predictions[0])
        detected_emotion = emotion_labels[max_index]

        # Save the detected emotion to JSON
        save_emotion_to_json(detected_emotion)

        # Draw a GREEN rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the detected emotion on screen
        cv2.putText(frame, f"Emotion: {detected_emotion}", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show the output
    cv2.imshow("Emotion Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
