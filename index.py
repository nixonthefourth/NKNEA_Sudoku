from tkinter import *
import sqlite3 as sq
from logics import logics
from random import *
from solutions import *
from datetime import *

root = Tk()
root.geometry('1280x720')
root.title('Sudoku')
root.resizable(False, False)
root['bg'] = '#FAFAFA'

value_dict = {}


# Labels Definitons

window_label = Label(root, text='SUDOKU', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA', foreground='#060606')

sudoku_status = Label(root, text='', font=('IBM Plex Mono', 20), background='#FAFAFA', foreground='#332E30')

# Define function in order to switch page from into to user register
def erase_values():
     sudoku_status.configure(text='')

     for x in range(2, 11):
          for y in range(1, 10):
               g = value_dict[(x, y)]

               if grid_list[x-2][y-1] == 0:
                    g.delete(0, 'end')

# Grid Creation

def grid_creator():
     frame = Frame(root, background='#060606')
     frame.place(x=395, y=143, width=480, height=480)

     # Cells

     for i in range(9):
          for j in range(9):
               entry = Entry(frame, background='#FAFAFA', foreground='#060606', justify='center', relief='solid',
                             validate='key', font=('IBM Plex Mono', 25, 'bold'),
                             validatecommand=(validation_register, '%P'), borderwidth=3)
               entry.place(x=i*53, y=j*53, width=55, height=55)

               value_dict[(i + 2, j + 1)] = entry
               

     # Horizontal Line Generator
     for i in range(-1, 9, 3):
          Frame(frame, background='#060606', width=480, borderwidth=5).place(x=0, y=(i+1)*53, height=5)

     # Vertical Line Generator
     for j in range(-1, 9, 3):
          Frame(frame, background='#060606', width = 5).place(x=(j+1)*52.8, y=0, height=478)


def signup_to_game():
     global grid_list
     global game_objects
     global t1

     game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643)}

     with sq.connect('sudoku_user_data.db') as con:
          cur = con.cursor()

          if len(username_entry.get()) == 0:

               incorrect_username_label.place(x=440, y=540)

               username_label['fg'] = '#C51605'

          elif '@' not in email_entry.get():

               incorrect_username_label['text'] = ''

               incorrect_email_label.place(x=470, y=540)

          elif len(email_entry.get()) == 0:

               username_label['fg'] = '#0D0C0C'

               incorrect_email_label['text'] = ''

               empty_email_label.place(x=460, y=540)

               email_label['fg'] = '#C51605'

          elif len(password_entry.get()) < 8:

               username_label['fg'] = '#0D0C0C'
               email_label['fg'] = '#0D0C0C'

               empty_email_label['text'] = ''

               incorrect_password_label.place(x=280, y=540)

               password_label['fg'] = '#C51605'

          elif str(password_entry.get()).isalnum() or str(password_entry.get()).isalpha() or str(
                  password_entry.get()).isdigit():

               incorrect_password_label['text'] = ''
               incorrect_password_type_label['text'] = ''

               incorrect_password_type_label.place(x=120, y=540)

          else:

               cur.execute(f'''

               INSERT INTO users_data(username, email, password)
               VALUES ( '{username_entry.get()}', '{email_entry.get()}', '{password_entry.get()}');

               ''')

               for i in signup_entries.keys():
                    i.destroy()

               sing_in_label.destroy()
               next_button.destroy()

               for x, y in game_objects.items():
                    x.place(x=y[0], y=y[1])

               window_label.place(x=390, y=10, width=500)
               sudoku_status.place(x=390, y=90, width=500)

               grid_list = choice(medium_grid)

               grid_creator()

               grid_list_operator(grid_list)

               #t1 = datetime.now()


def get_values():
     entry_values = []

     sudoku_status.configure(text='')

     for x in range(2, 11):
          empty_list = []

          for y in range(1, 10):
               empty_dict = value_dict[(x, y)].get()

               if empty_dict == '':
                    empty_list.append(0)

               else:
                    empty_list.append(int(empty_dict))
          
          entry_values.append(empty_list)
          
     update_value(entry_values)

     '''t2 = datetime.now()

     delta_t = t1 - t2

     print(delta_t)'''

def intro_to_signup():
     global signup_entries
     
     objects = [into_label, logIn_button, signUp_button]
     for i in objects:
          i.destroy()

     sing_in_label.place(relx=.5, y=120, anchor=CENTER)

     signup_entries = {username_label : (455, 250), username_entry : (630, 290), email_label : (430, 350),
                       email_entry : (630, 390), password_label : (455, 440), password_entry : (630, 480)}

     for x, y in signup_entries.items():
        x.place(x = y[0], y = y[1], anchor=CENTER)

     next_button.place(relx=.5, y=650, anchor=CENTER)

def validation_sudoku(user_entry):
     output_true = (user_entry.isdigit() or user_entry == ('')) and len(user_entry) < 2
     return output_true

validation_register = root.register(validation_sudoku)

def grid_list_operator(grid_list_counter):
     for x in range(9):
          for y in range(9):
               m = grid_list_counter[x][y]
               
               if m != 0:
                    value_dict[(x+2, y+1)].insert(0, str(m))


# Bottom Buttons

def update_widgets(x, y, update_value):
     value_dict[(x, y)].insert(0, update_value)

def update_value(x):
     l = logics(x)

     if l != 'No':
          for x in range(2, 11):
               for y in range(1, 10):

                    if not value_dict[(x, y)].get():
                         value_dict[(x, y)].delete(0, 'end')

                         root.after((x + y) * 100, update_widgets, x, y, l[x-2][y-1])
          
          sudoku_status['text'] = 'Sudoku is solved'

     else:

          sudoku_status['text'] = 'Sudoku isn\'t solved'

