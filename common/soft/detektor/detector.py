import cv2

face_cascade_db = cv2.CascadeClassifier("tank.xml") 

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1640,
    capture_height=1232,
    display_width=320,
    display_height=240,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink "
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

while True:
    
    success, img = cap.read()
    
    img = cv2.resize(img, (320, 240))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
       
    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 50, 0)

    for (x, y, w, h) in faces: cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
                                             
    cv2.imshow('name of window', img) 
    
    if cv2.waitKey(1) & 0xff == ord('q'):  break
    
cap.release() 
cv2.destroyAllWindows() 
