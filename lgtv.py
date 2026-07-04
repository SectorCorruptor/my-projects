import tkinter as tk
from PIL import Image, ImageTk
import subprocess

p = subprocess.Popen(
    ["/bin/bash"],
    stdin=subprocess.PIPE,
    text=True,
    bufsize=1
)

p.stdin.write("source lgtv-venv/bin/activate\n")
p.stdin.flush()

m=tk.Tk()
m.title("LG TV Remote")
m.geometry("300x420")
m.resizable(False, False)
img_open = Image.open("lgtv.webp").resize((300, 420))
tk_img = ImageTk.PhotoImage(img_open)

f=tk.Canvas(m, width=300, height=420)
f.place(x=0,y=0)

f.create_image(0, 0, image=tk_img, anchor=tk.NW)

clicked = lambda px, py, l, u, r, d:l<=px<=r and u<=py<=d

def regclick(event):
    if clicked(event.x,event.y, 127, 199, 151, 221):
        print("up")
        p.stdin.write("lgtv --name X sendButton up\n")
        p.stdin.flush()
    elif clicked(event.x,event.y, 104, 225, 119, 250):
        print("left")
        p.stdin.write("lgtv --name X sendButton left\n")
        p.stdin.flush()
    elif clicked(event.x,event.y, 156, 228, 175, 249):
        print("right")
        p.stdin.write("lgtv --name X sendButton right\n")
        p.stdin.flush()
    elif clicked(event.x,event.y, 123, 258, 151, 277):
        print("down")
        p.stdin.write("lgtv --name X sendButton down\n")
        p.stdin.flush()
    elif clicked(event.x,event.y, 127, 224, 154, 253):
        print("enter")
        p.stdin.write("lgtv --name X sendButton enter\n")
        p.stdin.flush()
    elif clicked(event.x,event.y, 99, 191, 119, 202):
        print("home")
        p.stdin.write("lgtv --name X sendButton home\n")
        p.stdin.flush()
    print(event.x, event.y)

f.bind("<Button-1>", regclick)
#f.bind("<Motion>", lambda ev:print(ev.x, ev.y))
def on_close():
    p.terminate()   # ask process to stop

    # optional: wait briefly
    try:
        p.wait(timeout=1)
    except:
        p.kill()    # force kill if needed

    m.destroy()

m.protocol("WM_DELETE_WINDOW", on_close)
m.mainloop()
