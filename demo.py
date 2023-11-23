import tkinter as tk
from tkinter import ttk
from RoundedButton import RoundedButton

class CustomTable(tk.Frame):
    def __init__(self, parent,  height, width1,width2):
        tk.Frame.__init__(self, parent)
        self.headers = []
        self.rows = 0

        self.game_frame = tk.Frame(self)
        self.game_frame.pack()

        self.my_game = ttk.Treeview(self.game_frame, height=int(height))

        # Change the columns to have only two
        self.my_game['columns'] = ('1', '2')

        self.my_game.column("#0", width=0,  stretch=tk.NO)
        self.my_game.column("1",anchor=tk.CENTER, width=width1)
        self.my_game.column("2",anchor=tk.CENTER,width=width2)
        
        

        self.my_game['show'] = 'tree' 

        # Add a scrollbar to the treeview
        self.scrollbar = ttk.Scrollbar(self.game_frame, orient="vertical", command=self.my_game.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.my_game.configure(yscrollcommand=self.scrollbar.set)

        self.my_game.pack()

    def insert_row(self, data):
        self.my_game.insert(parent='',index='end',iid=self.rows,text='',
                            values=(data[0], data[1]))
        self.rows += 1

    # Add a method to edit a specific item in the table
    def edit_item(self, row, column, value):
        # Use the set method of the treeview object to change the value of the item
        self.my_game.set(item=row, column=column, value=value)
    
    def delete_row(self, row):
        
        # Use the delete method of the treeview object to remove the item with the given index
        self.my_game.delete(row)
        
        for i in range(row, self.rows - 1):
            
            self.my_game.move(i+1, '', i)
        
        self.rows -= 1

    def delete_all(self):

        # Use the delete method of the treeview object to remove the item with the given index
        for i in range(self.rows):
            self.my_game.delete(i)
            self.rows -= 1

        # for i in range(row, self.rows - 1):
        #     self.my_game.move(i + 1, '', i)

    def get_item(self, row, column):
        # Use the item method of the treeview object to get the value of the item
        return self.my_game.item(row, 'values')[column]
    
    
    
        

'''
def func():
    table.edit_item(row=0 , column=0,value="gg")


root = tk.Tk()
root.geometry("500x500")
root.title('PythonGuides')
root['bg'] = '#ffffff'

table = CustomTable(root, height=11, width1=80,width2=80)
table.place(x=50,y=30)

btn1 = RoundedButton(root, text="fetch 1", border_radius=10, padding=20, command=func, color="#2bc8c8")          
btn1.place(x=50,y=300)
table.insert_row((0,0))
table.insert_row((1,1))
table.insert_row((2,2))
table.insert_row((3,3))
table.insert_row((4,4))
table.insert_row((5,5))
table.insert_row((6,6))
table.insert_row((7,7))
table.insert_row((8,8))
table.insert_row((9,9))
table.insert_row((0,0))
table.insert_row((1,1))
table.insert_row((2,2))
table.insert_row((3,3))
table.insert_row((4,4))
table.insert_row((5,5))
table.insert_row((6,6))
table.insert_row((7,7))
table.insert_row((8,8))
table.insert_row((9,9))
# Example of using the edit_item method to change the name of the third row to 'Samurai'
#table.edit_item(row='2', column='player_name', value='Samurai')

root.mainloop()
'''