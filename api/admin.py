# from django.contrib import admin

# Register your models here.



import cv2
from PIL import ImageGrab



while True:
    img = ImageGrab.grab(bbox=(100, 10, 400, 780))
    
    cv2.imshow("Video :", cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    cv2.waitKey(1)
