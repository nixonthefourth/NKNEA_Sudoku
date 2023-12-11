# Module Import

from tkinter import *
import sqlite3 as sq
from logics import logics
from random import *
from solutions import *
from time import *
from datetime import timedelta

# Define the window

root = Tk()
root.geometry('1280x720')
root.title('Sudoku')
root.resizable(False, False)
root['bg'] = '#FAFAFA'

# Define base variables

value_dict = {}

pseudo_destroy = 3000

timer = None

s = 0

# Labels Definitons

window_label = Label(root, text='SUDOKU', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA',
                     foreground='#060606')

sudoku_status = Label(root, text='', font=('IBM Plex Mono', 20), background='#FAFAFA', foreground='#332E30')


# Grid Creation

def grid_creator():
    global h_line_1, h_line_2, h_line_3, h_line_4, v_line_1, v_line_2, v_line_3, v_line_4
    global entry
    global entry_list
    global frame

    entry_list = []

    frame = Frame(root, background='#060606')
    frame.place(x=395, y=143, width=480, height=480)

    # Cells

    for i in range(9):
        for j in range(9):
            entry = Entry(frame, background='#FAFAFA', foreground='#060606', justify='center', relief='solid',
                          validate='key', font=('IBM Plex Mono', 25, 'bold'),
                          validatecommand=(validation_register, '%P'), borderwidth=3)
            entry.place(x=i * 53, y=j * 53, width=55, height=55)

            value_dict[(i + 2, j + 1)] = entry

            entry_list.append(entry)

    # Horizontal Line Generator

    h_line_1 = Frame(frame, background='#060606', width=480, borderwidth=5)
    h_line_1.place(x=0, y=(-1 + 1) * 53, height=5)

    h_line_2 = Frame(frame, background='#060606', width=480, borderwidth=5)
    h_line_2.place(x=0, y=(2 + 1) * 53, height=5)

    h_line_3 = Frame(frame, background='#060606', width=480, borderwidth=5)
    h_line_3.place(x=0, y=(5 + 1) * 53, height=5)

    h_line_4 = Frame(frame, background='#060606', width=480, borderwidth=5)
    h_line_4.place(x=0, y=(8 + 1) * 53, height=5)

    # Vertical Line Generator
    v_line_1 = Frame(frame, background='#060606', width=5)
    v_line_1.place(x=(-1 + 1) * 52.8, y=0, height=478)

    v_line_2 = Frame(frame, background='#060606', width=5)
    v_line_2.place(x=(2 + 1) * 52.8, y=0, height=478)

    v_line_3 = Frame(frame, background='#060606', width=5)
    v_line_3.place(x=(5 + 1) * 52.8, y=0, height=478)

    v_line_4 = Frame(frame, background='#060606', width=5)
    v_line_4.place(x=(8 + 1) * 52.8, y=0, height=478)


def get_values():
    global break_point
    global frame
    global entry_list

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

    break_point = False

    game_to_score()


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
    try:
        value_dict[(x, y)].insert(0, update_value)

    except Exception:
        pass


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
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    sing_in_label.place(relx=.5, y=120, anchor=CENTER)

    signup_entries = {username_label: (455, 250), username_entry: (630, 290), email_label: (430, 350),
                      email_entry: (630, 390), password_label: (455, 440), password_entry: (630, 480)}

    for x, y in signup_entries.items():
        x.place(x=y[0], y=y[1], anchor=CENTER)

    next_button.place(relx=.5, y=650, anchor=CENTER)


# Continuation of Sign Up Branch
# Sign Up Page to Homepage

def signup_to_homepage():
    global difficulty_choice
    signup_entries_list = [username_label, username_entry, email_label,
                           email_entry, password_label, password_entry]

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280)}

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
                i.place(x=pseudo_destroy, y=pseudo_destroy)

            for x, y in homepage_objects.items():
                x.place(x=y[0], y=y[1])

            score_button_homepage.place(x=540, y=409, width=316, height=263)

            sing_in_label.place(x=pseudo_destroy, y=pseudo_destroy)
            next_button.place(x=pseudo_destroy, y=pseudo_destroy)


# Intro Page to Login Page

