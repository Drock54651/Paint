
import customtkinter as ctk
from settings import *

class ToolPanel(ctk.CTkToplevel):
    def __init__(self, parent, brush_float, color_string):
        super().__init__()

        self.geometry('200x300')
        self.title('')
        self.resizable(False, False)
        # self.iconbitmap('empty.ico') #! doesnt work might be bug
        self.attributes('-topmost', True) #! makes this window always on top of main window
        self.protocol('WM_DELETE-WINDOW', self.close_app)
        self.parent = parent


        #* LAYOUT
        self.rowconfigure(0, weight = 2, uniform = 'a')
        self.rowconfigure(1, weight = 3, uniform = 'a')
        self.rowconfigure((2,3), weight = 1, uniform = 'a')
        self.columnconfigure((0,1,2), weight = 1, uniform = 'a')

        #* WIDGETS
        BrushSizeSlider(self, brush_float) 
        ColorPanel(self, color_string)

    def close_app(self):
        self.parent.quit()



class BrushSizeSlider(ctk.CTkFrame):
    def __init__(self, parent, brush_float):
        super().__init__(parent)
        self.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'news')
        ctk.CTkSlider(self, variable = brush_float, from_ = .2, to = 1).pack(fill = 'x', expand = True, padx = 5)


class ColorPanel(ctk.CTkFrame):
    def __init__(self, parent, color_string):
        super().__init__(parent, fg_color = 'transparent')
        self.grid(row = 1, column = 0, columnspan = 3, pady = 5, padx = 5)
        self.color_string = color_string

        #* LAYOUT
        self.rowconfigure( [row for row in range(COLOR_ROWS)], weight = 1, uniform = 'a')
        self.columnconfigure([col for col in range (COLOR_COLS)], weight = 1, uniform = 'a' )


        #* CREATING COLOR BUTTONS
        for row in range(COLOR_ROWS):
            for col in range(COLOR_COLS):
                # ctk.CTkButton(self, text = '', fg_color = f'#{COLORS[row][col]}').grid(row = row, column = col)
                color = COLORS[row][col]
                ColorFieldButton(self, row, col, color, self.pick_color)

    def pick_color(self, color):
        self.color_string.set(color)

#TODO create and place buttons with the respective colors
class ColorFieldButton(ctk.CTkButton):
    def __init__(self, parent, row, col, color, pick_color):
        super().__init__(parent, 
                         text = '', 
                         fg_color = f'#{color}', 
                         corner_radius = 1,
                         command = self.click_handler)
        
        self.grid(row = row, column = col, padx = .4, pady = .4)

        self.pick_color = pick_color
        self.color = color

    def click_handler(self): #! will call the pick_color function with the color as arg
       self.pick_color(self.color)
        # self.color_string.set(self.color)
        # print(self.color)