import face_recognition
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO

# Credit to adam geitgey for the face_recognition library and example code
# Method to turn RPi camera on as a video source: 'sudo modprobe bcm2835-v4l2'

class facerec:
    video_capture = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L) # Setup camera as video source in a way that it can be accessed by OpenCV

    # Load images for each face into separate arrays (this is to allow you to add more than one image per person)
    # Images here are in 320x240 and are centered on the face to reduce computational load
    # Images are also trained using the face_recognition library at this step
    person1_image = face_recognition.load_image_file("images/person1_small.jpg")
    person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

    person2_image = face_recognition.load_image_file("images/person2_small.jpg")
    person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        person1_face_encoding,
        person2_face_encoding
    ]
    known_face_names = [
        "person1",
        "person2"
    ]

    # Initialize all the variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    # LED pins
    green = 21
    red = 20

    # GPIO setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(red, GPIO.OUT)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(red, GPIO.LOW)

    # Method to toggle the red and green LEDs
    def green_toggle():
        GPIO.output(green, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(green, GPIO.LOW)

    def red_toggle():
        GPIO.output(red, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(red, GPIO.LOW)

    # Debug statement to show that the program made it past the initialization and training phase
    # print("Process Initialized, Running")

    while True:
        time.sleep(0.05) # Adjust the frame rate of the camera and with it all the logic.
        ret, frame = video_capture.read() # Read frame from camera

        if not ret:
            time.sleep(1)
            continue
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Resize frame

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the arrays of known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If there is no match, just use the closest face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                # If there is a match, enable green LED and set name, otherwise red LED
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    green_toggle()
                else:
                    red_toggle()
                face_names.append(name)

        # Skip processing every other frame to improve performance
        process_this_frame = not process_this_frame

        # Scale output to image to be full resolution from the 25% res we processed earlier
        for (top, right, bottom, left), name in zip(face_locations, face_names):

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a white box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            # Draw a label with a name below the face (why is there only one cv2 font?!)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        # Convert image to jpg
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Save the image
        with open('static/frame.jpg', 'wb') as f:
            f.write(jpeg.tobytes())

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