def intro_to_login():
     objects = [into_label, logIn_button, signUp_button]
     login_entries = {username_login_label: (455, 250), username_login_entry: (630, 290),
                      password_login_label: (430, 350), password_login_entry: (630, 390)}

     for i in objects:
          i.destroy()

     login_label.place(relx=.5, y=120, anchor=CENTER)

     for x, y in login_entries.items():
          x.place(x=y[0], y=y[1], anchor=CENTER)

     next_login_button.place(relx=.5, y=650, anchor=CENTER)
def login_to_game():

     with sq.connect('sudoku_user_data.db') as con:

          cur = con.cursor()


          cur.execute(f'''

                    SELECT username, password FROM users_data
                    WHERE username == '{username_login_entry.get()}' AND password == '{password_login_entry.get()}';

                    ''')

     if len(cur.fetchall()) > 0:
          game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643)}
          login_entries = {username_login_label: (455, 250), username_login_entry: (630, 290),
                           password_login_label: (430, 350), password_login_entry: (630, 390)}

          for i in login_entries.keys():
               i.destroy()

          login_label.destroy()
          next_login_button.destroy()

          for x, y in game_objects.items():
               x.place(x=y[0], y=y[1])


          window_label.place(x=390, y=10, width=500)
          sudoku_status.place(x=390, y=90, width=500)

          grid_list = easy_grid_1

          grid_creator()

          grid_list_operator(grid_list)

     else:
          incorrect_data.place(x=450, y=500)

# Game Page

# Define Buttons for signup page

incorrect_email_label = Label(root, text='There is no @ in email', background='#FAFAFA', foreground='#C51605',
                              font=('IBM Plex Mono', 20, 'bold'))

empty_email_label = Label(root, text='Email entry is empty', background='#FAFAFA', foreground='#C51605',
                              font=('IBM Plex Mono', 20, 'bold'))

incorrect_username_label = Label(root, text='Username entry is empty', background='#FAFAFA', foreground='#C51605',
                              font=('IBM Plex Mono', 20, 'bold'))

incorrect_password_label = Label(root, text='Password entry is too short (8 chars minimum)', background='#FAFAFA',
                                 foreground='#C51605', font=('IBM Plex Mono', 20, 'bold'))

incorrect_password_type_label = Label(root, text='Password should contains strings, special characters and numbers',
                                      background='#FAFAFA', foreground='#C51605', font=('IBM Plex Mono', 20, 'bold'))

# Labels for login page

incorrect_data = Label(root, text='Incorrect Login Details', background='#FAFAFA', foreground='#C51605',
                              font=('IBM Plex Mono', 20, 'bold'))

# Define Buttons

exit_button = Button(root, text='Exit', background='#FAFAFA', foreground='#060606', font=('IBM Plex Mono', 20, 'bold'),
                     width = 8, height= 1, relief='solid', cursor='target', command=root.destroy)

submit_button = Button(root, text='Submit', background='#060606', foreground='#FAFAFA',
                       font=('IBM Plex Mono', 20, 'bold'), width = 11, height= 1, relief='solid', cursor='target',
                       command=get_values)

clear_button = Button(root, text='Clear', background='#FAFAFA', foreground='#060606',
                      font=('IBM Plex Mono', 20, 'bold'), width = 8, height= 1, relief='solid', cursor='target',
                      command=erase_values)
     
# Define Intro Page

into_label = Label(root, text='SUDOKU', font=('IBM Plex Mono', 48, 'bold'), fg='#0D0C0C', bg='#FAFAFA')
into_label.place(relx=.5, y=220, anchor=CENTER)

logIn_button = Button(root, text='Log In', font=('IBM Plex Mono', 20, 'bold'), fg='#0D0C0C', background='#FAFAFA',
                      relief='solid', width='18', cursor='target', command=intro_to_login)
logIn_button.place(relx=.37, y=350, anchor=CENTER)

signUp_button = Button(root, text='Sign Up', font=('IBM Plex Mono', 20, 'bold'), fg='#FAFAFA', background='#0D0C0C',
                       relief='solid', width='18', cursor='target', command=intro_to_signup)
signUp_button.place(relx=.64, y=350, anchor=CENTER)

# Define Sign Up Page

sing_in_label = Label(root, text='Registration ', font=('IBM Plex Mono', 48, 'bold'), fg='#0D0C0C', background='#FAFAFA')

username_label = Label(root, text='Username: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
username_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid')

email_label = Label(root, text='Email: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
email_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                    bd=2, relief='solid')

password_label = Label(root, text='Password: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
password_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid', show = '•')

next_button = Button(root, text='Next', font=('IBM Plex Mono', 20, 'bold'), fg='#0D0C0C', background='#FAFAFA',
                     relief='solid', width='18', cursor='target', command= signup_to_game)

# Define Login Function

login_label = Label(root, text='Login ', font=('IBM Plex Mono', 48, 'bold'), fg='#0D0C0C', background='#FAFAFA')

username_login_label = Label(root, text='Username: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
username_login_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid')

password_login_label = Label(root, text='Password', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
password_login_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid', show = '•')

next_login_button = Button(root, text='Next', font=('IBM Plex Mono', 20, 'bold'), fg='#0D0C0C', background='#FAFAFA',
                     relief='solid', width='18', cursor='target', command= login_to_game)

root.mainloop()