def intro_to_login():
    objects = [into_label, logIn_button, signUp_button]

    login_entries = {username_login_label: (455, 250), username_login_entry: (630, 290),
                     password_login_label: (457, 350), password_login_entry: (630, 390)}

    for i in objects:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

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
                        leaderboard_button_homepage: (540, 280)}

    with sq.connect('sudoku_user_data.db') as con:

        cur = con.cursor()

        cur.execute(f'''

                   SELECT username, password FROM users_data
                   WHERE username == '{username_login_entry.get()}' AND password == '{password_login_entry.get()}';

                   ''')

    if len(cur.fetchall()) > 0:

        for i in login_entries_list:
            i.place(x=pseudo_destroy, y=pseudo_destroy)

        for x, y in homepage_objects.items():
            x.place(x=y[0], y=y[1])

        score_button_homepage.place(x=540, y=409, width=316, height=263)

        login_label.place(x=pseudo_destroy, y=pseudo_destroy)

        next_login_button.place(x=pseudo_destroy, y=pseudo_destroy)

    else:

        incorrect_data.place(x=450, y=500)


def homepage_to_difficulty():
    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280), score_button_homepage: (540, 409)}

    for i in homepage_objects:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    difficulty_objects = {difficulty_selection_label: (440, 40), easy_button: (480, 250),
                          medium_button: (480, 330), hard_button: (480, 410)}

    for x, y in difficulty_objects.items():
        x.place(x=y[0], y=y[1])


# Define Timer Function
def update_timer():
    global timer
    global s

    s += 1

    game_board_timer['text']=str(timedelta(seconds=s))
    timer = root.after(1000, update_timer)

def game_timer_start():
    update_timer()

def game_timer_stop():
    global timer

    root.after_cancel(timer)

    game_board_timer['text'] = '00:00'

# Transition to the game board

def difficulty_to_game(difficulty):
    global grid_list

    difficulty_objects = {difficulty_selection_label: (390, 40), easy_button: (480, 250),
                          medium_button: (480, 330), hard_button: (480, 410)}

    for i in difficulty_objects:
        i.place(x=2000, y=2000)

    game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643),
                    game_board_timer: (80, 80)}

    for x, y in game_objects.items():
        x.place(x=y[0], y=y[1])

    window_label.place(x=390, y=10, width=500)
    sudoku_status.place(x=390, y=90, width=500)

    difficulty_dict = {'Easy': 2000, 'Medium': 5000, 'Hard': 8000}
    difficulty_choice = difficulty_dict[difficulty]

    if difficulty == 'Easy':
        grid_list = choice(easy_grid)

    elif difficulty == 'Medium':
        grid_list = choice(medium_grid)

    elif difficulty == 'Hard':
        grid_list = choice(hard_grid)

    grid_creator()

    grid_list_operator(grid_list)

    game_timer_start()

    score_title_label['text'] = f'Your score is: {difficulty_choice}'

def game_to_score():

    # Transit to the new page
    # Destroy Objects
    game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643),
                    game_board_timer: (80, 80)}

    grid_lines = [h_line_1, h_line_2, h_line_3, h_line_4, v_line_1, v_line_2, v_line_3, v_line_4]

    for i in game_objects:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    window_label.place(x=pseudo_destroy, y=pseudo_destroy)
    sudoku_status.place(x=pseudo_destroy, y=pseudo_destroy)

    for i in grid_lines:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    for i in entry_list:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    frame.place(x=pseudo_destroy, y=pseudo_destroy)

    # Create New Objects
    score_title_label.place(x=250, y=180)
    score_button_scorepage.place(x=480, y=300)


def score_to_homepage():
    score_title_label.place(x=pseudo_destroy, y=pseudo_destroy)
    score_button_scorepage.place(x=pseudo_destroy, y=pseudo_destroy)

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280)}

    for x, y in homepage_objects.items():
        x.place(x=y[0], y=y[1])

    score_button_homepage.place(x=540, y=409, width=316, height=263)


