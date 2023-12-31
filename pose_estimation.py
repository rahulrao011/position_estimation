import mediapipe as mp
import cv2
import numpy as np
import time 
from get_angles import get_angles


'''
### STATUS: WORKS SUCCESSFULLY AS A BICEP CURL TRACKER (GRANTED THE BICEP CURLS AREN'T TOO FAST)
### USES ANGLES TO DETERMINE IF A BICEP CURL HAS BEEN COMPLETED AND IT TRACKS HOW MANY BICEP CURLS HAVE BEEN COMPLETED

### Youtube project tutorial: https://www.youtube.com/watch?v=06TE_U21FK4
'''

### CONSTANTS + VARIABLES:

# bicep curl counter
counter = 0

# either True or False
leftBicepStage = None
leftShoulderStage = None

rightBicepStage = None
rightShoulderStage = None


finishedLeftPunch = False
finishedRightPunch = False



# get mp tools like drawing to opencv and the holistic model (which can track a whole bunch on things)
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

relevant_landmarks_numerical = [
    # left side
    mp_holistic.PoseLandmark.LEFT_SHOULDER.value,
    mp_holistic.PoseLandmark.LEFT_ELBOW.value,
    mp_holistic.PoseLandmark.LEFT_WRIST.value,
    mp_holistic.PoseLandmark.LEFT_HIP.value,

    # right side
    mp_holistic.PoseLandmark.RIGHT_SHOULDER.value,
    mp_holistic.PoseLandmark.RIGHT_ELBOW.value,
    mp_holistic.PoseLandmark.RIGHT_WRIST.value,
    mp_holistic.PoseLandmark.RIGHT_HIP.value,
]
print(relevant_landmarks_numerical)


# get opencv camera
cap = cv2.VideoCapture(0)

# get camera dimensions
width = int(cap.get(3))
height = int(cap.get(4))

print(f'Width: {width}')
print(f'Height: {height}')







# Define states

#left state
WAITING_FOR_LEFT_PUNCH = 0
LEFT_PUNCH_DETECTED = 1

#right state
WAITING_FOR_RIGHT_PUNCH = 0
RIGHT_PUNCH_DETECTED = 1

# Initialize state
left_state = WAITING_FOR_LEFT_PUNCH
right_state = WAITING_FOR_RIGHT_PUNCH
# ... (rest of your code)


    # ... (rest of your code)




# initiating holistic model
# context manager: it's configuring the Holistic object with certain minimum detection and tracking confidence levels.
with mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.3) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()


        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #writeable stuff improves memory
        image.flags.writeable = False

        # make detections
        results = holistic.process(image)

        # recolor image back to BGR for rendering
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)



        # ... (rest of your code)

        try:
            leftBicepAngle, leftShoulderAngle, rightBicepAngle, rightShoulderAngle = get_angles(image, holistic, relevant_landmarks_numerical)
            #print(leftBicepAngle, leftShoulderAngle)
            #print(leftShoulderAngle > 30 and leftBicepAngle > 150)
            if not left_state==LEFT_PUNCH_DETECTED:
                if right_state == WAITING_FOR_RIGHT_PUNCH:
                    # Detect punch initiation
                    if rightShoulderAngle > 20 and rightBicepAngle > 90:
                        right_state = RIGHT_PUNCH_DETECTED
                elif right_state == RIGHT_PUNCH_DETECTED:
                    # Check for punch completion
                    if rightShoulderAngle < 25 or rightBicepAngle < 25:
                        counter += 1
                        print('Right punch detected - counter:', counter)
                        right_state = WAITING_FOR_RIGHT_PUNCH

            if not right_state==RIGHT_PUNCH_DETECTED:
                if left_state == WAITING_FOR_LEFT_PUNCH:
                    # Detect punch initiation
                    if leftShoulderAngle > 20 and leftBicepAngle > 90:
                        left_state = LEFT_PUNCH_DETECTED
                elif left_state == LEFT_PUNCH_DETECTED:
                    # Check for punch completion
                    if leftShoulderAngle < 25 or leftBicepAngle < 25:
                        counter += 1
                        print('Left punch detected - counter:', counter)
                        left_state = WAITING_FOR_LEFT_PUNCH

        except:
            pass



        # hand stuff
        
        # right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(130, 0, 75), thickness=2, circle_radius=2), # purple
                                  mp_drawing.DrawingSpec(color=(226, 43, 138), thickness=2, circle_radius=2)) # dark purple
        # left hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(139, 0, 0), thickness=2, circle_radius=2), # blue
                                  mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)) # dark blue

        # pose stuff
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 100, 0), thickness=2, circle_radius=2), # green
                                  mp_drawing.DrawingSpec(color=(0, 128, 0), thickness=2, circle_radius=2)) # dark green



        # render / display results
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
