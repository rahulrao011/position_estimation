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
WAITING_FOR_PUNCH = 0
PUNCH_DETECTED = 1

# Initialize state
state = WAITING_FOR_PUNCH

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
            if state == WAITING_FOR_PUNCH:
                # Detect punch initiation
                if leftShoulderAngle > 20 and leftBicepAngle > 90:
                    state = PUNCH_DETECTED
            elif state == PUNCH_DETECTED:
                # Check for punch completion
                if leftShoulderAngle < 25 or leftBicepAngle < 25:
                    counter += 1
                    print('Punch detected - counter:', counter)
                    state = WAITING_FOR_PUNCH

        except:
            pass



        '''
        
        # recolor feed to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #writeable stuff improves memory
        image.flags.writeable = False

        # make detections
        results = holistic.process(image)

        # recolor image back to BGR for rendering
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)



        try:
            leftBicepAngle, leftShoulderAngle, rightBicepAngle, rightShoulderAngle = get_angles(image, holistic, relevant_landmarks_numerical)


            # Biceps
            if leftBicepAngle < 25:
                leftBicepStage = False
            elif leftBicepAngle > 150 and not leftBicepStage:
                leftBicepStage = True

            #in this case, we set our bicep stage

             # Shoulders
            if leftShoulderAngle < 15:
                leftShoulderStage = False
            elif leftShoulderAngle > 30 and not leftShoulderStage:
                leftShoulderStage = True

            #setting shoulderstage
            punched = leftShoulderStage and leftBicepStage

            print(punched)
            if punched:
                print('counter += 1')
                while punched:
                    leftBicepAngle, leftShoulderAngle, rightBicepAngle, rightShoulderAngle = get_angles(image, holistic, relevant_landmarks_numerical)
                    # Biceps
                    if leftBicepAngle < 25:
                        leftBicepStage = False
                    elif leftBicepAngle > 150 and not leftBicepStage:
                        leftBicepStage = True

                    #in this case, we set our bicep stage

                    # Shoulders
                    if leftShoulderAngle < 15:
                        leftShoulderStage = False
                    elif leftShoulderAngle > 30 and not leftShoulderStage:
                        leftShoulderStage = True

                    #setting shoulderstage
                    punched = leftShoulderStage and leftBicepStage


        except:
            pass

            

        '''
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
