import cv2
import winsound
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from tkinter import ttk
from PIL import Image, ImageTk
import math
from openpyxl import Workbook
from datetime import datetime

# Global variable to track dark mode state
dark_mode = False

# Global variable for animation
angle = 0

# Global variable for Excel workbook and sheet
workbook = Workbook()
sheet = workbook.active


# Function to toggle dark mode
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    update_theme()


# Function to update the GUI theme based on dark mode state
def update_theme():
    bg_color = "#333" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"
    button_bg = "#4CAF50" if dark_mode else "green"

    root.configure(bg=bg_color)
    title_label.configure(bg=bg_color, fg=fg_color)
    image_label.configure(bg=bg_color)
    start_button.configure(bg=button_bg, fg=fg_color)
    team_label.configure(fg=fg_color, bg=bg_color)


# Function to update the animation
def update_animation():
    global angle
    if motion_detection_running:
        angle += 2  # Rotate by 2 degrees
        if angle >= 360:
            angle = 0
        rotated_logo = original_logo.rotate(angle)
        animated_logo = ImageTk.PhotoImage(rotated_logo)
        image_label.config(image=animated_logo)
        image_label.image = animated_logo
    root.after(50, update_animation)  # Call update_animation every 50ms


# Function to start motion detection
def start_motion_detection():
    global motion_detection_running
    if not motion_detection_running:
        messagebox.showinfo("Motion Detection", "Motion detection is starting.")
        motion_detection_running = True
        Thread(target=motion_detection).start()


# Your provided motion detection code
def motion_detection():
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        ret, frame = cam.read()
        ret, frame1 = cam.read()
        diff = cv2.absdiff(frame, frame1)
        grey = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(thresh, None, iterations=3)
        contour, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contour:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 138), 2)
            winsound.Beep(1000, 200)

        if cv2.waitKey(10) == ord('a'):
            break
        cv2.imshow("Motion Detection", frame)

        # Save motion detection data to Excel
        save_motion_data()

    cam.release()
    cv2.destroyAllWindows()
    motion_detection_running = False


# Function to save motion detection data to Excel
def save_motion_data():
    global sheet
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([timestamp, "Motion Detected"])
    workbook.save("motion_detection_data.xlsx")


# Create the tkinter window
root = tk.Tk()
root.title("Security Camera with Frame Detection Powered by AI")
root.configure(bg='white')  # Set default background color

# Load and display an image/logo
original_logo = Image.open("C://Users//Hp//PycharmProjects//python-security camera//sscam.jpg")  # Replace "logo.png" with your image file
original_logo = original_logo.resize((150, 150), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(original_logo)
image_label = tk.Label(root, image=photo)
image_label.image = photo
image_label.pack(pady=20)

# Create a label for the project title
title_label = tk.Label(root, text="Security Camera with Frame Detection Powered by AI", font=("Arial", 16, "bold"),
                       fg="black", bg="white")
title_label.pack(pady=10)

# Create a Start button (centered)
start_button = tk.Button(root, text="Start", command=start_motion_detection, font=("Arial", 12, "bold"), bg="green",
                         fg="white", padx=20, pady=10)
start_button.pack(pady=20)

# Create a label for the team members
team_label = tk.Label(root, text="Team Members:\nAbhi Success, Pranav Mehta, Piyush Kumar, Harshit Soni, Fahim-ul-haq",
                      font=("Arial", 12), fg="black", bg="white")
team_label.pack(pady=10)

# Create a dark mode toggle button
dark_mode_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, font=("Arial", 10, "bold"),
                             bg="gray", fg="white", padx=10, pady=5)
dark_mode_button.pack()

# Initialize motion detection state
motion_detection_running = False

# Start the tkinter main loop
root.geometry("600x500")  # Set the window size
update_theme()  # Initialize theme based on dark mode state
update_animation()  # Start the animation
root.mainloop()

