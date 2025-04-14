from tkinter import Tk, Frame, Label, PhotoImage, Label
from PIL import Image, ImageTk
from config import *

class App():
  def __init__(self):
    self.window = Tk()
    self.window.title("JuFO-KI GUI")
    self.window.attributes('-fullscreen', True)
    self.window.grid_rowconfigure(1, weight=1)
    self.window.grid_columnconfigure(0, weight=1)
    
    self.top_bar = Frame(self.window, bg=BAR_COLOR, height=50)
    self.top_bar.grid(row=0, column=0, sticky="ew", columnspan=3)
    
    self.image_frame = Frame(self.window, bg=IMAGE_FRAME_COLOR)
    self.image_frame.grid(row=1, column=0, sticky="nsew")
    self.image_label = Label(self.image_frame)
    
    self.info_frame = Frame(self.window, bg=INFO_FRAME_COLOR, width=100)
    self.info_frame.grid(row=1, column=2, sticky="nsew")
    self.info_label = Label(self.info_frame)
    
    self.bottom_bar = Frame(self.window, bg=BAR_COLOR, height=50)
    self.bottom_bar.grid(row=2, column=0, sticky="ew", columnspan=3)
  
  
  def show_image(self, image_path: str) -> None:
    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)
    self.image_label.config(image=img)
    self.image_label.image = img
    self.image_label.config(image=img)
    self.image_label.grid(row=1, column=0, sticky="nsw")
    self.window.update()
  
  def show_info(self, text) -> None:
    self.info_label.config(text=text)
  
  def run(self) -> None:
    self.window.mainloop()

if __name__ == "__main__":
  app: App = App()
  app.run()