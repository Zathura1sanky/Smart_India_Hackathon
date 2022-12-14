import pyautogui
from keras.models import load_model
from collections import deque
import numpy as np
import cv2
import os
import json
import gesture2 as gs
from pynput.keyboard import Key,Controller

Keyboard = Controller()

# Load the models built in the previous steps
mlp_model = load_model('../alpha/emnist_mlp_model.h5')
cnn_model = load_model('../alpha/emnist_cnn_model.h5')

# Letters lookup
letters = { 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j',
11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't',
21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z', 27: '-'}
points = deque(maxlen=512)

camera = cv2.VideoCapture(0)
# Keep looping
def alpha():
    global camera
    global points
    # (grab, frame) = camera.read()
    temp = 1
    prediction1 = 26
    prediction2 = 26
    blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
    alphabet = np.zeros((200, 200, 3), dtype=np.uint8)

    gesture = gs.gesture()

    while True:
        temp += 1
        # camera = cv2.VideoCapture(0)
        # Grab the current paintWindow
        (grabbed, frame) = camera.read()

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        center = None

        flag1,frame = gesture.hands(frame)
        coordinates = gesture.lm(frame)
        # print(flag1)
        # print("gggggggggg")
        # print(coordinates)
        if flag1==1:
            center=(coordinates[8][1],coordinates[8][2])
            points.appendleft(center)

        elif len(coordinates) == 0 or flag1!=1:
            if len(points) != 0:
                blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
                blur1 = cv2.medianBlur(blackboard_gray, 15)
                blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
                thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                blackboard_cnts = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
                print(type(blackboard_cnts))
                if len(blackboard_cnts) >= 1:
                    print(len(blackboard_cnts))
                    cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]
                    print(cv2.contourArea(cnt))
                    if cv2.contourArea(cnt) > 100:

                        x, y, w, h = cv2.boundingRect(cnt)
                        alphabet = blackboard_gray[y-10:y + h + 10, x-10:x + w + 10]
                        newImage = cv2.resize(alphabet, (28, 28))
                        newImage = np.array(newImage)
                        newImage = newImage.astype('float32')/255
                        print("early")
                        prediction1 = mlp_model.predict(newImage.reshape(1,28,28))[0]
                        prediction1 = np.argmax(prediction1)
                        print("Pre1")
                        prediction2 = cnn_model.predict(newImage.reshape(1,28,28,1))[0]
                        prediction2 = np.argmax(prediction2)
                        print("Pre2")

                points = deque(maxlen=512)
                print("Poi len",points)
                blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
                print(blackboard)


        else:
            points = deque(maxlen=512)


        for i in range(1, len(points)):
                if points[i - 1] is None or points[i] is None:
                        continue
                # print(i)
                cv2.line(frame, points[i - 1], points[i], (0, 0, 0), 2)
                cv2.line(blackboard, points[i - 1], points[i], (255, 255, 255), 8)

        cv2.putText(frame, "Multilayer Perceptron : " + str(letters[int(prediction1)+1]), (10, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255, 255, 255), 2)
        cv2.putText(frame, "Convolution Neural Network:  " + str(letters[int(prediction2)+1]), (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)



        if str((letters[int(prediction2)+1])) != "-"  and flag1==0:
            print(str(letters[int(prediction1) + 1]))
            print(str(letters[int(prediction2) + 1]))
            print("exiting")
            camera.release()
            cv2.destroyAllWindows()
            return str(letters[int(prediction2)+1])


        cv2.imshow("alphabets Recognition Real Time", frame)

        # If the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

def main():
    global camera
    screenshot = 0
    control = 1
    # print("Do you want to add gesture for screenshot")
    # x= input()
    # if x == "yes":
    screenshot = alpha()
    # with open('./data/dygestures.json', 'r') as openfile:
    #     # Reading from json file
    #     json_object = json.load(openfile)
    #
    # print(json_object)
    # f = open('./data/dygestures.json')

    # returns JSON object as
    # a dictionary
    # data = json.load(f)
    # print(data)
    # Iterating through the json
    # list
    # for i in data['emp_details']:
    #     print(i)

    # Closing file
    # f.close()
    # json_object.update(diction)
    #
    # with open('sample.json', 'w') as json_file:
    #     json.dump(json_object, json_file)

    print("Type 1 to test the gesture                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       ```````````````````````````````````````````````````````````````` ")
    x = input()
    if x == "1":
        camera= cv2.VideoCapture(0)
        control = alpha()
        if control == screenshot:
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(r'.\xyz2.png')
            return 0

        while (1) :

            if control == screenshot:
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save(r'.\xyz2.png')
                return 0
            else:
                camera = cv2.VideoCapture(0)
                control = alpha()
    elif x=='2':

        camera = cv2.VideoCapture(0)
        control = alpha()
        if control == screenshot:
            # myScreenshot = pyautogui.screenshot()
            # myScreenshot.save(r'.\xyz2.png')
            Keyboard.press(Key.alt)
            Keyboard.release(Key.alt)
            Keyboard.press(Key.tab)
            return 0

        while (1):

            if control == screenshot:
                Keyboard.press(Key.alt)
                Keyboard.press(Key.tab)
                Keyboard.release(Key.tab)

                return 0
            else:
                camera = cv2.VideoCapture(0)
                control = alpha()


    # print("Start recording")
    # screen=alpha()
    # print("hhhh")
    # print(screen)
    # if x==tab:
    #

    #     camera = cv2.VideoCapture(0)
    #     (grab, frame) = camera.read()
    #     cv2.putText(frame, "TRY", (200, 370),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    #     command = alpha(frame)
    #     if command == pause:
    #         Keyboard.press(Key.space)
    #


if __name__ == '__main__':
    main()


    print("Input gestures")


