# importing necessary libraries 
import tkinter as tk 
from PIL import ImageTk, Image
from itertools import product # this tool computes the cartesian product of input iterables
import re # RegEx module to check if a string contains the specified search pattern 

HEIGHT = 525
WIDTH = 600

text=''
instructions_text = 'A number lock has a 3 digit key. Hints of these\nthree digits are provided below. Can you crack the code?'
count = 0

"""
The following functions are used as a callback in the 'GUESS' button widget.
"""
# obtain the user's guess and verify it 
def get_guess(entry):
    global count
    count = count + 1 

    print("Your guess is:", entry) # this will allow the user to keep track of their guesses within the terminal

    # check if the string contains any letters from the alphabet 
    alpha_check = re.search('[a-zA-Z]', entry) 
    #check if the string contains any common symbols
    symbol_check = re.findall('[+!@`~#$%^&*()-]', entry)

    if entry == "" or alpha_check or symbol_check:
        lower_label.configure(text='Error: your input is invalid.')
    else: 
        int_entry = int(entry) # converts the specified value into an integer number 
        check_guess(entry)

# verify if the user's guess is correct
def check_guess(entry):
    if (entry == '042'):
        # if the user's guess is correct, configure the message outputted in lower_label to congratulate
        lower_label.configure(text='Congratulations! You guessed correctly.\nThe number was 042 and it only took you ' + str(count) + ' tries!')
    else: 
        # if the user's guess is not correct, configure the message outputted in lower_label to prompt the use to try again
        lower_label.configure(text='Sorry! Your guess was incorrect.\nPerhaps read the hints once more and try again.')

"""
The following functions are the hints given using Boolean logic in order to solve the 3 digit code.
If the user decides to 'GIVE UP' then the functions below will be called.
For this program, the numbers can be modified so long that the hints remain the same. 
"""
# 682 - one digit is correct and in the correct place
def first_hint(combination, condition):
    common_values = [digit for digit in combination if digit in condition]
    return(len(common_values) == 1) and (combination.index(common_values[0]) == condition.index(common_values[0]))

# 614 - one digit is correct but in the wrong place
def second_hint(combination, condition):
    common_values = [digit for digit in combination if digit in condition]
    return(len(common_values) == 1) and (combination.index(common_values[0]) != condition.index(common_values[0]))

# 206 - two digits are correct but both are in the wrong place
def third_hint(combination, condition):
    common_values = [digit for digit in combination if digit in condition]
    if len(common_values) != 2:
        return False
    for digit in common_values:
        if combination.index(digit) == condition.index(digit):
            return False
    return True

# 738 - all digits are wrong
def fourth_hint(combination, condition):
    common_values = [digit for digit in combination if digit in condition]
    return len(common_values) == 0

# 380 - one digit is correct but in the wrong place
def fifth_hint(combination, condition):
    common_values = [digit for digit in combination if digit in condition]
    return(len(common_values) == 1) and (combination.index(common_values[0]) != condition.index(common_values[0]))

def unlock():
    for combination in product(range(10), repeat=3):
        if (
            first_hint(combination, (6, 8, 2))
            and second_hint(combination, (6, 1, 4))
            and third_hint(combination, (2, 0, 6))
            and fourth_hint(combination, (7, 3, 8))
            and fifth_hint(combination, (3, 8, 0))
        ):
            result = "".join(map(str, combination)) # join() takes a string separator e.g. nothing and joins the elements
            lower_label.configure(text='CodeBreaker.py computed ' + result + ' as the result of the riddle.')
            return result
    return "No solution found."

"""
Creating a GUI application using Python Tkinter for the CodeBreaker
The purpose of the GUI application is to display the hints to the riddle in a user friendly manner
Significant features include an entry widget for user input and two buttons to run the program 
"""
# root window to place the contents
root = tk.Tk()
root.title('Code Breaker')

# setting the canvas
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# setting the background image of the window
background_image = ImageTk.PhotoImage(Image.open("blue-matrix.png"))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#34e0d2', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# widget to display the title 
title = tk.Label(frame, text="Can You Crack The Code?", font=('Modern', 25, 'bold'), bg='white', anchor='center', relief='sunken')
title.place(relwidth=1, relheight=1)

# frame to display the instructions and hints
center_frame = tk.Frame(root, bg='#2932cf', bd=10)
center_frame.place(relx=0.5, rely=0.225, relwidth=0.75, relheight=0.55, anchor='n')

# label widget to display brief instructions of what the user should be doing to run the program smoothly
instructions = tk.Label(center_frame, text=instructions_text, font=('Modern', 12, 'bold'), bg='white', anchor='center', relief='sunken')
instructions.grid(row=0, column=0, pady=5, padx=10, ipady=10, ipadx=25)

# label widget to display hints to help the user determine what the 3 digit key is 
center_label = tk.Label(center_frame, text="682 - one digit is correct and in the correct place\n\n614 - one digit is correct but in the wrong place\n\n206 - two digits are correct but both are in the wrong place\n\n738 - all digits are wrong\n\n380 - one digit is correct but in the wrong place", bd=1, font=('Courier', 10), bg='white', anchor='center', relief='sunken')
center_label.grid(row=1, column=0, pady=5, padx=10, ipady=10, ipadx=25)

# entry widget where the user enters in their guess 
entry = tk.Entry(center_frame, font=10)
entry.grid(row=2, column=0, pady=5, padx=5)

# frame to display the buttons
button_frame = tk.Frame(root, bg='#2932cf', bd=10)
button_frame.place(relx=0.5, rely=0.68, relwidth=0.75, relheight=0.10, anchor='n')

# enter button to obtain the user's guess
button = tk.Button(button_frame, text="ENTER", font=('Modern', 12, 'bold'), fg='#000000', width=10, command=lambda: get_guess(entry.get()))
button.grid(row=1, column=0, pady=5, padx=40, ipadx=20) 

# enter button to let the program calculate the answer
button2 = tk.Button(button_frame, text="GIVE UP", font=('Modern', 12, 'bold'), fg='#000000', width=10, command=lambda: unlock())
button2.grid(row=1, column=1, pady=5, padx=40, ipadx=20) 

# frame widget to display messages to the user depending on the input
lower_frame = tk.Frame(root, bg='#FFFFFF', bd=5)
lower_frame.place(relx=0.5, rely=0.80, relwidth=0.75, relheight=0.10, anchor='n')

lower_label = tk.Label(lower_frame, text=text, font=('courier', 12), bg='#000000', fg='white', anchor='center', relief='sunken')
lower_label.place(relwidth=1, relheight=1)

# to run the application
root.mainloop()