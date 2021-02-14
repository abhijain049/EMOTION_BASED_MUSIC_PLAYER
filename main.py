# Importing Required Modules & libraries
from tkinter import *
import pygame
import os
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import time
import os,random
import subprocess
from pygame import mixer
from tkinter import *
from urllib.request import  urlopen

# Defining MusicPlayer Class
face_classifier = cv2.CascadeClassifier(
            r'C:\Users\Abhishek\Downloads\archive\haarcascade_frontalface_default.xml')
classifier = load_model('EmotionDetectionModel.h5')
class MusicPlayer:

  # Defining Constructor
  def __init__(self,root):
    self.root = root
    # Title of the window
    self.root.title("Emotion Based Music Player")
    # Window Geometry
    self.root.geometry("1000x200+200+200")
    # Initiating Pygame
    pygame.init()
    # Initiating Pygame Mixer
    pygame.mixer.init()
    # Declaring track Variable
    self.track = StringVar()
    # Declaring Status Variable
    self.status = StringVar()

    # Creating Track Frame for Song label & status label
    trackframe = LabelFrame(self.root,text="Song Track",font=("times new roman",15,"bold"),bg="pink",fg="white",bd=5,relief=GROOVE)
    trackframe.place(x=0,y=0,width=600,height=100)
    # Inserting Song Track Label
    songtrack = Label(trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=0,column=0,padx=10,pady=5)
    # Inserting Status Label
    trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=0,column=1,padx=10,pady=5)

    # Creating Button Frame
    buttonframe = LabelFrame(self.root,text="Control Panel",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
    buttonframe.place(x=0,y=100,width=600,height=100)
    # Inserting Play Button
    playbtn = Button(buttonframe,text="PLAY",command=self.playsong,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=0,padx=10,pady=5)
    # Inserting Pause Button
    playbtn = Button(buttonframe,text="PAUSE",command=self.pausesong,width=8,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=1,padx=10,pady=5)
    # Inserting Unpause Button
    playbtn = Button(buttonframe,text="UNPAUSE",command=self.unpausesong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=2,padx=10,pady=5)
    # Inserting Stop Button
    playbtn = Button(buttonframe,text="STOP",command=self.stopsong,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=3,padx=10,pady=5)
    playbtn=Button(buttonframe,text="START",command=self.capture_emo,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=4,padx=10,pady=5)
    # Creating Playlist Frame
    songsframe = LabelFrame(self.root,text="Song Playlist",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
    songsframe.place(x=600,y=0,width=400,height=200)
    # Inserting scrollbar
    scrol_y = Scrollbar(songsframe,orient=VERTICAL)
    # Inserting Playlist listbox
    self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
    # Applying Scrollbar to listbox
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=self.playlist.yview)
    self.playlist.pack(fill=BOTH)
    # Changing Directory for fetching Songs


  def capture_emo(self):

        class_labels = ['Angry', 'Happy', 'Neutral', 'Sad']
        t0 = time.time()
        t0 = int(t0)
        cap ="http://192.168.43.1:8080/shot.jpg"
        now = time.time()
        fut = now + 60

        while True:
            frame=urlopen(cap)
            t1 = time.time()
            t1 = int(t1)
            img_arr = np.array(bytearray(frame.read()), dtype=np.uint8)

            c = cv2.imdecode(img_arr, -1)
            frame = cv2.flip(c, 1, 0)
            labels = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    preds = classifier.predict(roi)[0]
                    label = class_labels[preds.argmax()]
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    text = label
                else:
                    cv2.putText(frame, 'No Face Found', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            sec = t1 - t0
            cv2.imshow('Emotion Detector', frame)
            if cv2.waitKey(30) & sec > 10:
                break
        cap.release()
        cv2.destroyAllWindows()
        self.status.set(text)
        self.select_song(text)
  def select_song(self,text):
     self.emo=text
     if self.emo=="Happy":
        file=r"C:/Users/Abhishek/Music/Happy"
     if self.emo=="Sad":
        file = r"C:/Users/Abhishek/Music/Sad"
     if self.emo=="Neutral":
        file = r"C:/Users/Abhishek/Music/Neutral"
     if self.emo=="Angry" :
        file = r"C:/Users/Abhishek/Music/Angry"
     os.chdir(file)
    # Fetching Songs
     self.playlist.delete(0,END)

     songtracks = os.listdir()
    # Inserting Songs into Playlist
     for track in songtracks:
      self.playlist.insert(END, track)

  # Defining Play Song Function
  def playsong(self):
    # Displaying Selected Song title
    self.track.set(self.playlist.get(ACTIVE))
    # Displaying Status
  #  self.status.set("-Playing")
    # Loading Selected Song
    pygame.mixer.music.load(self.playlist.get(ACTIVE))
    # Playing Selected Song
    pygame.mixer.music.play()

  def stopsong(self):
    # Displaying Status
   # self.status.set("-Stopped")
    # Stopped Song
    pygame.mixer.music.stop()

  def pausesong(self):
    # Displaying Status
    self.status.set("-Paused")
    # Paused Song
    pygame.mixer.music.pause()

  def unpausesong(self):
    # Displaying Status
   # self.status.set("-Playing")
    # Playing back Song
    pygame.mixer.music.unpause()

# Creating TK Container
root = Tk()
# Passing Root to MusicPlayer Class
MusicPlayer(root)
# Root Window Looping
root.mainloop()
