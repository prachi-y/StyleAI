from tkinter import *
from PIL import Image, ImageTk
import copy
from tkinter import filedialog as fd
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np

def second():
    start.place_forget()
    win.place(relx=0.5, rely=0.5, anchor="center")

def img_display(window, img_path, x, y):
    org = Image.open(img_path)
    disp = copy.deepcopy(org)
    disp.thumbnail((250, 250))
    org.thumbnail((1000, 1000))
    test2 = ImageTk.PhotoImage(disp, master=window)
    img = Label(window, image=test2)
    img.image = test2
    img.place(relx=x, rely=y, anchor="center")
    return img, org

def content_select():    
    filetype = (("JPEG", "*.jpg;*.jpeg;*.jpe;*.jfif"),
                ("GIF", "*.gif"),
                ("TIFF", "*.tif;*.tiff"),
                ("PNG", "*.png"),
                ("ICO", "*.ico"),
                ("All Files", "*.*"))
    content_path = fd.askopenfilename(title="Select an Image", filetypes = filetype)
    if content_path:
        global img1, org1
        select1['text'] = "Change Content Image"
        img1.place_forget()
        img1, org1 = img_display(win, content_path, 0.32, 0.28)

def style_select():  
    filetype = (("JPEG", "*.jpg;*.jpeg;*.jpe;*.jfif"),
                ("GIF", "*.gif"),
                ("TIFF", "*.tif;*.tiff"),
                ("PNG", "*.png"),
                ("ICO", "*.ico"),
                ("All Files", "*.*"))
    style_path = fd.askopenfilename(title="Select an Image", filetypes = filetype)
    if style_path:
        global img2, org2
        select2['text'] = "Change Style Image"
        img2.place_forget()
        img2, org2 = img_display(win, style_path, 0.57, 0.28)
    
def preprocess(org_img):
    t_img = tf.convert_to_tensor(org_img)
    t_img = tf.image.convert_image_dtype(org_img, tf.float32)
    t_img = t_img[tf.newaxis, :]
    
    return t_img

def stylise():
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    
    global img3, org1, org2, org3, t_stylised_img
    
    t_content = preprocess(org1)
    t_style = preprocess(org2)
    
    t_stylised_img = model(tf.constant(t_content), tf.constant(t_style))[0]
    
    img3.place_forget()
    org3 = tf.keras.preprocessing.image.array_to_img(np.squeeze(t_stylised_img))
    disp3 = copy.deepcopy(org3)
    disp3.thumbnail((250, 250))
    test3 = ImageTk.PhotoImage(disp3, master=win)
    img3 = Label(win, image=test3)
    img3.image = test3
    img3.place(relx=0.45, rely=0.73, anchor="center")

def save_img():
    global org3
    filetype = (("JPEG", "*.jpg;*.jpeg;*.jpe;*.jfif"),
                ("GIF", "*.gif"),
                ("TIFF", "*.tif;*.tiff"),
                ("PNG", "*.png"),
                ("ICO", "*.ico"),
                ("All Files", "*.*"))
    filename = fd.asksaveasfilename(title="Save Stylised Image", filetypes = filetype)
    if filename:
        org3.save(filename)

def go_back():
    global img1, img2, img3
    img1.place_forget()
    img2.place_forget()
    img3.place_forget()
    img1, org1 = img_display(win, "add.jpg", 0.32, 0.28)
    img2, org2 = img_display(win, "add.jpg", 0.57, 0.28)
    img3, org3 = img_display(win, "empty.png", 0.45, 0.73)
    win.place_forget()
    start.place(relx=0.5, rely=0.5, anchor="center")

root = Tk()
root.title("StyleAI")
w_s = root.winfo_screenwidth()
h_s = root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (w_s, h_s))
root.configure(bg="black")
root.resizable(False, False)
root.iconbitmap("icon.ico")
root.state("zoomed")

#start window
start = Frame(root, width=w_s, height=h_s, bg="light blue")

bg_img1 = Image.open("back.jpeg")
bg_img1 = bg_img1.resize((w_s, h_s))
test1 = ImageTk.PhotoImage(bg_img1, master=start)
background1 = Label(start, image=test1)
background1.image = test1
background1.place(relx=0, rely=0)

name_comp = Frame(start, width=40, height=20, bg="black")
name_comp.place(relx=0.5, rely=0.5, anchor="center")

name1 = Label(name_comp, text = "Welcome to", font = ("Lucida Handwriting", 15), width=40, anchor="w")
name1.pack()

name2 = Label(name_comp, text = "StyleAI", font = ("Elephant", 60), width=40)
name2.pack()

name3 = Label(name_comp, text = "Using Neural Style Transfer", font = ("Lucida Handwriting", 15), width=40, anchor="e")
name3.pack()

create1 = Button(start, text = "Create Your Own Stylised Image", padx=10, pady=10, font=("Comic Sans MS", 13), borderwidth=4, command=second)
create1.place(relx=0.5, rely=0.7, anchor="center")

#second window
win = Frame(root, width=w_s, height=h_s, bg="light yellow")

bg_img2 = Image.open("back2.jpg")
bg_img2 = bg_img2.resize((w_s, h_s))
test2 = ImageTk.PhotoImage(bg_img2, master=win)
background2 = Label(win, image=test2)
background2.image = test2
background2.place(relx=0, rely=0)

img1, org1 = img_display(win, "add.jpg", 0.32, 0.28)
img2, org2 = img_display(win, "add.jpg", 0.57, 0.28)

select1 = Button(win, text = "Choose Content Image", padx=10, pady=5, font=("Arial", 12), command=content_select)
select1.place(relx=0.32, rely=0.48, anchor="center")

select2 = Button(win, text = "Choose Style Image", padx=10, pady=5, font=("Arial", 12), command=style_select)
select2.place(relx=0.57, rely=0.48, anchor="center")

img3, org3 = img_display(win, "empty.png", 0.45, 0.73)

create2 = Button(win, text = "Create", padx=10, pady=5, font=("Arial", 12), command=stylise)
create2.place(relx=0.78, rely=0.30, anchor="center")

save = Button(win, text = "Save", padx=10, pady=5, font=("Arial", 12), command=save_img)
save.place(relx=0.78, rely=0.69, anchor="center")

back = Button(win, text = "Back", padx=10, pady=5, font=("Arial", 12), command=go_back)
back.place(relx=0.78, rely=0.77, anchor="center")

start.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()


