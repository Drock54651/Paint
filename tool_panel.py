
import customtkinter as ctk
from settings import *
from PIL import Image
from tkinter import Canvas
#! All the erase bool stuff makes it so clicking anything color related automatically switches to brush mode


class ToolPanel(ctk.CTkToplevel):
    def __init__(self, parent, brush_float, color_string, erase_bool, clear_canvas):
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
        ColorPanel(self, color_string, erase_bool)
        ColorSliderPanel(self, color_string, erase_bool)
        DrawBrushButton(self, erase_bool)
        EraserButton(self, erase_bool)
        ClearAllButton(self, clear_canvas, erase_bool)
        BrushPreview(self, color_string, brush_float, erase_bool)

    def close_app(self):
        self.parent.quit()

class BrushPreview(Canvas):
    def __init__(self,parent, color_string, brush_float, erase_bool):
        super().__init__(parent, bg = BRUSH_PREVIEW_BG, bd = 0, relief= 'ridge', highlightthickness = 0)
        self.grid(row = 0, column = 1, columnspan = 2, sticky = 'news')

        #* DATA
        self.color_string = color_string    
        self.brush_float = brush_float
        self.erase_bool = erase_bool

        #* CANVAS SETUP
        self.x = 0
        self.y = 0
        self.max_length = 0 #! makes sure radius of the brush preview isnt too big, uses height as its smaller than width

        #* TRACE
        self.brush_float.trace('w', self.update)
        self.color_string.trace('w', self.update)
        self.erase_bool.trace('w', self.update)

        self.bind('<Configure>', self.setup)

    def setup(self, event):
        self.x = event.width / 2
        self.y = event.height / 2
        self.max_length = (event.height / 2) * 0.8
        self.update()

    def update(self, *args):
        current_radius = self.max_length * self.brush_float.get()

        self.delete('all') #! clears previous drawn ovals 
        

        #TODO: update color
        #TODO: if the eraser is active the color should be the same as the BRUSH_PREVIEW_BG and there should be a black circle
        color = f'#{self.color_string.get()}' if not self.erase_bool.get() else BRUSH_PREVIEW_BG
        outline_color = f'#{self.color_string.get()}' if not self.erase_bool.get() else 'black'

        
        self.create_oval(self.x - current_radius, 
                         self.y - current_radius, 
                         self.x + current_radius, 
                         self.y + current_radius, 
                         fill = color,
                         outline = outline_color,
                         dash = 20)
        
class BrushSizeSlider(ctk.CTkFrame):
    def __init__(self, parent, brush_float):
        super().__init__(parent)
        self.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'news')
        ctk.CTkSlider(self, variable = brush_float, from_ = .2, to = 1).pack(fill = 'x', expand = True, padx = 5)


class ColorPanel(ctk.CTkFrame):
    def __init__(self, parent, color_string, erase_bool):
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
                hover_color = HOVER_COLORS[row][col]
                ColorFieldButton(self, row, col, hover_color, color, self.pick_color, erase_bool)

    def pick_color(self, color):
        self.color_string.set(color)

#TODO create and place buttons with the respective colors
class ColorFieldButton(ctk.CTkButton):
    def __init__(self, parent, row, col, hover_color, color, pick_color, erase_bool):
        super().__init__(parent, 
                         text = '', 
                         fg_color = f'#{color}',
                         hover_color = f'#{hover_color}', 
                         corner_radius = 1,
                         command = self.click_handler)
        
        self.grid(row = row, column = col, padx = .4, pady = .4)
        self.erase_bool = erase_bool
        self.pick_color = pick_color
        self.color = color

    def click_handler(self): #! will call the pick_color function with the color as arg
       self.pick_color(self.color)
       self.erase_bool.set(False) #! clicking on color will automatically switch to brush mode
        # self.color_string.set(self.color)
        # print(self.color)


class ColorSliderPanel(ctk.CTkFrame):
    def __init__(self, parent, color_string, erase_bool):
        super().__init__(parent)
        self.grid(row = 0, column = 0, sticky = 'news', padx = 5, pady = 5)

        #* DATA
        self.color_string = color_string
        self.color_string.trace('w', self.set_color)
        self.erase_bool = erase_bool

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

        self.erase_bool.set(False)

    def set_color(self, *args):
        #TODO: make it so when clicking on color, it also updates the slider values
        self.r_int.set(COLOR_RANGE.index(self.color_string.get()[0])) #! Gets the index from the list
        self.g_int.set(COLOR_RANGE.index(self.color_string.get()[1])) 
        self.b_int.set(COLOR_RANGE.index(self.color_string.get()[2])) 


class Button(ctk.CTkButton):
    def __init__(self, parent, image_path, col, func):
        image = ctk.CTkImage(light_image = Image.open(image_path), dark_image = Image.open(image_path) )

        super().__init__(parent, command = func, text = '', image = image, fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER_COLOR)
        self.grid(row = 3, column = col, sticky = 'news', padx = 5, pady = 5)



#TODO: Create the 3 buttons
class DrawBrushButton(Button):
    def __init__(self, parent, erase_bool):
        super().__init__(parent, image_path = 'images/brush.png', col = 0, func = self.activate_brush)
        self.erase_bool = erase_bool
        self.erase_bool.trace('w', self.update_state)

    def update_state(self, *args): #! changes how the button looks if active
        if not self.erase_bool.get():
            self.configure(fg_color = BUTTON_ACTIVE_COLOR)

        else: 
            self.configure(fg_color = BUTTON_COLOR)

    def activate_brush(self):
        self.erase_bool.set(False)

class EraserButton(Button):
    def __init__(self, parent, erase_bool):
        super().__init__(parent, image_path = 'images/eraser.png', col = 1, func  = self.activate_erase)
        self.erase_bool = erase_bool
        self.erase_bool.trace('w', self.update_state)
    
    def update_state(self, *args): #! changes how button looks is active
        if self.erase_bool.get():
            self.configure(fg_color = BUTTON_ACTIVE_COLOR)

        else: 
            self.configure(fg_color = BUTTON_COLOR)

    def activate_erase(self):
        self.erase_bool.set(True)

class ClearAllButton(Button):
    def __init__(self,parent, clear_canvas, erase_bool):
        super().__init__(parent, image_path = 'images/clear.png', col = 2, func = self.clear_all)
        self.erase_bool = erase_bool
        self.clear_canvas = clear_canvas

    def clear_all(self):
        self.clear_canvas()
        self.erase_bool.set(False)