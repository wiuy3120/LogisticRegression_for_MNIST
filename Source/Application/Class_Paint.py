from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageDraw
import numpy as np
import pickle
from Class_ProcessImage import ProcessImage
import cv2 as cv
# import cv2 as cv
# import os
    
class Paint():
    #DEFAULT_PEN_SIZE = 1000.0
    DEFAULT_COLOR = 'black'
    DEFAULT_SIZE = (600,600)
    def __init__(self):
        #
        self.root = Tk()
        # Vẽ song song với canvas
        self.image=Image.new("RGB", self.DEFAULT_SIZE,(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        #
        self.root.title("My Pen")
        self.pen_button = Button(self.root, height=1, width = 10, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.color_button = Button(self.root, height=1, width = 10, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, height=1, width = 10, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        self.reset_button = Button(self.root, height=1, width = 10, text='Reset', command=self.use_reset)
        self.reset_button.grid(row=0, column=3)

        # self.choose_img_button = Button(self.root, height=1, width = 10, text='Choose Image', command=self.use_choose_img)
        # self.choose_img_button.grid(row=0, column=4)

        # self.undo_button = Button(self.root, height=1, width = 10, text='Undo', command=self.use_undo)
        # self.undo_button.grid(row=0, column=4)

        self.predict_button = Button(self.root, height=1, width = 20, text='Predict', command=self.use_predict)
        self.predict_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=self.DEFAULT_SIZE[0], height=self.DEFAULT_SIZE[1])
        self.c.grid(row=1, columnspan=6)

        # self.list_c = []
        # self.list_img = []

        self.setup()
        self.activate_button(self.pen_button)
        self.root.mainloop()

    def setup(self):
        self.root_x = 0
        self.root_y = 0 
        self.check = False
        self.old_x = None
        self.old_y = None
        self.line_width = 5
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    # def use_undo(self):
    #     self.activate_button(self.undo_button)
    #     if len(self.list_img) >0:
    #         print("Undo")
    #         #Undo
    #         self.image = self.list_img[-1]
    #         self.list_img.pop()
    #         #
    #         self.c = self.list_c[-1]
    #         self.list_c.pop()
    #     self.c.update()            
    #     self.activate_button(self.pen_button)
    # def use_choose_img(self):
    #     #self.check = True
    #     self.activate_button(self.choose_img_button, eraser_mode=True)
    #     file_path = filedialog.askopenfilename()
    #     self.image = Image.open(file_path)
    #     # self.image = self.image.resize((self.DEFAULT_SIZE[0], self.DEFAULT_SIZE[1]), Image.ANTIALIAS)
    #     self.draw=ImageDraw.Draw(self.image)
    #     render = ImageTk.PhotoImage(self.image)
    #     self.c.image = render
    #     self.c.create_image(0, 0, anchor=NW, image=render)
    #     self.c.update()
    #     self.activate_button(self.pen_button)
    
    def use_reset(self):
        self.activate_button(self.reset_button)
        self.c.delete("all")
        self.image=Image.new("RGB", self.DEFAULT_SIZE ,(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        self.setup()
        self.activate_button(self.pen_button)
        self.reset_button.config(relief=RAISED)

    def use_predict(self):
        self.activate_button(self.predict_button)
        self.predict_button.config(relief=RAISED)
        ######
        self.np_image = np.array(self.image)
        img_process = ProcessImage(self.np_image, mode=1)
        img_process.find_digits()
        pipeline = pickle.load(open('pipeline_LR.sav', 'rb'))
        for i in range(len(img_process.list_info)):
            info_img = img_process.list_info[i]
            x0 = info_img[0]
            y0 = info_img[1]
            x1 = info_img[2] + x0 + 1
            y1 = info_img[3] + y0 + 1
            self.c.create_rectangle(x0, y0, x1, y1, fill="", outline='green', width = 2)
            text = pipeline.predict(np.array([img_process.list_digits[i]]))[0]
            if y0 - 15 > 5:
                self.c.create_text((x0+x1)/2-5, y0 - 15, anchor=W, font=("Purisa",20),text=text)
            else:
                self.c.create_text((x0+x1)/2-5, y1 + 15, anchor=W, font=("Purisa",20),text=text)
        self.activate_button(self.pen_button)
        #print(pipeline.predict(img_process.list_digits))

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = 5
        if self.eraser_on:
            paint_color = 'white'
            self.line_width=10  
        else:
            paint_color = self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND)
            self.draw.line(((self.old_x,self.old_y),(event.x,event.y)),
                             fill=paint_color,width=self.line_width)
        self.old_x = event.x
        self.old_y = event.y
        #print(self.old_x, self.old_y)

    def reset(self, event):
        self.old_x, self.old_y = None, None
        # self.list_c.append(self.c)
        # self.list_img.append(self.image)
        # print(2)