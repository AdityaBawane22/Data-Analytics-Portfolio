import tkinter as tk
from PIL import Image, ImageTk
import os


class VisualsViewerWindow(tk.Toplevel):
    """Opens as a new window *within the same app*, and returns to Dashboard on close"""
    def __init__(self, controller, folder_path, cluster_id):
        super().__init__()
        self.controller = controller
        self.folder_path = folder_path
        self.cluster_id = cluster_id

        self.title(f"Cluster {cluster_id} Visuals")

        # Fullscreen based on device resolution
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.configure(bg="#FF5F1F")

        self.image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        self.current_index = 0
        self.photo_image = None

        top_frame = tk.Frame(self, bg="#FF5F1F")
        top_frame.pack(pady=10)

        tk.Button(top_frame, text="< BACK", bg="#D4D4D4", font=('Arial', 10, 'bold'),
                  command=self.go_back).pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(top_frame, text="", bg="#FF5F1F", fg="white", font=('Arial', 12, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.image_label = tk.Label(self, bg="#EAEAEA")
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        nav_frame = tk.Frame(self, bg="#FF5F1F")
        nav_frame.pack(pady=10)

        tk.Button(nav_frame, text="< Previous", command=self.prev_image, bg="#008000", fg="white",
                  font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Button(nav_frame, text="Next >", command=self.next_image, bg="#008000", fg="white",
                  font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)

        self.load_image(0)

    def load_image(self, index):
        if not self.image_files:
            self.status_label.config(text="No visuals available.")
            return

        image_path = os.path.join(self.folder_path, self.image_files[index])
        img = Image.open(image_path)

        # Resize image dynamically to fit window while keeping aspect ratio
        max_width = self.winfo_screenwidth() - 100
        max_height = self.winfo_screenheight() - 200
        img.thumbnail((max_width, max_height))

        self.photo_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo_image)
        self.status_label.config(text=f"Image {index + 1} of {len(self.image_files)}")

    def next_image(self):
        if not self.image_files:
            return
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.load_image(self.current_index)

    def prev_image(self):
        if not self.image_files:
            return
        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.load_image(self.current_index)

    def go_back(self):
        self.destroy()  # Close the visuals window
        self.controller.show_frame("ClusterDetailPage", self.cluster_id)  # Return to the dashboard page
