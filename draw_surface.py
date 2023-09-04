from tkinter import Canvas
from settings import *

class DrawSurface(Canvas):
    def __init__(self, parent, color_string, brush_float, erase_bool):
        super().__init__(parent, bg = CANVS_BG, bd = 0, highlightthickness = 0, relief = 'ridge')
        self.pack(expand = True, fill = 'both')


        #* DATA
        self.color_string = color_string
        self.brush_float = brush_float
        self.allow_draw = False
        self.erase_bool = erase_bool

        #* INPUT
        self.bind('<Motion>', self.draw) #! Captures mouse movement
        self.bind('<Button>', self.activate_draw)
        self.bind('<ButtonRelease>', self.deactivate_draw)

        #* Start Pos
        self.old_x = None
        self.old_y = None
    
    #* METHODS

    def draw(self, event):
        if self.old_x and self.old_y:

            if self.allow_draw:
                
                self.create_brush_line((self.old_x, self.old_y), (event.x, event.y )) 
            

        self.old_x = event.x
        self.old_y = event.y

    def create_brush_line(self, start, end):
        brush_size = self.brush_float.get() * 10 ** 2
        color = f'#{self.color_string.get()}' if not self.erase_bool.get() else '#FFF' #! if erase bool is false, get color, else make color white
        self.create_line(start, end,  fill = color, width = brush_size, capstyle = 'round') #! capstyle prevents weird visual artifacts

    def activate_draw(self, event):
        self.allow_draw = True
        self.create_brush_line((event.x, event.y), (event.x + 1, event.y + 1))

    def deactivate_draw(self, event):
        self.allow_draw = False

        
        self.old_x = None
        self.old_y = None