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

bold_20 = ('IBM Plex Mono', 20, 'bold')
bold_48 = ('IBM Plex Mono', 48, 'bold')

timer = None

s = 0

# Labels Definitons

window_label = Label(root, text='SUDOKU', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA',
                     foreground='#060606')

sudoku_status = Label(root, text='', font=('IBM Plex Mono', 20), background='#FAFAFA', foreground='#332E30')

'''Functions'''


# Function that helps database with retrieving score value

def get_user_score():
    global transfer_score

    with sq.connect('sudoku_user_data.db') as con:
        cur = con.cursor()

        cur.execute(f'''

            SELECT score FROM users_data
            WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';

            ''')

        transfer_score = cur.fetchall()

        score_button_homepage['text'] = transfer_score


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

            score_button_homepage['text'] = '0'

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
                   WHERE username = '{username_login_entry.get()}' AND password = '{password_login_entry.get()}';

                   ''')

    if len(cur.fetchall()) > 0:

        for i in login_entries_list:
            i.place(x=pseudo_destroy, y=pseudo_destroy)

        for x, y in homepage_objects.items():
            x.place(x=y[0], y=y[1])

        score_button_homepage.place(x=540, y=409, width=316, height=263)

        login_label.place(x=pseudo_destroy, y=pseudo_destroy)

        next_login_button.place(x=pseudo_destroy, y=pseudo_destroy)

        incorrect_data['text'] = ''

        get_user_score()

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
    global s
    global timer

    s += 1
    game_board_timer['text'] = str(timedelta(seconds=s))
    timer = root.after(1000, update_timer)

def start_timer():
    global timer
    global s

    if timer is not None:
        root.after_cancel(timer)
        timer = None
        game_board_timer['text'] = '00:00'
        s=0

    if timer is None:
        update_timer()


# Transition to the game board

def difficulty_to_game(difficulty):
    global grid_list
    global difficulty_start_score

    difficulty_objects = {difficulty_selection_label: (390, 40), easy_button: (480, 250),
                          medium_button: (480, 330), hard_button: (480, 410)}

    for i in difficulty_objects:
        i.place(x=2000, y=2000)

    game_objects = {exit_button: (394, 643), submit_button: (540, 643), clear_button: (730, 643),
                    game_board_timer: (60, 25)}

    for x, y in game_objects.items():
        x.place(x=y[0], y=y[1])

    window_label.place(x=390, y=10, width=500)
    sudoku_status.place(x=390, y=90, width=500)

    difficulty_dict = {
        'Easy': 3000,
        'Medium': 5000,
        'Hard': 8000
    }

    difficulty_choice = difficulty_dict[difficulty]
    difficulty_start_score = difficulty_dict.get(difficulty)

    if difficulty == 'Easy':
        grid_list = choice(easy_grid)

    elif difficulty == 'Medium':
        grid_list = choice(medium_grid)

    elif difficulty == 'Hard':
        grid_list = choice(hard_grid)

    grid_creator()

    grid_list_operator(grid_list)

    start_timer()

    score_title_label['text'] = f'Your score is: {difficulty_choice}'


# Score Calculation Script and Transition

def game_to_score():
    global difficulty_start_score
    global s

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

    # Score Calculation
    end_game_score = difficulty_start_score - s

    # Create New Objects
    score_title_label['text'] = end_game_score

    # Put This Score into the database

    with sq.connect('sudoku_user_data.db') as con:

        cur = con.cursor()

        cur.execute(f'''


                   UPDATE users_data
                   SET score = '{end_game_score}'
                   WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';

                   ''')

    score_title_label.place(x=560, y=180)
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

    get_user_score()


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
    cell_list = [username_label_button, score_label_button, time_label_button, username_cell_0, username_cell_1,
                 username_cell_2,
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

    get_user_score()


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

    get_userdata_profile()


def profile_to_homepage():

    # Destroy previous objects

    profile_elements = [username_title, profile_to_homepage_button, email_profile_label,
                        password_profile_label, change_details_button, username_profile_label]

    for i in profile_elements:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    # Place objects back

    homepage_objects = {
        homepage_label: (490, 30), play_button_homepage: (420, 155),
        profile_button_homepage: (540, 155),
        leaderboard_button_homepage: (540, 280)
    }

    for x, y in homepage_objects.items():
        x.place(x=y[0], y=y[1])

    score_button_homepage.place(x=540, y=409, width=316, height=263)

    get_user_score()

'''Code for Change Personal Details Page'''

def profile_to_selection():
    profile_elements = [username_title, profile_to_homepage_button, email_profile_label,
                        password_profile_label, change_details_button, username_profile_label]
    for i in profile_elements:
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    selection_elements = {
        selection_password: (640, 350),
        selection_email: (300, 350),
        selection_title: (355, 250)
    }
    for x, y in selection_elements.items():
        x.place(x=y[0], y=y[1])

def selection_to_email():
    selection_elements = {
        selection_password: (640, 350),
        selection_email: (300, 350),
        selection_title: (350, 250)
    }
    for i in selection_elements.keys():
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    email_selection_elements = {
        email_title: (380, 150),
        email_selection_label: (378, 250),
        email_selection_entry: (380, 290),
        next_email_button: (475, 450)
    }
    for x, y in email_selection_elements.items():
        x.place(x=y[0], y=y[1])

def email_to_profile():
    email_selection_elements = {
        email_title: (379, 150),
        email_selection_label: (378, 250),
        email_selection_entry: (380, 290),
        next_email_button: (475, 450)
    }

    for i in email_selection_elements.keys():
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    with sq.connect('sudoku_user_data.db') as con:
        cur = con.cursor()

        cur.execute(f''' 

            UPDATE users_data
            SET email = '{email_selection_entry.get()}'
            WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';


        ''')

    username_title.place(x=80, y=180)

    left_column = 850

    username_profile_label.place(x=left_column, y=180)
    email_profile_label.place(x=left_column, y=230)
    password_profile_label.place(x=left_column, y=290)

    change_details_button.place(x=left_column, y=350)

    profile_to_homepage_button.place(x=500, y=600)

    get_userdata_profile()

def selection_to_password():
    selection_elements = {
        selection_password: (640, 350),
        selection_email: (300, 350),
        selection_title: (350, 250)
    }
    for i in selection_elements.keys():
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    password_selection_elements = {
        password_title: (379, 150),
        password_selection_label: (378, 250),
        password_selection_entry: (380, 290),
        next_password_button: (475, 450)
    }
    for x, y in password_selection_elements.items():
        x.place(x=y[0], y=y[1])

def password_to_profile():
    password_selection_elements = {
        password_title: (379, 150),
        password_selection_label: (378, 250),
        password_selection_entry: (380, 290),
        next_password_button: (475, 450)
    }

    for i in password_selection_elements.keys():
        i.place(x=pseudo_destroy, y=pseudo_destroy)

    with sq.connect('sudoku_user_data.db') as con:
        cur = con.cursor()

        cur.execute(f''' 

                UPDATE users_data
                SET password = '{password_selection_entry.get()}'
                WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';


            ''')

    username_title.place(x=80, y=180)

    left_column = 850

    username_profile_label.place(x=left_column, y=180)
    email_profile_label.place(x=left_column, y=230)
    password_profile_label.place(x=left_column, y=290)

    change_details_button.place(x=left_column, y=350)

    profile_to_homepage_button.place(x=500, y=600)

    get_userdata_profile()

'''Function That Retrieves Stored Data From Table'''

profile_username = None
profile_password = None
profile_email = None

def get_userdata_profile():
    global profile_username, profile_password, profile_email

    with sq.connect('sudoku_user_data.db') as con:
        cur = con.cursor()
        cur.execute(f''' 

            SELECT username FROM users_data
            WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';

        ''')

        profile_username = cur.fetchall()

    with sq.connect('sudoku_user_data.db') as con:
        cur = con.cursor()
        cur.execute(f''' 

            SELECT password FROM users_data
            WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';

        ''')

        profile_password = cur.fetchall()

    with sq.connect('sudoku_user_data.db') as con:
        cur = con.cursor()
        cur.execute(f''' 

            SELECT email FROM users_data
            WHERE username = '{username_login_entry.get()}' OR username = '{username_entry.get()}';

        ''')

        profile_email = cur.fetchall()

    username_profile_label['text'] = profile_username
    email_profile_label['text'] = profile_email
    password_profile_label['text'] = profile_password


def erase_values():
    global grid_list
    sudoku_status.configure(text='')

    for x in range(2, 11):
        for y in range(1, 10):
            g = value_dict[(x, y)]

            if grid_list[x - 2][y - 1] == 0:
                g.delete(0, 'end')


'''Game Objects'''

# Signup Page Failure Elements

incorrect_email_label = Label(root, text='There is no @ in email', background='#FAFAFA', foreground='#C51605',
                              font=bold_20)
empty_email_label = Label(root, text='Email entry is empty', background='#FAFAFA', foreground='#C51605',
                          font=bold_20)
incorrect_username_label = Label(root, text='Username entry is empty', background='#FAFAFA', foreground='#C51605',
                                 font=bold_20)
incorrect_password_label = Label(root, text='Password entry is too short (8 chars minimum)', background='#FAFAFA',
                                 foreground='#C51605', font=bold_20)
incorrect_password_type_label = Label(root, text='Password should contains strings, special characters and numbers',
                                      background='#FAFAFA', foreground='#C51605', font=bold_20)

# Login Page Failure Elements

incorrect_data = Label(root, text='Incorrect Login Details', background='#FAFAFA', foreground='#C51605',
                       font=bold_20)

'''Game Grid'''

# Service Elements

exit_button = Button(root, text='Exit', background='#FAFAFA', foreground='#060606', font=bold_20,
                     width=8, height=1, relief='solid', cursor='target', command=root.destroy)
submit_button = Button(root, text='Submit', background='#060606', foreground='#FAFAFA',
                       font=bold_20, width=11, height=1, relief='solid', cursor='target',
                       command=get_values)
clear_button = Button(root, text='Clear', background='#FAFAFA', foreground='#060606',
                      font=bold_20, width=8, height=1, relief='solid', cursor='target',
                      command=erase_values)
game_board_timer = Label(root, text='', font=('IBM Plex Mono', 16, 'bold'), fg='#0D0C0C', bg='#FAFAFA')

'''Intro Page'''

into_label = Label(root, text='SUDOKU', font=bold_48, fg='#0D0C0C', bg='#FAFAFA')
into_label.place(relx=.5, y=220, anchor=CENTER)
logIn_button = Button(root, text='Log In', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                      relief='solid', width='18', cursor='target', command=intro_to_login)
logIn_button.place(relx=.37, y=350, anchor=CENTER)
signUp_button = Button(root, text='Sign Up', font=bold_20, fg='#FAFAFA', background='#0D0C0C',
                       relief='solid', width='18', cursor='target', command=intro_to_signup)
signUp_button.place(relx=.64, y=350, anchor=CENTER)

'''Signup Page'''

sing_in_label = Label(root, text='Registration ', font=bold_48, fg='#0D0C0C',
                      background='#FAFAFA')
username_label = Label(root, text='Username: ', font=bold_20, background='#FAFAFA', fg='#0D0C0C')
username_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid')
email_label = Label(root, text='Email: ', font=bold_20, background='#FAFAFA', fg='#0D0C0C')
email_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA', fg="#0D0C0C",
                    bd=2, relief='solid')
password_label = Label(root, text='Password: ', font=bold_20, background='#FAFAFA', fg='#0D0C0C')
password_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA', fg="#0D0C0C",
                       bd=2, relief='solid', show='•')
next_button = Button(root, text='Next', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                     relief='solid', width='18', cursor='target', command=signup_to_homepage)

'''Login Page'''

login_label = Label(root, text='Login ', font=bold_48, fg='#0D0C0C', background='#FAFAFA')
username_login_label = Label(root, text='Username: ', font=bold_20, background='#FAFAFA',
                             fg='#0D0C0C')
username_login_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA',
                             fg="#0D0C0C", bd=2, relief='solid')
password_login_label = Label(root, text='Password: ', font=bold_20, background='#FAFAFA',
                             fg='#0D0C0C')
password_login_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA',
                             fg="#0D0C0C", bd=2, relief='solid', show='•')
next_login_button = Button(root, text='Next', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                           relief='solid', width='18', cursor='target', command=login_to_homepage)

'''Change Personal Details'''

# Selection Page

selection_title = Label(root, text='Change Details', font=bold_48, fg='#0D0C0C', background='#FAFAFA')
selection_email = Button(root, text='Email', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                           relief='solid', width='18', cursor='target', command=selection_to_email)
selection_password = Button(root, text='Password', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                           relief='solid', width='18', cursor='target', command=selection_to_password)

# Email Change Page

email_title = Label(root, text='Change Email', font=bold_48, fg='#0D0C0C', background='#FAFAFA')
email_selection_label = Label(root, text='Email:', font=bold_20, fg='#0D0C0C', background='#FAFAFA')
email_selection_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA', fg="#0D0C0C",
                    bd=2, relief='solid')
next_email_button = Button(root, text='Next', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                           relief='solid', width='18', cursor='target', command=email_to_profile)

# Password Change Page

password_title = Label(root, text='Change Password', font=bold_48, fg='#0D0C0C', background='#FAFAFA')
password_selection_label = Label(root, text='Password:', font=bold_20, fg='#0D0C0C', background='#FAFAFA')
password_selection_entry = Entry(root, width=30, font=bold_20, selectbackground='#FAFAFA', fg="#0D0C0C",
                    bd=2, relief='solid')
next_password_button = Button(root, text='Next', font=bold_20, fg='#0D0C0C', background='#FAFAFA',
                           relief='solid', width='18', cursor='target', command=password_to_profile)

'''Homepage'''

homepage_label = Label(root, text='Homepage', font=bold_48, background='#FAFAFA',
                       foreground='#060606')

# Homepage Grid

play_button_homepage = Button(root, text='Play', font=bold_20, background='#0D0C0C',
                              foreground='#FAFAFA', relief='solid', cursor='target',
                              height=14, width=7, command=homepage_to_difficulty)
profile_button_homepage = Button(root, text='View Profile', font=bold_20, background='#FAFAFA',
                                 foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18,
                                 command=homepage_to_profile)
leaderboard_button_homepage = Button(root, text='Leaderboard', font=bold_20, background='#FAFAFA',
                                     foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18,
                                     command=homepage_to_leaderboard)
score_button_homepage = Button(root, text='', font=('IBM Plex Mono', 21, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid')

'''Score Page'''

score_title_label = Label(root, text='', font=bold_48,
                          background='#FAFAFA', foreground='#060606')
score_button_scorepage = Button(root, text='Home', font=bold_20, background='#FAFAFA',
                                foreground='#0D0C0C', relief='solid', width='18', cursor='target',
                                command=score_to_homepage)

'''Difficulty Page'''

difficulty_selection_label = Label(root, text='Difficulty', font=bold_48,
                                   background='#FAFAFA', foreground='#060606')

# Buttons

# Easy

easy_button = Button(root, text='Easy', font=bold_20, background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda: difficulty_to_game('Easy'))

# Medium

medium_button = Button(root, text='Medium', font=bold_20, background='#FAFAFA',
                       foreground='#0D0C0C', relief='solid', width='18', cursor='target',
                       command=lambda: difficulty_to_game('Medium'))

# Hard

hard_button = Button(root, text='Hard', font=bold_20, background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda: difficulty_to_game('Hard'))

'''Leaderboard'''

leaderboard_title_label = Label(root, text='Leaderboard', font=bold_48, background='#FAFAFA',
                                foreground='#060606')
username_label_button = Button(root, text='Username', font=bold_20, background='#0D0C0C',
                               foreground='#FAFAFA', relief='solid', width='18')
score_label_button = Button(root, text='Score', font=bold_20, background='#0D0C0C',
                            foreground='#FAFAFA', relief='solid', width='18')
time_label_button = Button(root, text='Time', font=bold_20, background='#0D0C0C',
                           foreground='#FAFAFA', relief='solid', width='18')
leaderboard_to_homepage_button = Button(root, text='Back', font=bold_20, background='#0D0C0C',
                                        foreground='#FAFAFA', relief='solid', width='18',
                                        command=leaderboard_to_homepage)

# Cells for Leaderboard

username_cell_0 = Button(root, text='username', font=bold_20, background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18')
username_cell_1 = Button(root, text='username', font=bold_20, background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18')
username_cell_2 = Button(root, text='username', font=bold_20, background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18')
username_cell_3 = Button(root, text='username', font=bold_20, background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18')
username_cell_4 = Button(root, text='username', font=bold_20, background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18')
username_cell_5 = Button(root, text='username', font=bold_20, background='#FAFAFA',
                         foreground='#0D0C0C', relief='solid', width='18')
score_cell_0 = Button(root, text='score', font=bold_20, background='#FAFAFA',
                      foreground='#0D0C0C', relief='solid', width='18')
score_cell_1 = Button(root, text='score', font=bold_20, background='#FAFAFA',
                      foreground='#0D0C0C', relief='solid', width='18')
score_cell_2 = Button(root, text='score', font=bold_20, background='#FAFAFA',
                      foreground='#0D0C0C', relief='solid', width='18')
score_cell_3 = Button(root, text='score', font=bold_20, background='#FAFAFA',
                      foreground='#0D0C0C', relief='solid', width='18')
score_cell_4 = Button(root, text='score', font=bold_20, background='#FAFAFA',
                      foreground='#0D0C0C', relief='solid', width='18')
score_cell_5 = Button(root, text='score', font=bold_20, background='#FAFAFA',
                      foreground='#0D0C0C', relief='solid', width='18')
time_cell_0 = Button(root, text='time', font=bold_20, background='#FAFAFA',
                     foreground='#0D0C0C', relief='solid', width='18')
time_cell_1 = Button(root, text='time', font=bold_20, background='#FAFAFA',
                     foreground='#0D0C0C', relief='solid', width='18')
time_cell_2 = Button(root, text='time', font=bold_20, background='#FAFAFA',
                     foreground='#0D0C0C', relief='solid', width='18')
time_cell_3 = Button(root, text='time', font=bold_20, background='#FAFAFA',
                     foreground='#0D0C0C', relief='solid', width='18')
time_cell_4 = Button(root, text='time', font=bold_20, background='#FAFAFA',
                     foreground='#0D0C0C', relief='solid', width='18')
time_cell_5 = Button(root, text='time', font=bold_20, background='#FAFAFA',
                     foreground='#0D0C0C', relief='solid', width='18')

'''Profile Page'''

username_title = Label(root, text='Welcome back!', font=bold_48,
                       background='#FAFAFA', foreground='#060606')
username_profile_label = Label(root, text='', font=bold_20,
                               background='#FAFAFA', foreground='#060606')
email_profile_label = Label(root, text='', font=bold_20,
                            background='#FAFAFA', foreground='#060606')
password_profile_label = Label(root, text='', font=bold_20,
                               background='#FAFAFA', foreground='#060606')
change_details_button = Button(root, text='Change Details', font=bold_20, background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', width='18', command=profile_to_selection)
profile_to_homepage_button = Button(root, text='Back', font=bold_20, background='#0D0C0C',
                                    foreground='#FAFAFA', relief='solid', width='18', command=profile_to_homepage)

# Loop the Game

root.mainloop()