import cv2 

know_distance = 30
know_width = 14.3

GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length

def Distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance

def face_data(image):
    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for(x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), WHITE, 1)
        face_width = w

    return face_width    

cap = cv2.VideoCapture(0)

# Capture a frame for reference image
ret, ref_image = cap.read()
ref_image_face_width = face_data(ref_image)

# Display the reference image
cv2.imshow("ref_image.png", ref_image)

# Calculate the focal length
Focal_length_found = FocalLength(know_distance, know_width, ref_image_face_width)

while True:
    _, frame = cap.read()

    face_width_in = face_data(frame)

    # Calculate the distance using the focal length and face width in the frame
    if face_width_in != 0:
        distance = Distance_finder(Focal_length_found, know_width, face_width_in)
        print(f"Distance: {distance} inches")

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
