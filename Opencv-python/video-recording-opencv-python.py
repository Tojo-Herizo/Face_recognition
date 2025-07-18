import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2

class FaceRecognitionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Interface de Reconnaissance Faciale Avancée")
        self.window.geometry("1000x700")
        self.window.configure(bg="#2c3e50")

        self.video_running = False

        # OpenCV
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Title
        self.title_label = ttk.Label(self.window, text="Reconnaissance Faciale", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=10)

        # Canvas
        self.canvas = tk.Canvas(self.window, width=800, height=600, bg="#34495e")
        self.canvas.pack(pady=20)

        # Controls
        self.controls_frame = ttk.Frame(self.window)
        self.controls_frame.pack(pady=10)

        self.start_button = ttk.Button(self.controls_frame, text="Démarrer Caméra", command=self.start_video)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(self.controls_frame, text="Arrêter Caméra", command=self.stop_video)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.capture_button = ttk.Button(self.controls_frame, text="Capturer", command=self.capture_image)
        self.capture_button.grid(row=0, column=2, padx=10)

        self.quit_button = ttk.Button(self.controls_frame, text="Quitter", command=self.quit_app)
        self.quit_button.grid(row=0, column=3, padx=10)

    def start_video(self):
        if not self.video_running:
            self.video_running = True
            self.update_video()

    def stop_video(self):
        self.video_running = False

    def quit_app(self):
        self.stop_video()
        self.cap.release()
        self.window.destroy()

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("capture.jpg", frame)
            messagebox.showinfo("Capture", "Image enregistrée sous 'capture.jpg'.")

    def update_video(self):
        if self.video_running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Convert for Tkinter
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk  # prevent garbage collection

            self.window.after(15, self.update_video)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

