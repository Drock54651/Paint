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

        #* DATA
        self.color_string = ctk.StringVar(value = '000') #! RGB
        self.brush_float = ctk.DoubleVar(value = 0.2) #! Size of brush, can only be between 0.2 -> 1




        
        #* WIDGETS
        DrawSurface(self, self.color_string, self.brush_float)


        #* RUN
        self.mainloop()

if __name__ == '__main__':
    App()