from tkinter import Canvas
from settings import * 
import customtkinter as ctk
from draw_surface import DrawSurface
from tool_panel import ToolPanel
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(('800x600'))
        self.title('')
        self.iconbitmap('empty.ico')
        ctk.set_appearance_mode('light')

        #* DATA
        self.color_string = ctk.StringVar(value = '000') #! RGB
        self.brush_float = ctk.DoubleVar(value = 1) #! Size of brush, can only be between 0.2 -> 1




        
        #* WIDGETS
        DrawSurface(self, self.color_string, self.brush_float)
        ToolPanel(self, self.brush_float, self.color_string)

        #* MOUSE WHEEL EVENT
        self.bind('<MouseWheel>', self.adjust_brush_size)


        #* RUN
        self.mainloop()


    def adjust_brush_size(self, event):
        #TODO: get a direction from mousewheel
        direction = int(event.delta / 120)
        # print(direction)
        new_brush_size = self.brush_float.get() + .05 * direction #! direction would be -1 or 1

        #TODO limit brush size between .2 and 1
        new_brush_size = max(.2, min(1, new_brush_size))
        
        # if new_brush_size < .2: #! this works too!
        #     new_brush_size = .2

        # if new_brush_size > 1:
        #     new_brush_size = 1

        self.brush_float.set(new_brush_size)





if __name__ == '__main__':
    App()