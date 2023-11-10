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

# Grid Creation

def grid_creator():
     global h_line_1, h_line_2, h_line_3, h_line_4, v_line_1, v_line_2, v_line_3, v_line_4

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

     h_line_1 = Frame(frame, background='#060606', width=480, borderwidth=5)
     h_line_1.place(x=0, y=(-1+1)*53, height=5)

     h_line_2 = Frame(frame, background='#060606', width=480, borderwidth=5)
     h_line_2.place(x=0, y=(2 + 1) * 53, height=5)

     h_line_3 = Frame(frame, background='#060606', width=480, borderwidth=5)
     h_line_3.place(x=0, y=(5 + 1) * 53, height=5)

     h_line_4 = Frame(frame, background='#060606', width=480, borderwidth=5)
     h_line_4.place(x=0, y=(8 + 1) * 53, height=5)

     # Vertical Line Generator
     v_line_1 = Frame(frame, background='#060606', width = 5)
     v_line_1.place(x=(-1+1)*52.8, y=0, height=478)

     v_line_2 = Frame(frame, background='#060606', width=5)
     v_line_2.place(x=(2 + 1) * 52.8, y=0, height=478)

     v_line_3 = Frame(frame, background='#060606', width=5)
     v_line_3.place(x=(5 + 1) * 52.8, y=0, height=478)

     v_line_4 = Frame(frame, background='#060606', width=5)
     v_line_4.place(x=(8 + 1) * 52.8, y=0, height=478)

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


def validation_sudoku(user_entry):
    output_true = (user_entry.isdigit() or user_entry == ('')) and len(user_entry) < 2
    return output_true


validation_register = root.register(validation_sudoku)


def grid_list_operator(grid_list_counter):
    for x in range(9):
        for y in range(9):
            m = grid_list_counter[x][y]

            if m != 0:
                value_dict[(x + 2, y + 1)].insert(0, str(m))

def update_widgets(x, y, update_value):
    value_dict[(x, y)].insert(0, update_value)


def update_value(x):
    l = logics(x)

    if l != 'No':
        for x in range(2, 11):
            for y in range(1, 10):

                if not value_dict[(x, y)].get():
                    value_dict[(x, y)].delete(0, 'end')

                    root.after((x + y) * 100, update_widgets, x, y, l[x - 2][y - 1])

        sudoku_status['text'] = 'Sudoku is solved'

    else:

        sudoku_status['text'] = 'Sudoku isn\'t solved'


# Transition Functions

# Intro Page to Sign Up Page
def intro_to_signup():
    global signup_entries

    objects = [into_label, logIn_button, signUp_button]
    for i in objects:
        i.destroy()

    sing_in_label.place(relx=.5, y=120, anchor=CENTER)

    signup_entries = {username_label: (455, 250), username_entry: (630, 290), email_label: (430, 350),
                      email_entry: (630, 390), password_label: (455, 440), password_entry: (630, 480)}

    for x, y in signup_entries.items():
        x.place(x=y[0], y=y[1], anchor=CENTER)

    next_button.place(relx=.5, y=650, anchor=CENTER)

# Continuation of Sign Up Branch
# Sign Up Page to Homepage

def signup_to_homepage():
    signup_entries_list = [username_label, username_entry, email_label,
                      email_entry, password_label, password_entry]

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280), score_button_homepage: (540, 409)}

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

            for i in signup_entries_list:
                i.destroy()

            for x, y in homepage_objects.items():
                x.place(x=y[0], y=y[1])

            sing_in_label.destroy()
            next_button.destroy()

# Intro Page to Login Page

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

# Continuation of the Login Branch
# Login Page to Homepage

def login_to_homepage():
    login_entries_list = [username_login_label, username_login_entry,
                     password_login_label, password_login_entry]

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280), score_button_homepage: (540, 409)}

    with sq.connect('sudoku_user_data.db') as con:

        cur = con.cursor()

        cur.execute(f'''

                   SELECT username, password FROM users_data
                   WHERE username == '{username_login_entry.get()}' AND password == '{password_login_entry.get()}';

                   ''')

    if len(cur.fetchall()) > 0:

        for i in login_entries_list:
            i.destroy()

        for x, y in homepage_objects.items():
            x.place(x=y[0], y=y[1])

        login_label.destroy()

        next_login_button.destroy()

    else:

        incorrect_data.place(x=450, y=500)

