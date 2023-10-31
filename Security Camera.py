import cv2
import winsound
import tkinter as tk

def start_action():
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
            cv2.imshow("Abhi Personal Camera", frame)

root = tk.Tk()
root.title("Start and End Buttons")

start_button = tk.Button(root, text="Start", command=start_action())
start_button.pack(pady=20)

root.mainloop()
