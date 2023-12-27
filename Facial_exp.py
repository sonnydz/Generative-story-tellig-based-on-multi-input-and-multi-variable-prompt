import cv2
import numpy as np
from keras.models import load_model
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


model = load_model('facial_expression_model.h5')


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
      
        roi_gray = gray[y:y + h, x:x + w]

      
        roi_gray = cv2.resize(roi_gray, (48, 48))

      
        roi_gray = roi_gray / 255.0

    
        roi_gray = np.reshape(roi_gray, (1, 48, 48, 1))

       
        prediction = model.predict(roi_gray)

        emotion_index = np.argmax(prediction)
      
        emotion = emotions[emotion_index]

     
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if emotion == 'sad':
            print("Student is confused. Notify the teacher!")

   
    cv2.imshow('Real-time Facial Expression Analysis', frame)

  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
