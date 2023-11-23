import tkinter as tk
import tkinter.font as font
class RoundedButton(tk.Canvas):
    t=''
    def __init__(self, parent, border_radius, padding, color, text='', command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0,
                           relief="raised", highlightthickness=0, bg='#ffffff'  )
        self.command = command
        self.clipboard_append(text)
        self.t = text
        font_size = 12
        self.font = font.Font(size=font_size, family='Helvetica')
        self.id = None
        height = font_size + (1 * padding)
        width = self.font.measure(text)+(1*padding)
        width = width if width >= 80 else 80
        if border_radius > 0.5*width:
            print("Error: border_radius is greater than width.")
            return None
        if border_radius > 0.5*height:
            print("Error: border_radius is greater than height.")
            return None
        rad = 2*border_radius
        def shape():
            self.create_arc((0, rad, rad, 0),start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-rad, 0, width, rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width, height-rad, width-rad,height), start=270, extent=90, fill=color, outline=color)
            self.create_arc((0, height-rad, rad, height), start=180, extent=90, fill=color, outline=color)
            return self.create_polygon((0, height-border_radius, 0, border_radius, border_radius, 0, width-border_radius, 0, width,border_radius, width, height-border_radius, width-border_radius, height, border_radius, height),fill=color, outline=color)
        id = shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.create_text(width/2 - 2, height/2 - 2, text=text, fill='#ffffff', font=self.font)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        
    def _on_press(self, event):
        self.itemconfig("all", fill='#d2d6d3')
        # self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text=self.t, fill='#ffffff', font=self.font)

    def _on_release(self, event):
        self.itemconfig("all", fill="#172f5f")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text=self.t, fill='#ffffff', font=self.font)
        if self.command is not None:
            self.command()

    def disable(self):
        # self.unbind("<1>")
        # This method will disable the button by unbinding the events and changing the color to gray
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")
        self.itemconfig("all", fill="#a9a9a9")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text=self.t,
                         fill='#ffffff', font=self.font)

    def first_disable(self):
        # self.unbind("<1>")
        # This method will disable the button by unbinding the events and changing the color to gray
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")
        self.itemconfig("all", fill="#a9a9a9")
        self.create_text(self.winfo_width() + 42, self.winfo_height() + 12, text=self.t,
                         fill='#ffffff', font=self.font)
    
    def enable(self):
        # self.config(state="normal")
        # This method will enable the button by binding the events and changing the color to the original one
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.itemconfig("all", fill="#172f5f")
        # self.create_text(self.winfo_width()+42, self.winfo_height()+12, text=self.t, fill='#ffffff', font=self.font)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text=self.t, fill='#ffffff', font=self.font)


'''
def func():
    print("Button pressed")
          
def des():
    btn1.disable()
def en():
    btn1.enable()
               
         
root = tk.Tk()
root.wm_minsize(500, 250)
root.wm_maxsize(500, 250)          
btn1 = RoundedButton(root, text="fetch 1", border_radius=10, padding=20, command=func, color="#172f5f")          
btn1.place(x=50,y=30)
btn2 = RoundedButton(root, text="fetch 2", border_radius=10, padding=20, command=des, color="#172f5f")    
btn2.place(x=50,y=90)
btn3 = RoundedButton(root, text="fetch 3", border_radius=10, padding=20, command=en, color="#172f5f")    
btn3.place(x=50,y=150)

root.mainloop()
'''



