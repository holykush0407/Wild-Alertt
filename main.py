import tkinter as tk
from tkinter import ttk, messagebox
import threading
import numpy as np
import cv2
import imutils
import time
import os
from collections import Counter
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
from datetime import datetime

# Initialize Pygame for sound
pygame.mixer.init()
file_path = os.path.join(os.getcwd(), 'audio/siren.wav')
pygame.mixer.music.load(file_path)

# Model files
protext = r"models/MobileNetSSD_deploy.prototxt.txt"
model = r"models/MobileNetSSD_deploy.caffemodel"

# Classes
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
           "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
           "train", "tvmonitor"]
REQ_CLASSES = ["bird", "cat", "cow", "dog", "horse", "sheep"]

# Load model
net = cv2.dnn.readNetFromCaffe(protext, model)

conf_thresh = 0.2
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Send email alert
def send_email_alert():
    sender_email = "kushbajpai2003@gmail.com"
    receiver_email = "kushbajpai20003@gmail.com"                                                 
    password = "obpe abrh ocrn yczt"

    subject = "Animal Intrusion Alert"
    body = "An animal intrusion has been detected by the system. Please take necessary action.🚨🚨🆘🆘😮😮😮"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Log intrusion to CSV
def log_intrusion(animal_type, confidence_score):
    filename = "intrusion_log.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Time", "Animal", "Confidence"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), animal_type, f"{confidence_score:.2f}"])

# GUI class
class AnimalDetectorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Wild-Alert: An Animal Intrusion Detector")
        self.master.geometry("600x500")
        self.master.configure(bg='#f0f0f0')
        self.running = False
        self.thread = None
        
        # Create main frame
        self.main_frame = ttk.Frame(master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and description
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=(0, 10))
        
        title_label1 = ttk.Label(
            title_frame,
            text="Wild-Alert: ",
            font=('Helvetica', 16, 'bold')
        )
        title_label1.pack(side=tk.LEFT)
        
        title_label2 = ttk.Label(
            title_frame,
            text="An Animal Intrusion Detector",
            font=('Helvetica', 16, 'italic')
        )
        title_label2.pack(side=tk.LEFT)
        
        desc_label = ttk.Label(
            self.main_frame,
            text="Monitor your farm for unauthorized animal intrusions",
            font=('Helvetica', 10)
        )
        desc_label.pack(pady=(0, 20))
        
        # Status frame
        self.status_frame = ttk.LabelFrame(self.main_frame, text="System Status", padding="10")
        self.status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="System Status: Stopped",
            font=('Helvetica', 10)
        )
        self.status_label.pack()
        
        # Detection info frame
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Detection Information", padding="10")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        self.detection_label = ttk.Label(
            self.info_frame,
            text="No animals detected",
            font=('Helvetica', 10)
        )
        self.detection_label.pack()
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)
        
        # Style configuration
        style = ttk.Style()
        style.configure('Action.TButton', font=('Helvetica', 10))
        
        self.start_btn = ttk.Button(
            self.button_frame,
            text="Start Detection",
            command=self.start_detection,
            style='Action.TButton',
            width=20
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            self.button_frame,
            text="Stop Detection",
            command=self.stop_detection,
            style='Action.TButton',
            width=20
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.quit_btn = ttk.Button(
            self.button_frame,
            text="Quit Application",
            command=self.quit_app,
            style='Action.TButton',
            width=20
        )
        self.quit_btn.pack(side=tk.LEFT, padx=5)
        
        # Footer
        footer_label = ttk.Label(
            self.main_frame,
            text="© 2024 Farm Security System",
            font=('Helvetica', 8)
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def start_detection(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="System Status: Running")
            self.start_btn.state(['disabled'])
            self.stop_btn.state(['!disabled'])
            self.thread = threading.Thread(target=self.detect)
            self.thread.start()

    def stop_detection(self):
        self.running = False
        self.status_label.config(text="System Status: Stopped")
        self.start_btn.state(['!disabled'])
        self.stop_btn.state(['disabled'])
        self.detection_label.config(text="No animals detected")

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.running = False
            self.master.destroy()

    def detect(self):
        vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        time.sleep(2)
        count = []
        flag = 0
        c = 0

        while self.running:
            success, frame = vs.read()
            if not success:
                break

            frame = imutils.resize(frame, width=500)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            det = 0
            detected_animal = ""
            detected_conf = 0

            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > conf_thresh:
                    idx = int(detections[0, 0, i, 1])
                    if CLASSES[idx] in REQ_CLASSES:
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        label = f"{CLASSES[idx]}: {confidence*100:.2f}%"
                        cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                        det = 1
                        detected_animal = CLASSES[idx]
                        detected_conf = confidence * 100
                        
                        # Update detection label
                        self.detection_label.config(
                            text=f"Detected: {detected_animal} ({detected_conf:.1f}% confidence)"
                        )

            count.append(det)
            if flag == 1 and len(count) > c + (11 * 18):
                flag = 0
            if Counter(count[-36:])[1] > 15 and flag == 0:
                self.detection_label.config(
                    text=f"ALERT: {detected_animal} intrusion detected! ({detected_conf:.1f}% confidence)"
                )
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                flag = 1
                c = len(count)

                # Send email notification
                send_email_alert()

                # Log to CSV
                if detected_animal:
                    log_intrusion(detected_animal, detected_conf)

            cv2.imshow("Animal Detector", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        vs.release()
        cv2.destroyAllWindows()

# Run GUI
root = tk.Tk()
app = AnimalDetectorGUI(root)
root.mainloop()
