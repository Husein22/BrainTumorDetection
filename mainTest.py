
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2
from PIL import Image
from keras.models import load_model
import numpy as np
model=load_model('TumorMozga10EpochsCategotical.h5')

slika=cv2.imread("C:\\Users\\Administrator\\Desktop\\engBrainTumor\\datasets\\no\\no1.jpg")

img=Image.fromarray(slika)

img=img.resize((64,64))

img=np.array(img)

input_img = np.expand_dims(img, axis=0)
result = np.argmax(model.predict(input_img), axis=-1)

print("Result is",result)


