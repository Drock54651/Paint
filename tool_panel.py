
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
        ColorSliderPanel(self, color_string)

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
                         hover_color = f'#{color}', 
                         corner_radius = 1,
                         command = self.click_handler)
        
        self.grid(row = row, column = col, padx = .4, pady = .4)

        self.pick_color = pick_color
        self.color = color

    def click_handler(self): #! will call the pick_color function with the color as arg
       self.pick_color(self.color)
        # self.color_string.set(self.color)
        # print(self.color)


class ColorSliderPanel(ctk.CTkFrame):
    def __init__(self, parent, color_string):
        super().__init__(parent)
        self.grid(row = 0, column = 0, sticky = 'news', padx = 5, pady = 5)

        #* DATA
        self.color_string = color_string
        self.color_string.trace('w', self.set_color)

        #! Variables that would represent slider position
        self.r_int = ctk.IntVar(value = self.color_string.get()[0])
        self.g_int = ctk.IntVar(value = self.color_string.get()[1])
        self.b_int = ctk.IntVar(value = self.color_string.get()[2])

        #* LAYOUT
        self.rowconfigure((0,1,2), weight = 1, uniform = 'a')
        self.columnconfigure(0, weight = 1, uniform = 'a')


        #* SLIDER WIDGETS
        ctk.CTkSlider(self, from_ = 0, to = 15, number_of_steps = 16, command = lambda value: self.set_single_color('r', value), variable = self.r_int, button_color = SLIDER_RED, button_hover_color = SLIDER_RED).grid(row = 0, column = 0, padx = 2)
        ctk.CTkSlider(self, from_ = 0, to = 15, number_of_steps = 16, command = lambda value: self.set_single_color('g', value), variable = self.g_int, button_color = SLIDER_GREEN, button_hover_color = SLIDER_GREEN).grid(row = 1, column = 0, padx = 2)
        ctk.CTkSlider(self, from_ = 0, to = 15, number_of_steps = 16, command = lambda value: self.set_single_color('b', value), variable = self.b_int, button_color = SLIDER_BLUE, button_hover_color = SLIDER_BLUE).grid(row = 2, column = 0, padx = 2)


    def set_single_color(self, color, value): #! takes in slider value and gets the index from COLOR_RANGE to get new color

        current_color_list = list(self.color_string.get())

        match color:
            case 'r': current_color_list[0] = COLOR_RANGE[int(value)]

            case 'g': current_color_list[1] = COLOR_RANGE[int(value)]

            case 'b': current_color_list[2] = COLOR_RANGE[int(value)]

        self.color_string.set(f'{"".join(current_color_list)}')

    def set_color(self, *args):
        #TODO: make it so when clicking on color, it also updates the slider values
        self.r_int.set(COLOR_RANGE.index(self.color_string.get()[0])) #! Gets the index from the list
        self.g_int.set(COLOR_RANGE.index(self.color_string.get()[1])) 
        self.b_int.set(COLOR_RANGE.index(self.color_string.get()[2])) 