from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial
from pymongo import MongoClient

import numpy as np
import multiprocessing as mp
import time
import cv2
import pymongo
import os
import time
import pigpio
import pygame
import sys
import math
import serial
import pynmea2
import requests
import json

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

resX = 320
resY = 240

cx = resX / 2
cy = resY / 2

pygame.init()
lcd = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(False)

panX = 19.2
panY = 19.2

pi = pigpio.pi()
pi.set_mode(4, pigpio.OUTPUT)
pi.set_PWM_frequency(4, 50)
pi.set_PWM_dutycycle(4, panX)

pi.set_mode(17, pigpio.OUTPUT)
pi.set_PWM_frequency(17, 50)
pi.set_PWM_dutycycle(17, panY)

camera = PiCamera()
camera.resolution = (resX, resY)
camera.rotation=180
camera.framerate = 60

rawCapture = PiRGBArray(camera, size=(resX, resY))


def draw_frame(img):
    global panX
    global panY
    cv2.imwrite('tmp.jpg', img)
    img = pygame.image.load('tmp.jpg')
    lcd.blit(img, (0, 0))
    pygame.display.update()


### Main ######################################################################

if __name__ == '__main__':
    camera.capture(rawCapture, format="bgr")
    rawCapture.truncate(0)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        draw_frame(image)
        rawCapture.truncate(0)
        for event in pygame.event.get():
            if (event.type is pygame.MOUSEBUTTONDOWN):
                pi.stop()
                pygame.quit()
                pool.close()
                sys.exit()

