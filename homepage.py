from tkinter import *

root = Tk()
root.geometry('1280x720')
root.title('Sudoku')
root.resizable(False, False)
root['bg'] = '#FAFAFA'

# Homepage label
homepage_label = Label(root, text='Homiepage', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA',
                       foreground='#060606')
homepage_label.place(x=490, y=30)

# Grid
play_button_homepage = Button(root, text='Play', font=('IBM Plex Mono', 20, 'bold'), background='#0D0C0C',
                              foreground='#FAFAFA', relief='solid', cursor='target', height=14, width=7)
play_button_homepage.place(x=420, y=155)

profile_button_homepage = Button(root, text='View Profile', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                                 foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18)
profile_button_homepage.place(x=540, y=155)

leaderboard_button_homepage = Button(root, text='Leaderboard', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA',
                                     foreground='#0D0C0C', relief='solid', cursor='target', height=3, width=18)
leaderboard_button_homepage.place(x=540, y=280)

score_button_homepage = Button(root, text='2354p', font=('IBM Plex Mono', 32, 'bold'), background='#FAFAFA',
                               foreground='#0D0C0C', relief='solid', height=4, width=11)
score_button_homepage.place(x=540, y=409)

root.mainloop()