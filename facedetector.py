import cv2
import sys
from datetime import datetime

# cascPath = sys.argv[1]
# print(cascPath)
cascPath = "haarcascades/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
# Used to take pictures when a face is detected in the camera
cam_capture = cv2.cv.CaptureFromCAM(0)

faces_count = 0

# Initializes start_time just in case
start_time = datetime.now()

# minutes_to_refresh holds the number of minutes the program should wait to start taking
# snapshots again after taking them
minutes_to_refresh = 1

# Number of snapshots that will be taken when a face is detected
snapshots = 3

# Creates the snapshots folder in case it doesn't exist yet
if not os.path.isdir("snapshots"):
    os.makedirs("snapshots")

while True:

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Takes three pictures when a face is detected by the camera
        if faces_count >= 1 and faces_count <= snapshots:
            img = cv2.cv.QueryFrame(cam_capture)
            cv2.cv.SaveImage('snaptshots/snapshot'+str(faces_count)+'.jpg', img)
            # Stores the time when faces_count reached its max value
            start_time = datetime.now()
        
        faces_count += 1

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    end = datetime.now()
    time_difference = datetime.strptime(start_time.strftime('%b %d %H:%M:%S %Y'), "%b %d %H:%M:%S %Y") - datetime.strptime(end.strftime('%b %d %H:%M:%S %Y'), "%b %d %H:%M:%S %Y")
    # Resets the faces_count to 1, minutes_to_refresh minutes after taking the third snapshot
    if str(time_difference) == "-1 day, 23:"+str(59 - minutes_to_refresh)+":59":
        faces_count = 1

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
