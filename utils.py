# -*- coding: utf-8 -*-
"""utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yAREcbfqVC1At4Q0zhoB6I7D9oxyp9FM
"""

# Program To Read video
# and Extract Frames
import cv2  # noqa
#from cv2 import WaitKey,VideoCapture,imwrite
import os
import time #noqa
#image size of the cropped face
import numpy as np
#--------------------------------------
#image size of the cropped face
IMG_SHAPE = (160, 160)
#contains file location of the video file
VIDEO_FILE="/content/drive/My Drive/git/meet1.mp4"
#contains all the images obtained from frame
IMAGE_FOLDER="/content/drive/My Drive/git/images/"
MODEL_PATH="/content/drive/My Drive/git/model2.json"
WEIGHT_PATH="/content/drive/My Drive/git/model2v2.h5"
FACENET_MODEL_PATH="/content/model/facenet_keras.h5"
DATA_PATH="/content/drive/My Drive/git/db.csv"
FRAME_RATE=5
#--------------------------------------

from FaceRecognition.face_recognition import FaceVerification
fv=FaceVerification()
model=fv.get_model(MODEL_PATH,WEIGHT_PATH)
model.compile(loss="binary_crossentropy",optimizer='adam')

class FaceRecognitionUtils:
    """
    Import utils
    """

    def __init__(self):
        pass

    def video_to_frame(self,input_video,IMAGE_FOLDER):
      if not os.path.exists(IMAGE_FOLDER):
          os.mkdir(IMAGE_FOLDER)
      vidcap = cv2.VideoCapture(input_video)
      success,image = vidcap.read()
      count = 0
      frame_rate = FRAME_RATE
      prev = 0  
      while success:
        time_elapsed = time.time() - prev
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            cv2.imwrite(IMAGE_FOLDER+"/frame%d.jpg" % count, image)     # save frame as JPEG file
            success,image = vidcap.read()
            count += 1
    """
    def get_encoding(e1,e2):
        return np.subtract(e1,e2)
   
    def check_in_db(self,data,embedding,labels):
        for i,j in zip(data,labels):
            vector=get_encoding(i,embedding)
            result=model.predict(vector)
            if result<=0.5:
                return j
        return None
    """
    def check_in_db(self,data,embedding,labels):
      i_p=embedding
      import numpy as np
      dicti=data
      answer=[None]*i_p.shape[0]
      for i in range(0,dicti.shape[0]):
        m=i_p.shape[0]+i
        if(i_p.shape[0]+i>dicti.shape[0]):
          m=(i_p.shape[0]+i)%(dicti.shape[0])
          new=np.concatenate((dicti[i:dicti.shape[0]],dicti[0:m]),axis=0)
          current_labels=np.concatenate((labels[i:len(labels)],labels[0:m]),axis=0)
          vector=np.subtract(new,i_p)
        else:
          vector=np.subtract(dicti[i:m],i_p)
          current_labels=labels[i:m]
        result=model.predict(vector)
        for i in range(0,len(result)):
          if result[i][0]<=0.5:
            #i_p=np.delete(i_p,i,axis=0)
            answer[i]=current_labels[i]
      return answer

