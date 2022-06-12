import cv2
import pickle
import cvzone
import numpy as np
import urllib.request
import pyrebase
import pandas as pd

firebaseConfig = {
    'apiKey': "AIzaSyDnRpPw3zjIm1oUenUtqTEwJnf0tFuUTuc",
    'authDomain': "crudapp-86bdf.firebaseapp.com",
    'databaseURL': "https://crudapp-86bdf-default-rtdb.firebaseio.com",
    'projectId': "crudapp-86bdf",
    'storageBucket': "crudapp-86bdf.appspot.com",
    'messagingSenderId': "612441472514",
    'appId': "1:612441472514:web:f9df2a589bbef64b6e311b",
    'measurementId': "G-GX2SGJG7PS"
}

# firebaseConfig = {
#   'apiKey': "AIzaSyBavD0kFNReplwh1onprP4optM798gXgWQ",
#   'authDomain': "parkingspaces-63113.firebaseapp.com",
#   'databaseURL': "https://parkingspaces-63113-default-rtdb.firebaseio.com/",
#   'projectId': "parkingspaces-63113",
#   'storageBucket': "parkingspaces-63113.appspot.com",
#   'messagingSenderId': "798550527382",
#   'appId': "1:798550527382:web:33363e7133ebff7f0fa1b7"
# }

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
# auth = firebase.auth()
# storage = firebase.storage()

# Video Feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

numberPos = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
             31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,
             58,59,60,61,62,63,64,65,66,67,68,69]

def checkParkingSpace(imgPro):

    spaceCounter = 0

    for pos in posList:
        x,y = pos

        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x+y),imgCrop)
        # cv2.imshow("imgCropped",imgCrop)

        count = cv2.countNonZero(imgCrop)
        if count < 900:
            color = (0,255,0)
            thickness = 5
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

        cvzone.putTextRect(img,str(count),(x,y+height-5), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}',(100,50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
    # db.child("ParkingSpaces").update({'freespaces': spaceCounter})

# def numberingParkingBox():
#     # print("Nilai ada pada NumberPos : ", numberPos)
#     # count2 += 1
#     for pos in posList:
#         while True:


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3),np.int8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)

    checkParkingSpace(imgDilate)
    # numberingParkingBox()

    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


