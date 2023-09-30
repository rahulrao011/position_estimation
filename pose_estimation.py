import mediapipe as mp
import cv2
import numpy as np
import time 


'''
### STATUS: WORKS SUCCESSFULLY AS A BICEP CURL TRACKER (GRANTED THE BICEP CURLS AREN'T TOO FAST)
### USES ANGLES TO DETERMINE IF A BICEP CURL HAS BEEN COMPLETED AND IT TRACKS HOW MANY BICEP CURLS HAVE BEEN COMPLETED

### Youtube project tutorial: https://www.youtube.com/watch?v=06TE_U21FK4
'''


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
    mp_holistic.PoseLandmark.LEFT_SHOULDER.value,
    mp_holistic.PoseLandmark.LEFT_ELBOW.value,
    mp_holistic.PoseLandmark.LEFT_WRIST.value
]
print(relevant_landmarks_numerical)


# bicep curl counter
counter = 0

# either 'up' or 'down'
stage = None



# get opencv camera
cap = cv2.VideoCapture(0)

# get camera dimensions
width = int(cap.get(3))
height = int(cap.get(4))

print(f'Width: {width}')
print(f'Height: {height}')



# initiating holistic model
# context manager: it's configuring the Holistic object with certain minimum detection and tracking confidence levels.
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
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
            a = [landmarks[relevant_landmarks_numerical[0]].x, landmarks[relevant_landmarks_numerical[0]].y]
            b = [landmarks[relevant_landmarks_numerical[1]].x, landmarks[relevant_landmarks_numerical[1]].y]
            c = [landmarks[relevant_landmarks_numerical[2]].x, landmarks[relevant_landmarks_numerical[2]].y]

            # calculate angle between relevant points
            angle = calculate_angle(a, b, c)
            #print(angle)
            #time.sleep(0.5)
            # visualize angle

            # not working
            # cv2.putText(image, str(angle), tuple(np.multiply(elbow, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AAA)


            # tracks if a bicep curl has been completed and how many bicep curls have been completed

            if angle < 25:
                stage = 'down'
                #in this context, down means retracted 
            if angle > 150 and stage == 'down':
                stage = 'up'
                counter+=1
                print('i just punched a ho ',counter)
            # if angle > 130:
            #     stage = 'down'
            # if angle < 30 and stage == 'down':
            #     stage = 'up'
            #     counter += 1
            #     print(counter)

        except:
            pass


        # draws a blue rectangle in the top left of the screen
        #cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)


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