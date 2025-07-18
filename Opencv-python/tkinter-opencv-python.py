import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class VideoCaptureApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Capture Vidéo OpenCV + Tkinter")
        self.window.geometry("900x700")
        self.window.configure(bg="#2c3e50")

        self.video_running = False

        # OpenCV
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Erreur : Impossible d'ouvrir la caméra")
            exit()

        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.fps = 20

        # VideoWriter pour sauvegarder
        self.out = cv2.VideoWriter('output.avi',
                                   cv2.VideoWriter_fourcc(*'MJPG'),
                                   self.fps,
                                   (self.frame_width, self.frame_height))

        # Titre
        self.title_label = ttk.Label(self.window, text="Interface Capture Vidéo",
                                     font=("Helvetica", 24, "bold"), foreground="white", background="#2c3e50")
        self.title_label.pack(pady=10)

        # Canvas pour affichage vidéo
        self.canvas = tk.Canvas(self.window, width=self.frame_width, height=self.frame_height, bg="#34495e")
        self.canvas.pack(pady=20)

        # Boutons
        self.controls_frame = ttk.Frame(self.window)
        self.controls_frame.pack(pady=10)

        self.start_button = ttk.Button(self.controls_frame, text="Démarrer Capture", command=self.start_video)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(self.controls_frame, text="Arrêter Capture", command=self.stop_video)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.quit_button = ttk.Button(self.controls_frame, text="Quitter", command=self.quit_app)
        self.quit_button.grid(row=0, column=2, padx=10)

    def start_video(self):
        if not self.video_running:
            self.video_running = True
            self.update_video()

    def stop_video(self):
        self.video_running = False

    def quit_app(self):
        self.stop_video()
        self.cap.release()
        self.out.release()
        self.window.destroy()

    def update_video(self):
        if self.video_running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)

                # Enregistrer la frame
                self.out.write(frame)

                # Convertir pour Tkinter
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk  # Référence pour éviter le garbage collector

            self.window.after(15, self.update_video)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureApp(root)
    root.mainloop()