def homepage_to_leaderboard():

    # Delete Previous Objects
    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280), score_button_homepage: (540, 409)}

    for i in homepage_objects:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    # Create a table
    table = {leaderboard_title_label: (450, 30), username_label_button: (185, 130), score_label_button: (500, 130),
             time_label_button: (815, 130)}

    for x, y in table.items():
        x.place(x=y[0], y=y[1])

    # Create Table Cells

    # Cell Variables

    username_cell = 185
    score_cell = 499
    time_cell = 814

    # Table Variables

    table_y_0 = 189
    table_y_1 = 248
    table_y_2 = 307
    table_y_3 = 366
    table_y_4 = 425
    table_y_5 = 484

    # Username

    username_cell_0.place(x=username_cell, y=table_y_0)
    username_cell_1.place(x=username_cell, y=table_y_1)
    username_cell_2.place(x=username_cell, y=table_y_2)
    username_cell_3.place(x=username_cell, y=table_y_3)
    username_cell_4.place(x=username_cell, y=table_y_4)
    username_cell_5.place(x=username_cell, y=table_y_5)

    # Score

    score_cell_0.place(x=score_cell, y=table_y_0)
    score_cell_1.place(x=score_cell, y=table_y_1)
    score_cell_2.place(x=score_cell, y=table_y_2)
    score_cell_3.place(x=score_cell, y=table_y_3)
    score_cell_4.place(x=score_cell, y=table_y_4)
    score_cell_5.place(x=score_cell, y=table_y_5)

    # Time

    time_cell_0.place(x=time_cell, y=table_y_0)
    time_cell_1.place(x=time_cell, y=table_y_1)
    time_cell_2.place(x=time_cell, y=table_y_2)
    time_cell_3.place(x=time_cell, y=table_y_3)
    time_cell_4.place(x=time_cell, y=table_y_4)
    time_cell_5.place(x=time_cell, y=table_y_5)

    leaderboard_to_homepage_button.place(x=500, y=600)

def leaderboard_to_homepage():
    cell_list = [username_label_button, score_label_button, time_label_button, username_cell_0, username_cell_1, username_cell_2,
                 username_cell_3, username_cell_4, username_cell_5, score_cell_0, score_cell_1, score_cell_2,
                 score_cell_3, score_cell_4, score_cell_5, time_cell_0, time_cell_1, time_cell_2, time_cell_3,
                 time_cell_4, time_cell_5, leaderboard_to_homepage_button, leaderboard_title_label]

    # Place homepage objects

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280)}

    for x, y in homepage_objects.items():
        x.place(x=y[0], y=y[1])

    score_button_homepage.place(x=540, y=409, width=316, height=263)

    for i in cell_list:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

def homepage_to_profile():

    # Destroy Previous Objects

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280), score_button_homepage: (540, 409)}

    for i in homepage_objects:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    # Profile Elements

    username_title.place(x=80, y=180)

    left_column = 850

    username_profile_label.place(x=left_column, y=180)
    email_profile_label.place(x=left_column, y=230)
    password_profile_label.place(x=left_column, y=290)

    change_details_button.place(x=left_column, y=350)

    profile_to_homepage_button.place(x=500, y=600)


def profile_to_homepage():

    # Destroy previous objects

    profile_elements = [username_title, profile_to_homepage_button, email_profile_label,
                        password_profile_label, change_details_button, username_profile_label]

    for i in profile_elements:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    # Place objects back

    homepage_objects = {homepage_label: (490, 30), play_button_homepage: (420, 155),
                        profile_button_homepage: (540, 155),
                        leaderboard_button_homepage: (540, 280)}

    for x, y in homepage_objects.items():
        x.place(x=y[0], y=y[1])

    score_button_homepage.place(x=540, y=409, width=316, height=263)


# Define function in order to switch page from into to user register
def erase_values():
    global grid_list
    sudoku_status.configure(text='')

    for x in range(2, 11):
        for y in range(1, 10):
            g = value_dict[(x, y)]

            if grid_list[x - 2][y - 1] == 0:
                g.delete(0, 'end')


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

# Game Board Elements

# Define Buttons
exit_button = Button(root, text='Exit', background='#FAFAFA', foreground='#060606', font=('IBM Plex Mono', 20, 'bold'),
                     width=8, height=1, relief='solid', cursor='target', command=root.destroy)

submit_button = Button(root, text='Submit', background='#060606', foreground='#FAFAFA',
                       font=('IBM Plex Mono', 20, 'bold'), width=11, height=1, relief='solid', cursor='target',
                       command=get_values)

clear_button = Button(root, text='Clear', background='#FAFAFA', foreground='#060606',
                      font=('IBM Plex Mono', 20, 'bold'), width=8, height=1, relief='solid', cursor='target',
                      command=erase_values)

game_board_timer = Label(root, text='00:00', font=('IBM Plex Mono', 16, 'bold'), fg='#0D0C0C', bg='#FAFAFA')

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
sing_in_label = Label(root, text='Registration ', font=('IBM Plex Mono', 48, 'bold'), fg='#0D0C0C',
                      background='#FAFAFA')

