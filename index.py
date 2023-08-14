# Import Libraries

from tkinter import *

# Window Creation
root = Tk()
root.geometry('1280x720')
root.title('Sudoku')
root.resizable(False, False)
root['bg'] = '#FAFAFA'

# Labels Definitons

window_label = Label(root, text='SUDOKU', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA', foreground='#060606')
window_label.place(x=390, y=10, width=500)

sudoku_status = Label(root, text='Game Status', font=('IBM Plex Mono', 20), background='#FAFAFA', foreground='#332E30')
sudoku_status.place(x=390, y=90, width=500)

value_dict = {}

def validation_sudoku(user_entry):
     output_true = (user_entry.isdigit() or user_entry == ('')) and len(user_entry) < 2
     return output_true

validation_register = root.register(validation_sudoku)

# Grid Creation

def grid_creator():
     frame = Frame(root, background='#060606')
     frame.place(x=395, y=143, width=480, height=480)

     grid_font = font=('IBMPlexMono-Bold', 22)

     # Cells

     for i in range(9):
          for j in range(9):
               entry = Entry(frame, background='#FAFAFA', foreground='#060606', justify='center', relief='solid', validate='key', validatecommand=(validation_register, '%P'), borderwidth=3)
               entry.place(x=i*53, y=j*53, width=55, height=55)

               value_dict[(i + 2, j + 1)] = entry

     # Horizontal Line Generator
     for i in range(-1, 9, 3):
          Frame(frame, background='#060606', width=480, borderwidth=5).place(x=0, y=(i+1)*53, height=5)

     # Vertical Line Generator
     for j in range(-1, 9, 3):
          Frame(frame, background='#060606', width = 5).place(x=(j+1)*52.8, y=0, height=478)



def erase_values():
     sudoku_status.configure(text='')

     for x in range(2, 11):
          for y in range(1, 10):
               clear_dict = value_dict[(x, y)]
               clear_dict.delete(0, 'end')

def get_values():
     entry_values = []

     sudoku_status.configure(text='')

     for x in range(2, 11):
          empty_list = []

          for y in range(2, 11):
               empty_dict = value_dict[(x, y)].get()

               if empty_dict == '':
                    empty_list.append(0)

               else:
                    empty_list.append(int(empty_dict))
          
          entry_values.append(empty_list)

     update_function(entry_values)

# Bottom Buttons

exit_button = Button(root, text='Exit', background='#FAFAFA', foreground='#060606', font=('IBM Plex Mono', 20, 'bold'), width = 8, height= 1, relief='solid', cursor='target', command=root.destroy)
exit_button.place(x = 394, y = 643)

submit_button = Button(root, text='Submit', background='#060606', foreground='#FAFAFA', font=('IBM Plex Mono', 20, 'bold'), width = 11, height= 1, relief='solid', cursor='target', command=get_values)
submit_button.place(x = 540, y = 643)

clear_button = Button(root, text='Clear', background='#FAFAFA', foreground='#060606', font=('IBM Plex Mono', 20, 'bold'), width = 8, height= 1, relief='solid', cursor='target', command=erase_values)
clear_button.place(x = 730, y = 643)

grid_creator()

def update_widgets(x, y, update_value):
     value_dict[(x, y)].insert(0, update_value)

root.mainloop() 
