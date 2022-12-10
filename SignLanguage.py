import cv2
import mediapipe as mp
import numpy as np

# This function get tha distance betewwn two landmarks
def get_landmarks_distance(a,b):
    return ((a["x"] - b["x"])**2 + (a["y"] - b["y"])**2)**0.5

# Check if hand is opended or closed
def get_hand_status(points):
    # True rappresent hand opened
    if get_landmarks_distance(points[0], points[9]) > get_landmarks_distance(points[0], points[12]):
        return False
    
    return True

# Check if hand is vertical or horizontal
def get_landmarks_align(a,b):
    if (a["x"] - b["x"]) < 0.1 and a["x"] - b["x"] > -0.1:
        return "Vertical"
    
    return "Horizontal"

# This function get then hand direction to optmize letter check
def get_hand_direction(points):
    if get_landmarks_align(points[9],points[0]) == "Vertical":
        if points[0]["y"] > points[9]["y"]:
            return "Top"
        else:
            return "Down"
    else:
        if points[0]["x"] < points[9]["x"]:
            return "Right"
        else:
            return "Left"

# get_lettere function check tha hand direction and some landmarks distance to recognize the letter
def get_letter(points):
    if get_landmarks_align(points[9],points[0]) == "Horizontal" and get_hand_direction(points) == "Right":
        if get_landmarks_distance(points[0], points[8]) > get_landmarks_distance(points[0], points[7])\
        and get_landmarks_distance(points[0], points[12]) > get_landmarks_distance(points[0], points[11]) \
        and get_landmarks_distance(points[0], points[16]) < get_landmarks_distance(points[0], points[13]) \
        and get_landmarks_distance(points[0], points[20]) < get_landmarks_distance(points[0], points[17]):
            if get_landmarks_distance(points[3], points[4]) > get_landmarks_distance(points[9], points[4]) or get_landmarks_distance(points[3], points[4]) > get_landmarks_distance(points[16], points[4]) :
                return "H"

    elif get_landmarks_align(points[9],points[0]) == "Vertical" and get_hand_direction(points) == "Top":
        if get_landmarks_distance(points[8], points[6]) > get_landmarks_distance(points[8], points[4]) \
            and get_landmarks_distance(points[12], points[10]) > get_landmarks_distance(points[12], points[4]) \
            and get_landmarks_distance(points[16], points[14]) > get_landmarks_distance(points[16], points[4]) \
            and get_landmarks_distance(points[20], points[18]) > get_landmarks_distance(points[20], points[4]):
            return "O"

        elif get_landmarks_distance(points[0], points[6]) > get_landmarks_distance(points[0], points[8]) \
            and get_landmarks_distance(points[0], points[10]) > get_landmarks_distance(points[0], points[12]) \
            and get_landmarks_distance(points[0], points[14]) > get_landmarks_distance(points[0], points[16]) \
            and get_landmarks_distance(points[0], points[18]) > get_landmarks_distance(points[0], points[20]) \
            and get_landmarks_distance(points[0], points[9]) > get_landmarks_distance(points[0], points[4]):
            return "E"

        elif get_landmarks_distance(points[0], points[17]) > get_landmarks_distance(points[0], points[20]) \
            and get_landmarks_distance(points[0], points[13]) > get_landmarks_distance(points[0], points[16]) \
            and get_landmarks_distance(points[0], points[9]) > get_landmarks_distance(points[0], points[12]) \
            and get_landmarks_distance(points[0], points[8]) > get_landmarks_distance(points[0], points[6]) \
            and get_landmarks_distance(points[5], points[4]) > get_landmarks_distance(points[4], points[3]):
            return "L"

#This function create the list of charachters to form the word
def write_cool_text(letter):
    if None not in word and letter == None:
        word.append(letter)
    elif None in word and letter != None:
        word.remove(None)
        word.append(letter)
    elif letter not in word:
        word.append(letter)

    print(word)
    for i in range(0,len(word)):
        if word[i] != None:
            cv2.putText(image, word[i], (80+(i*50), 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), thickness=3)


print("Hi, this program can recognize the letters (H - E - L - O) with signal language \n")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

word = []

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5, 
    max_num_hands=1) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for id, landmark in enumerate(hand_landmarks.landmark):
                    landmarks.append({"id": id, "x": landmark.x, "y": landmark.y})

                write_cool_text(get_letter(landmarks))

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()