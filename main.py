from tkinter import Canvas
from settings import * 
import customtkinter as ctk
from draw_surface import DrawSurface

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(('800x600'))
        self.title('')
        self.iconbitmap('empty.ico')
        ctk.set_appearance_mode('light')


        #* WIDGETS
        DrawSurface(self)


        #* RUN
        self.mainloop()

if __name__ == '__main__':
    App()