import tkinter as tk
from tkinter import font
import datetime

WIDTH, HEIGHT = 360, 720  
RADIUS = 36  

class PhoneMockup(tk.Toplevel):  
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Customer's Phone")

        self.resizable(True, True)
        self.geometry(f"{WIDTH*3}x{HEIGHT*2}")  
        self.minsize(WIDTH+100, HEIGHT+100)
        self.bind("<Escape>", lambda e: self.destroy())

        self.background_frame = tk.Frame(self, bg="#FFA500")
        self.background_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.background_frame, width=WIDTH, height=HEIGHT,
                                highlightthickness=0, bg="#FFA500")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")  

        self.phone_x = 0
        self.phone_y = 0

        self.large_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.small_font = font.Font(family="Helvetica", size=12)
        self.bottom_font = font.Font(family="Helvetica", size=16, weight="bold")

        self.draw_phone_body()
        self.create_status_elements()

        self.message_text_id = self.canvas.create_text(WIDTH/2, HEIGHT/2,
                                                       text="",
                                                       font=self.small_font,
                                                       fill="#FFFFFF",
                                                       width=WIDTH-40,
                                                       justify="center")

        self.update_loop()

    def _create_rounded_rectangle(self, x1, y1, x2, y2, r=25, **kwargs):
        if r > (x2-x1)/2:
            r = (x2-x1)/2
        if r > (y2-y1)/2:
            r = (y2-y1)/2

        self.canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style='pieslice', **kwargs)
        self.canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style='pieslice', **kwargs)
        self.canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style='pieslice', **kwargs)
        self.canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style='pieslice', **kwargs)

        rect1 = self.canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
        rect2 = self.canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)
        return rect1

    def draw_phone_body(self):
        x1 = self.phone_x
        y1 = self.phone_y
        x2 = x1 + WIDTH
        y2 = y1 + HEIGHT


        self._create_rounded_rectangle(x1-6, y1-6, x2+6, y2+6, r=RADIUS+4, fill="#050203", outline="")
        
        self.body_id = self._create_rounded_rectangle(x1, y1, x2, y2, r=RADIUS, fill="#050203", outline="#000")

        inset = 18
        self.screen_id = self._create_rounded_rectangle(x1+inset, y1+inset, x2-inset, y2-inset,
                                                        r=RADIUS-8, fill="#050203")

        
        notch_w = 100
        notch_h = 8
        nx1 = x1 + (WIDTH - notch_w)//2
        ny1 = y1 + 22
        self._create_rounded_rectangle(nx1, ny1, nx1+notch_w, ny1+notch_h, r=6, fill="#050203", outline="")

    def create_status_elements(self):
        self.time_text = self.canvas.create_text(WIDTH/2, 160,
                                                 text="--:--", font=self.large_font, fill="#F70D1A")
        self.date_text = self.canvas.create_text(WIDTH/2, 200,
                                                 text="Loading date...", font=self.small_font, fill="#FFFFFF")

    def update_time_display(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%A, %b %d %Y")
        self.canvas.itemconfigure(self.time_text, text=time_str)
        self.canvas.itemconfigure(self.date_text, text=date_str)

    def update_loop(self):
        self.update_time_display()
        self.after(1000, self.update_loop)

    def update_message(self, message):
        self.canvas.itemconfigure(self.message_text_id, text=message)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = PhoneMockup(master=root)
    app.mainloop()
