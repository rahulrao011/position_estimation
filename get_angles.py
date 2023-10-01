import numpy as np



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



def get_angles(image, holistic, relevant_landmarks_numerical): # gets angles
    
    results = holistic.process(image)
    
    landmarks = results.pose_landmarks.landmark
        #.landmark gives you hashmap stuff that has references to all of your xyz tuples 

        # get coords for relevant points

        #get the x and y of the given body point on the 2d camera plane

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


    # returns a tuple ( ... )
    return leftBicepAngle, leftShoulderAngle, rightBicepAngle, rightShoulderAngle