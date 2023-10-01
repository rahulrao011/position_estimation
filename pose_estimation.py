import mediapipe as mp
import cv2
import numpy as np
import time 


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

#this takes three points on the pose net, like elbow, shoulder, and wrist, and calculates the angle that there is there
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle



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



# initiating holistic model
# context manager: it's configuring the Holistic object with certain minimum detection and tracking confidence levels.
with mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.3) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        
        
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
            landmarks = results.pose_landmarks.landmark
            #.landmark gives you hashmap stuff that has references to all of your xyz tuples 

            # get coords for relevant points

            #get the x and y of the given body point on the 2d camera plane

            '''
             mp_holistic.PoseLandmark.LEFT_SHOULDER.value,
    mp_holistic.PoseLandmark.LEFT_ELBOW.value,
    mp_holistic.PoseLandmark.LEFT_WRIST.value,
    mp_holistic.PoseLandmark.LEFT_HIP.value,

    # right side
    mp_holistic.PoseLandmark.RIGHT_SHOULDER.value,
    mp_holistic.PoseLandmark.RIGHT_ELBOW.value,
    mp_holistic.PoseLandmark.RIGHT_WRIST.value,
    mp_holistic.PoseLandmark.RIGHT_HIP.value,
            '''

            # landmarks is similar to a list of hash-maps: with each coordinate in the list: {12:{'x': 3.141, 'y': 2.712, 'z': 12.31},... }

            # these are all coordinates (x, y)

            left_shoulder = [landmarks[relevant_landmarks_numerical[0]].x, landmarks[relevant_landmarks_numerical[0]].y]
            left_elbow = [landmarks[relevant_landmarks_numerical[1]].x, landmarks[relevant_landmarks_numerical[1]].y]
            left_wrist = [landmarks[relevant_landmarks_numerical[2]].x, landmarks[relevant_landmarks_numerical[2]].y]
            left_hip = [landmarks[relevant_landmarks_numerical[3]].x, landmarks[relevant_landmarks_numerical[3]].y]

            right_shoulder = [landmarks[relevant_landmarks_numerical[4]].x, landmarks[relevant_landmarks_numerical[4]].y]
            right_elbow = [landmarks[relevant_landmarks_numerical[5]].x, landmarks[relevant_landmarks_numerical[5]].y]
            right_wrist = [landmarks[relevant_landmarks_numerical[6]].x, landmarks[relevant_landmarks_numerical[6]].y]
            right_hip = [landmarks[relevant_landmarks_numerical[7]].x, landmarks[relevant_landmarks_numerical[7]].y]

            # calculate angle between relevant points
            leftBicepAngle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            rightBicepAngle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            leftShoulderAngle = calculate_angle(left_hip, left_shoulder, left_elbow)
            rightShoulderAngle = calculate_angle(right_hip, right_shoulder, right_elbow)
            #print(angle)
            #time.sleep(0.5)


            # tracks if a bicep curl has been completed and how many bicep curls have been completed


            # Biceps
            if leftBicepAngle < 25 or finishedLeftPunch:
                leftBicepStage = False
                finishedLeftPunch = False
            elif leftBicepAngle > 150 and not leftBicepStage and not finishedLeftPunch:
                leftBicepStage = True

            '''
            if rightBicepAngle < 25 or finishedRightPunch:
                rightBicepStage = False
                finishedRightPunch = False
            elif rightBicepAngle > 150 and not rightBicepStage and not finishedRightPunch:
                rightBicepStage = True



            list = [
            left_elbow_angle at time t = 0 is the 0th element,
            left_elbow_angle at time t = 1 is the 1th element.
            ]

            math = (list[1] - list[2]) / (time difference between frames) = rate of change of the elbow angle

            if math > some number:
            
            if it is + then the elbow angle is increasing

            if it is 0 then the elbow angle is not changing

            if it is - then im retracting my arm



            '''

            # Shoulders
            if leftShoulderAngle < 15 or finishedLeftPunch:
                leftShoulderStage = False
                finishedLeftPunch = False
            elif leftShoulderAngle > 30 and not leftShoulderStage:
                leftShoulderStage = True


            '''
            if rightShoulderAngle < 15 or finishedRightPunch:
                rightShoulderStage = False
                finishedRightPunch = False
            elif rightShoulderAngle > 30 and not rightShoulderStage:
                rightShoulderStage = True
            '''

            # random logs
            #print(f'Right Shoulder Sage: {rightShoulderAngle}, {rightShoulderStage}')
            #print(f'Right Bicep Stage: {rightBicepAngle}, {rightBicepStage}')
            #print(f'Finished Right Punch: {finishedRightPunch}')

            #print('Right Bicep Angle: ', {rightBicepAngle})

            #time.sleep(0.5)


            if leftBicepStage and leftShoulderStage and not finishedLeftPunch:
                leftBicepStage = None
                leftShoulderStage = None
                finishedLeftPunch = True
                counter += 1
                print('left punch: ', counter)


            '''
            if rightBicepStage and rightShoulderStage and not finishedRightPunch:
                rightBicepStage = None
                rightShoulderStage = None
                finishedRightPunch = True
                counter += 1
                print('right punch: ', counter)
            '''
            

        except:
            pass


        # render / draw landmarks

        # face stuff
        # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
        # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)

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
