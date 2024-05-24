import threading
import winsound
import cv2
import imutils

# setting up camera
cap = cv2.VideoCapture(0)

# resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# starting frame
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

# setting up alarm
alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        else:
            print("ALARM")
            winsound.Beep(2500, 1000)
    alarm = False

while True:
    # Capture frame-by-frame
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        # Process the frame for alarm mode
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        # Compute difference between current frame and initial frame
        difference = cv2.absdiff(start_frame, frame_bw)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw  # Update start frame

        # Check the amount of motion
        if threshold.sum() > 300:
            print(threshold.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("cam", threshold)  # Display threshold image
    else:
        cv2.imshow("cam", frame)  # Display original frame

    # Trigger the alarm if counter exceeds the threshold
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode  # Toggle alarm mode
        alarm_counter = 0            # Reset alarm counter
    if key_pressed == ord("q"):
        alarm_mode = False  # Disable alarm mode
        break

cap.release()
cv2.destroyAllWindows()
