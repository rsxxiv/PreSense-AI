import cv2 as cv
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pyfacerec-default-rtdb.firebaseio.com/',
    'storageBucket': 'pyfacerec.appspot.com'
})

# Importing the Students images into a list
folderPath = "Images"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []

studentId = []
for path in pathList:
    imgList.append(cv.imread(os.path.join(folderPath, path)))
    # Creating a list of student Ids by extracting them from image name
    studentId.append(os.path.splitext(path)[0])
    # print(path)
    # print(os.path.splitext(path)[0])

    # Adding Images to DataBase
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print("Uploaded Images to Firebase: ",studentId)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        # OpenCV uses BGR whereas face_recognition uses RBG
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#
# print("Encoding Started")
# encodeListKnown = findEncodings(imgList)
# print(encodeListKnown)
# encodeListKnownWithId = [encodeListKnown, studentId]
# print("Encoding Completed")

# file = open("EncodeFile.p", 'wb')
# pickle.dump(encodeListKnownWithId, file)
# file.close()
# print("File Saved")