def homepage_to_difficulty():
    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280), score_button_homepage: (540, 409)}

    for i in homepage_objects:
        i.destroy()

    difficulty_objects = {difficulty_selection_label: (390, 40), easy_button: (480, 250),
                          medium_button: (480, 330), hard_button: (480, 410)}

    for x, y in difficulty_objects.items():
        x.place(x=y[0], y=y[1])

def difficulty_to_game():
    global grid_list

    difficulty_objects = {difficulty_selection_label: (390, 40), easy_button: (480, 250),
                          medium_button: (480, 330), hard_button: (480, 410)}

    for i in difficulty_objects:
        i.destroy()

    game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643)}

    for x, y in game_objects.items():
        x.place(x=y[0], y=y[1])

    window_label.place(x=390, y=10, width=500)
    sudoku_status.place(x=390, y=90, width=500)

    grid_list = easy_grid_1

    grid_creator()

    grid_list_operator(grid_list)

def game_to_score():
    game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643)}

    grid_lines = [h_line_1, h_line_2, h_line_3, h_line_4, v_line_1, v_line_2, v_line_3, v_line_4]

    for i in game_objects:
        i.destroy()

    window_label.destroy()
    sudoku_status.destroy()

    for i in grid_lines:
        i.destroy()

def score_to_homepage():
    pass

def homepage_to_leaderboard():
    pass

def leaderboard_to_homepage():
    pass

def homepage_to_profile():
    pass

def profile_to_homepage():
    pass

# Define function in order to switch page from into to user register
def erase_values():
     global grid_list
     sudoku_status.configure(text='')

     for x in range(2, 11):
          for y in range(1, 10):
               g = value_dict[(x, y)]

               if grid_list[x-2][y-1] == 0:
                    g.delete(0, 'end')

def button_choice(button_press):
    button_value = ''
    difficulty_points = [2000, 5000, 8000]

    if button_press == easy_button:
        button_value = 'Easy'
        difficulty_choice = difficulty_points[0]

    elif button_press == medium_button:
        button_value = 'Medium'
        difficulty_choice = difficulty_points[1]

    elif button_press == hard_button:
        button_value = 'Hard'
        difficulty_choice = difficulty_points[2]

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
                     relief='solid', width='18', cursor='target', command=signup_to_homepage)

# Define Login Function

login_label = Label(root, text='Login ', font=('IBM Plex Mono', 48, 'bold'), fg='#0D0C0C', background='#FAFAFA')

username_login_label = Label(root, text='Username: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
username_login_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid')

password_login_label = Label(root, text='Password', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
password_login_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid', show = '•')

next_login_button = Button(root, text='Next', font=('IBM Plex Mono', 20, 'bold'), fg='#0D0C0C', background='#FAFAFA',
                     relief='solid', width='18', cursor='target', command=login_to_homepage)

# Homepage
# Homepage label

homepage_label = Label(root, text='Homepage', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA',
                       foreground='#060606')

# Grid
play_button_homepage = Button(root, text='Play', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                              foreground='#FAFAFA', relief='solid', cursor='target',
                              height=14, width=7, command=homepage_to_difficulty)

profile_button_homepage = Button(root, text='View Profile', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                                 foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18)

leaderboard_button_homepage = Button(root, text='Leaderboard', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                                     foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18)

score_button_homepage = Button(root, text='2354p', font=('IBM Plex Mono', 32, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', height=4, width=11)

# Difficulty Label

score_title_label = Label(root, text='Your score is:  2230P', font=('IBM Plex Mono', 48, 'bold'),
                          background='#FAFAFA', foreground='#060606')

# Buttons
# Home
homepage_button = Button(root, text='Home', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18', cursor='target')

# Rematch

rematch_button = Button(root, text='Rematch', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                        foreground='#0D0C0C', relief='solid', width='18', cursor='target')

# exit

exit_score_button = Button(root, text='Exit', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                           foreground='#0D0C0C', relief='solid', width='18', cursor='target', command=root.destroy)

# Difficulty Page
# Difficulty Label

difficulty_selection_label = Label(root, text='Difficulty', font=('IBM Plex Mono', 48, 'bold'),
                                   background='#FAFAFA', foreground='#060606')

# Buttons
# Easy
easy_button = Button(root, text='Easy', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda : button_choice(easy_button))

# Medium

medium_button = Button(root, text='Medium', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                       relief='solid', width='18', cursor='target', command=lambda : button_choice(medium_button))

# Hard

hard_button = Button(root, text='Hard', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda : button_choice(hard_button))

root.mainloop()