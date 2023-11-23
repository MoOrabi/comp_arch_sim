import tkinter as tk
import tkinter.font as font

class CustomTextArea(tk.Frame):
    def __init__(self, parent, width, height, bg_color, fg_color, font_size):
        tk.Frame.__init__(self, parent, bg=bg_color)
        self.text = tk.Text(self, width=width, height=height, bg=bg_color, fg=fg_color, font=font.Font(size=font_size))
        self.text.pack(side="left", fill="both", expand=True)
        self.text.config(highlightthickness=0, bd=0)

   
    def insert(self, index, text):
        self.text.insert(index, text)

    def delete(self, start, end=None):
        self.text.delete(start, end)


'''
root = tk.Tk()
root.geometry("400x300")

text_area = CustomTextArea(root, width=25, height=10, bg_color="#f0f0f0", fg_color="#000000", font_size=12)
text_area.place(x=30,y=10)

def print_text():
    text = text_area.text.get("1.0", "3.0")
    print(text)

button = tk.Button(root, text="Print Text", command=print_text)
button.place(x=50,y=250)

root.mainloop()
'''