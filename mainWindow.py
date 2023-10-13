# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 01:13:55 2023

@author: Saif
"""
import tkinter as tk
from datetime import datetime
from PIL import ImageTk, Image
import cv2
import threading
import winsound
import imutils


root= tk.Tk()
root.title ("Motion Detection System")
root.wm_iconbitmap('resources/logo.ico')
# CREATE WINDOW - RESIZE FALSE - SIZE - TITLE CARD
root.resizable(False, False)
root.geometry('1000x600')
# for full screen 
# root.attributes('-fullscreen', True)
root.configure(bg='#c7d5e0')

def about():
    new_window = tk.Toplevel(root)
    new_window.geometry('600x600')
    new_window.title("About Us")
    new_window.resizable(False, False)
    
    about_label= tk.Label(new_window,text="About Us", height=1, bg="#03A9F4",  fg="#ffffff")
    about_label.pack()

    #creating tuple 
    Font_tuples = ("Comic Sans MS", 20 ,"bold")
    about_label.configure(font= Font_tuples)
    
    frame= tk.Frame(new_window, width=500, height=400)
    frame.pack()
    frame.place(anchor='center',relx=0.5, rely=0.5)
    
    label_mem = tk.Label(frame, text="GROUP MEMBERS:\n1. [group_member1]\n2.  [group_member2] \n3.  [group_member3] \n\nCLASS:\n[your_class]\n\nCOLLEGE:\n[your_ college_name]\n\nNAME OF GUIDE:\n[your_guide_name]", font="Times 15" )
    label_mem.pack(padx=10,pady=10)
      
    label_ver = tk.Label(frame, text="Version 1.0", font="Times 12" )
    label_ver.pack(padx=10,pady=10)

    frame.pack()
    frame.place(anchor='center',relx=0.5, rely=0.5)
    
# console function to write in console
def writeInConsole():
    end_labelcns = tk.Label(console_box, text=">>Motion Detected\n"+">>Motion Detection Stopped.",  font='Montserrat 12', bg="#000", fg= "#2de327")
    end_labelcns.pack()
    end_labelcns.place(x = 505, y = 170)        

    file_label = tk.Label(console_box, text=">>Please check MotionDetector_Logs.txt file",  font='Montserrat 12', bg="#000", fg= "#2de327")
    file_label.pack()
    file_label.place(x = 505, y = 210)    
    
# for motion detect class
def motionDetect():
    start_labelcns = tk.Label(console_box, text=">>starting motion detection...",  font='Montserrat 12', bg="#000", fg= "#2de327")
    start_labelcns.pack()
    start_labelcns.place(x = 505, y = 150)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    _,start_frame = cap.read()
    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    alarm = False
    alarm_mode = False
    alarm_counter  = 0

    def beep_alarm():
        global alarm
        for _ in range(5):
            if not alarm_mode:
                break
        
        # save text in file
        txt = "Motion Detected - ALARM"
        with open("MotionDetector_Logs.txt", "a+") as f1:
            f1.write(txt + " - "+ datetime.now().strftime('%A, %d %B %Y')+"\n")
        
        print(txt)
        winsound.Beep(2500,1000)
        alarm = False        
        
     

    while True:
        _, frame = cap.read()
        frame = imutils.resize(frame, width=500)

        if alarm_mode:
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)

            difference = cv2.absdiff(frame_bw, start_frame)
            threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
            start_frame = frame_bw

            if threshold.sum() > 300:
                alarm_counter += 1
            else:
                if alarm_counter > 0:
                    alarm_counter -= 1

            cv2.imshow("Motion Detector Cam start/end= t, exit= q", threshold)
        else:
            cv2.imshow("Motion Detector Cam start/end= t, exit= q", frame)

        if alarm_counter > 20:
            if not alarm:
                alarm = True
                threading.Thread(target=beep_alarm).start()
            
            if alarm:
                threading.Thread(target=beep_alarm).start()

        else:
            alarm = False

        key_pressed = cv2.waitKey(30)
        if key_pressed == ord("t"):
            alarm_mode = not alarm_mode
            alarm_counter = 0
        if key_pressed == ord("q"):
            alarm_mode = False
            writeInConsole()
            break

    cap.release()
    cv2.destroyAllWindows()

# DRAW TOP BLUE BAR - DRAW TITLE - DRAW DATETIME
top_bg = tk.Canvas(root, width=1000, height=60, bg='#1b2838', highlightthickness=0).place(x=0, y=0)
tk.Label(top_bg, text='Dashboard', font='Montserrat 25', bg='#1b2838', fg='white').place(x=15, y=3)
tk.Label(top_bg, text=datetime.now().strftime('%A, %d %B %Y'), font='Montserrat 20', bg='#1b2838', fg='white').place(
    x=600, y=8)


toolbar_box = tk.Canvas(root, width=960, height=450, bg='#2a475e', highlightthickness=0).place(x=20, y=100)
toolbar_box_top = tk.Canvas(root, width=960, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=80)
tk.Label(toolbar_box_top, text='Welcome in Motion Detection System', font='Montserrat 7 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=25, y=80)

 
# Creating a photoimage object to use image
img_mask = tk.PhotoImage(file = "resources/bg.png")

# set image on button
tk.Button(root, text = 'Motion Detect',  image = img_mask,command= motionDetect, cursor="hand2").place(x=80, y=120)
tk.Label(root, text="Motion Detection System", bg= "#FFFFFF", fg= "#f0f").place(x = 210, y = 120)

# box for console
console_box = tk.Canvas(root, width=450, height=305, bg='#000', highlightthickness=0).place(x=500, y=120)
tk.Label(console_box, text=">>Motion Detection System's Console",  font='Montserrat 13', bg="#000", fg= "#2de327").place(x = 505, y = 130)


btn_about = tk.Button (root, text="About US", command= about,height=3,width=20,  bg="#006C62", fg='#fff', cursor="hand2").place(x=210, y=450)

btn_exit = tk.Button (root, text="Exit",command=root.destroy, height=3, width=20,  bg="red", fg='#fff', cursor="hand2").place(x=640, y=450)

root.mainloop() 