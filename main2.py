import tkinter as tk
from tkinter import PhotoImage
from _datetime import datetime
import pickle
import cvzone
import numpy as np
import cv2 as cv
import os
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://pyfacerec-default-rtdb.firebaseio.com/',
    'storageBucket': 'pyfacerec.appspot.com'
})

bucket = storage.bucket()

# Capturing the Video
cap = cv.VideoCapture(0)

# Create Tkinter window
root = tk.Tk()
root.title("Face Attendance System")

# Load background image
background_image = cv.imread('Resources/background.png')
background_image = cv.cvtColor(background_image, cv.COLOR_BGR2RGB)
background_photo = PhotoImage(data=cv.imencode('.png', background_image)[1].tobytes())

# Create a Tkinter Canvas
canvas = tk.Canvas(root, width=background_image.shape[1], height=background_image.shape[0])
canvas.pack()

# Display the background image on the Canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

# Importing the modeList into a list
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the EncodeFile.p
print("Loading Encodefile.p ....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithId = pickle.load(file)
file.close()
encodeListKnown, studentId = encodeListKnownWithId
# print(studentId)
print("Encodefile.p Loaded Succesfully")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    EncodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurrFrame:

        for encodeFace, faceLoc in zip(EncodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print('Matches',matches)
            # print('Face Distance',faceDis)

            matchIndex = np.argmin(faceDis)
            # print('Match Index',matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentId[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0)
                id = studentId[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (272,400))
                    cv.imshow("Face Attendance", imgBackground)
                    cv.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                #Download the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # Download the image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv.imdecode(array, cv.COLOR_BGRA2BGR)

                # Update Data of attendance
                dateTimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   '%Y-%m-%d %H:%M:%S')

                secondsElapsed = (datetime.now()-dateTimeObject).total_seconds()

                # Setting TIme interval for the Attendance
                if secondsElapsed >= 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    # Placing Student Information on the UI
                    cv.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), cv.FONT_HERSHEY_COMPLEX,
                                   1, (255, 255, 255), 1)
                    cv.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv.FONT_HERSHEY_COMPLEX,
                               0.5, (100, 100, 100), 1)
                    cv.putText(imgBackground, str(id), (1006, 493), cv.FONT_HERSHEY_COMPLEX,
                               0.5, (100, 100, 100), 1)
                    cv.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv.FONT_HERSHEY_COMPLEX,
                               0.6, (100, 100, 100), 1)
                    cv.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv.FONT_HERSHEY_COMPLEX,
                               0.6, (100, 100, 100), 1)
                    cv.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), cv.FONT_HERSHEY_COMPLEX,
                               0.6, (100, 100, 100), 1)

                    (w, h), _ = cv.getTextSize(studentInfo['name'], cv.FONT_HERSHEY_COMPLEX, 1,1)
                    offset = (414 - w)//2
                    cv.putText(imgBackground, str(studentInfo['name']), ((808 + offset), 445), cv.FONT_HERSHEY_COMPLEX,
                               1, (0, 0, 0), 1)

                    imgBackground[175:175+216, 909:909+216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    # cv.imshow("Webcam", img)
    cv.imshow("Face Attendance", imgBackground)
    cv.waitKey(1)
