from tkinter import *

root = Tk()
root.geometry('1280x720')
root.title('Sudoku')
root.resizable(False, False)
root['bg'] = '#FAFAFA'

# Difficulty Label

difficulty_selection_label = Label(root, text='Difficulty', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA', foreground='#060606')
difficulty_selection_label.place(x=390, y=40, width=500)

# Functions

# Score Counter

def score_calc(difficulty_selector = 'easy'):
    global difficulty_points

    if difficulty_selector == 'easy':
        difficulty_points = 2000

    return difficulty_points

'''def easy_button_difficulty():
    global difficulty_choice
    difficulty_choice = 'easy'
    return difficulty_choice

    # Transition code added here


def medium_button_difficulty():
    difficulty_choice = 'medium'
    return difficulty_choice

    # Transition code added here


def hard_button_difficulty():
    difficulty_choice = 'hard'
    return difficulty_choice

    # Transition code added here
'''
# Buttons
# Easy
easy_button = Button(root, text='Easy', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=score_calc)
easy_button.place(x = 480, y = 250)

# Medium

medium_button = Button(root, text='Medium', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                       relief='solid', width='18', cursor='target', command=lambda: score_calc('medium'))
medium_button.place(x = 480, y = 330)

# Hard

hard_button = Button(root, text='Hard', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C',
                     relief='solid', width='18', cursor='target', command=lambda: score_calc('hard'))
hard_button.place(x = 480, y = 410)

print(difficulty_points)

root.mainloop()