username_label = Label(root, text='Username: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
username_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid')

email_label = Label(root, text='Email: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
email_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                    bd=2, relief='solid')

password_label = Label(root, text='Password: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', fg='#0D0C0C')
password_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid', show='•')

next_button = Button(root, text='Next', font=('IBM Plex Mono', 20, 'bold'), fg='#0D0C0C', background='#FAFAFA',
                     relief='solid', width='18', cursor='target', command=signup_to_homepage)

# Define Login Page
login_label = Label(root, text='Login ', font=('IBM Plex Mono', 48, 'bold'), fg='#0D0C0C', background='#FAFAFA')

username_login_label = Label(root, text='Username: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                             fg='#0D0C0C')
username_login_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA',
                             fg="#0D0C0C",
                             bd=2, relief='solid')

password_login_label = Label(root, text='Password: ', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                             fg='#0D0C0C')
password_login_entry = Entry(root, width=30, font=('IBM Plex Mono', 20, 'bold'), selectbackground='#FAFAFA',
                             fg="#0D0C0C",
                             bd=2, relief='solid', show='•')

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
                                 foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18,
                                 command=homepage_to_profile)

leaderboard_button_homepage = Button(root, text='Leaderboard', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                                     foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18,
                                     command=homepage_to_leaderboard)

score_button_homepage = Button(root, text='2500p', font=('IBM Plex Mono', 21, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid')

# Difficulty Label
score_title_label = Label(root, text='', font=('IBM Plex Mono', 48, 'bold'),
                          background='#FAFAFA', foreground='#060606')

score_button_scorepage = Button(root, text='Home', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                                foreground='#0D0C0C', relief='solid', width='18', cursor='target',
                                command=score_to_homepage)

# Buttons
# Home
homepage_button = Button(root, text='Home', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18', cursor='target')

# Exit
exit_score_button = Button(root, text='Exit', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                           foreground='#0D0C0C', relief='solid', width='18', cursor='target', command=root.destroy)

# Difficulty Page
# Difficulty Label
difficulty_selection_label = Label(root, text='Difficulty', font=('IBM Plex Mono', 48, 'bold'),
                                   background='#FAFAFA', foreground='#060606')

# Buttons
# Easy
easy_button = Button(root, text='Easy', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda: difficulty_to_game('Easy'))

# Medium
medium_button = Button(root, text='Medium', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                       foreground='#0D0C0C', relief='solid', width='18', cursor='target',
                       command=lambda: difficulty_to_game('Medium'))

# Hard
hard_button = Button(root, text='Hard', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda: difficulty_to_game('Hard'))

# Leaderboard Objects
leaderboard_title_label = Label(root, text='Leaderboard', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA',
                                foreground='#060606')

username_label_button = Button(root, text='Username', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                               foreground='#FAFAFA', relief='solid', width='18')

score_label_button = Button(root, text='Score', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                               foreground='#FAFAFA', relief='solid', width='18')

time_label_button = Button(root, text='Time', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                               foreground='#FAFAFA', relief='solid', width='18')

leaderboard_to_homepage_button = Button(root, text='Back', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                               foreground='#FAFAFA', relief='solid', width='18', command=leaderboard_to_homepage)

# Cells
username_cell_0 = Button(root, text='username', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

username_cell_1 = Button(root, text='username', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

username_cell_2 = Button(root, text='username', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

username_cell_3 = Button(root, text='username', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

username_cell_4 = Button(root, text='username', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

username_cell_5 = Button(root, text='username', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

score_cell_0 = Button(root, text='score', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

score_cell_1 = Button(root, text='score', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

score_cell_2 = Button(root, text='score', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

score_cell_3 = Button(root, text='score', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

score_cell_4 = Button(root, text='score', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

score_cell_5 = Button(root, text='score', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

time_cell_0 = Button(root, text='time', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

time_cell_1 = Button(root, text='time', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

time_cell_2 = Button(root, text='time', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

time_cell_3 = Button(root, text='time', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

time_cell_4 = Button(root, text='time', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

time_cell_5 = Button(root, text='time', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

# Profile Page

username_title = Label(root, text='Welcome back!', font=('IBM Plex Mono', 48, 'bold'),
                                   background='#FAFAFA', foreground='#060606')

username_profile_label = Label(root, text='username', font=('IBM Plex Mono', 20, 'bold'),
                                   background='#FAFAFA', foreground='#060606')

email_profile_label = Label(root, text='email', font=('IBM Plex Mono', 20, 'bold'),
                                   background='#FAFAFA', foreground='#060606')

password_profile_label = Label(root, text='password', font=('IBM Plex Mono', 20, 'bold'),
                                   background='#FAFAFA', foreground='#060606')

change_details_button = Button(root, text='Change Details', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18')

profile_to_homepage_button = Button(root, text='Back', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                               foreground='#FAFAFA', relief='solid', width='18', command=profile_to_homepage)

root.mainloop()