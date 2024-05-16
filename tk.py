import tkinter as tk

from PIL import ImageTk, Image

root = tk.Tk()

root.attributes("-topmost", True)
root.attributes("-alpha", 0.5)
root.overrideredirect(True)

label = tk.Label()
image = Image.open("img.png")
imagetk = ImageTk.PhotoImage(image)

label.configure(image=imagetk)
label.pack()
root.geometry(f"{image.width}x{image.height}+100+100")

try:
    root.mainloop()
except KeyboardInterrupt:
    root.quit()
