#simple tool for getting the pixels of the text in the levels for the PNG creation

from PIL import Image
import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk

img = Image.open("../png/soundoutActivityBulbasaurTextSizeTest.png")
root = tk.Tk()
root.title("Click to get coordinates")

# Create frame for scrollbars
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
frameHorizontal = tk.Frame(frame)
frameHorizontal.pack(side=tk.BOTTOM, fill=tk.X)

# Create canvas with scrollbars
canvas = Canvas(frame, width=1000, height=600)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbarBottom = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbarBottom.pack(side=tk.BOTTOM, fill=tk.X)
canvas.config(yscrollcommand=scrollbar.set)
canvas.config(xscrollcommand=scrollbarBottom.set)

photo = ImageTk.PhotoImage(img)
canvas.create_image(50, 0, image=photo, anchor="nw")
canvas.config(scrollregion=canvas.bbox("all"))

def on_click(event):
    print(f"Clicked at: ({event.x + canvas.canvasx(0)}, {event.y + canvas.canvasy(0)})")

canvas.bind("<Button-1>", on_click)
root.mainloop()