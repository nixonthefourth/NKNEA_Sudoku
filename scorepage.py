from tkinter import *

root = Tk()
root.geometry('1280x720')
root.title('Sudoku')
root.resizable(False, False)
root['bg'] = '#FAFAFA'

# Difficulty Label

score_title_label = Label(root, text='Your score is:  2230P', font=('IBM Plex Mono', 48, 'bold'), background='#FAFAFA', foreground='#060606')
score_title_label.place(x=255, y=70)

# Buttons
# Home
homepage_button = Button(root, text='Home', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C', relief='solid', width='18', cursor='target')
homepage_button.place(x = 480, y = 250)

# Rematch

rematch_button = Button(root, text='Rematch', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C', relief='solid', width='18', cursor='target')
rematch_button.place(x = 480, y = 330)

# exit

exit_button = Button(root, text='Exit', font=('IBM Plex Mono', 20, 'bold'), background='#FAFAFA', foreground='#0D0C0C', relief='solid', width='18', cursor='target', command=root.destroy)
exit_button.place(x = 480, y = 410)

root.mainloop()