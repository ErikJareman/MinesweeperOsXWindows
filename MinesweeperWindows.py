from tkinter import *
from random import *
from tkinter.messagebox import *
import math
import sys
import os

master = Tk()
master.title('Minesweeper')
master.config(background='Grey85')

row_tot = IntVar()
col_tot = IntVar()
bomb = IntVar()
tiles_count = 0
bomb_positions = []
button_list = []
col_list = []
flag_list = []
large_font = ('Verdana', 14, 'bold')
small_font = ('Verdana', 12, 'bold')
entry_font = ('Verdana', 12)
start_font = ('Verdana', 9, 'bold')

def restart():
    msg = 'Are you sure you want to restart?'
    answer = askquestion('Restart', msg)
    if answer == 'yes':
        reveal_bombs()
        reset()
    else:
        return

def quit():
    msg = 'Are you sure you want to quit?'
    answer = askquestion('Quit', msg)
    if answer == 'yes':
        exit()
    else:
        return

def reset():
    row_tot = IntVar(0)
    col_tot = IntVar(0)
    bomb = IntVar(0)
    tiles_count = 0
    bomb_positions.clear()
    button_list.clear()
    col_list.clear()
    flag_list.clear()
    game('Restart')

def reveal_bombs():
    for i in bomb_positions:
        row = i
        while row > row_total:
            row -= row_total
        row -= 1
        col = col_list[i]

        label = Label(master, width=4)
        photo = PhotoImage(file='bomb_real.gif')
        label.config(image=photo, width=25, height=20)
        label.image = photo
        label.grid(row=int(row), column=int(col))

def bomb_trigger(event):
    reveal_bombs()
    msg = 'You lost! Play again?'
    answer = askquestion('Play again', msg)
    if answer == 'yes':
        reset()
    else:
        exit()

def victory():
    reveal_bombs()
    msg = 'You won! Play again?'
    answer = askquestion('Play again', msg)
    if answer == 'yes':
        reset()
    else:
        quit()

def place_flag(button_number):
    col = col_list[button_number]
    row = button_number
    while row > row_total:
        row -= row_total
    row -= 1
    if button_number not in flag_list:      #Create flag button
        flag_list.append(button_number)
        btn = Button(master, width=3)
        btn.bind('<ButtonRelease-2>', lambda event: place_flag(button_number))
        photo = PhotoImage(file='flag_real.gif')
        btn.config(image=photo, width=25, height=20)
        btn.image = photo
        btn.grid(row=row, column=col)

    else:
        flag_list.remove(button_number)
        if button_number in bomb_positions: #Re-create bomb button
            btn = Button(master, width=3)
            btn.bind('<ButtonRelease-1>', bomb_trigger)
            btn.bind('<ButtonRelease-2>', lambda event: place_flag(button_number))
            btn.grid(row=row, column=col)
        else:                               #Re-create safe button
            btn = Button(master, width=3)
            btn.bind('<ButtonRelease-1>', lambda event: check_neigbors(button_number))
            btn.bind('<ButtonRelease-2>', lambda event: place_flag(button_number))
            btn.grid(row=row, column=col)

def check_neigbors(button_number):
    if button_number not in button_list:
        return
    button_list.remove(button_number)
    global tiles_count
    tiles_count -= 1
    dangerzone = 0
    col = col_list[button_number]
    row = button_number
    while row > row_total:
        row -= row_total
    row -= 1

    if col_list[button_number-1] == col_list[button_number]:    #Check # bombs nearby
        if button_number-1 in bomb_positions:
            dangerzone += 1
        if button_number-row_total-1 in bomb_positions:
            dangerzone += 1
        if button_number+row_total-1 in bomb_positions:
            dangerzone += 1

    if col_list[button_number+1] == col_list[button_number]:
        if button_number+1 in bomb_positions:
            dangerzone += 1
        if button_number-row_total+1 in bomb_positions:
            dangerzone += 1
        if button_number+row_total+1 in bomb_positions:
            dangerzone += 1

    if button_number -row_total in bomb_positions:
        dangerzone += 1
    if button_number +row_total in bomb_positions:
        dangerzone += 1

#If # of bombs nearby:
    if dangerzone == 0:
        a = Label(master, width=0, relief=SUNKEN, text='0', fg='grey85', bg='Grey85', font='small_font')
        a.grid(row=int(row), column=int(col), sticky=W+E)
        check_neigbors(button_number-row_total)
        check_neigbors(button_number+row_total)

        if col_list[button_number-1] == col_list[button_number]:
            check_neigbors(button_number-1)         #Call function again if no bombs nearby
            check_neigbors(button_number-row_total-1)
            check_neigbors(button_number+row_total-1)

        if col_list[button_number+1] == col_list[button_number]:
            check_neigbors(button_number+1)
            check_neigbors(button_number-row_total+1)
            check_neigbors(button_number+row_total+1)

    if 3 > dangerzone > 0:
        a = Label(master, width=0, relief=SUNKEN, text=dangerzone, fg='Blue', bg='grey85', font=small_font)
        a.grid(row=int(row), column=int(col), sticky=W+E)

    if 5 > dangerzone > 2:
        a = Label(master, width=0, relief=SUNKEN, text=dangerzone, fg='darkorchid', bg='grey85', font=small_font)
        a.grid(row=int(row), column=int(col), sticky=W+E)

    if 4 < dangerzone:
        a = Label(master, relief=SUNKEN, text=dangerzone, fg='firebrick', bg='grey85', font=small_font)
        a.grid(row=int(row), column=int(col), sticky=W+E)

    tiles_remaining = Label(master, text='Tiles Left: ' + str(tiles_count), font=small_font, bg='Grey85', width=14)
    tiles_remaining.grid(row=3)
    if tiles_count == 0:
        victory()

def game(string):
    gridsize = Label(master, text="Height:", font=small_font) #"Questions"
    gridsize.grid(row=5, sticky=W+E)
    gridsize = Label(master, text="Width:", font=small_font, justify='center')
    gridsize.grid(row=7, sticky=W+E)
    gridsize = Label(master, text="Bomb percentage:", font=small_font)
    gridsize.grid(row=9, sticky=W+E)

    entry = Entry(master, textvariable=col_tot, justify='center', font=entry_font)              #input columns total
    entry.delete(0, END)
    entry.insert(0, '>4')
    entry.grid(row=8, column=0, sticky=W+E, ipady=2)

    entry = Entry(master, textvariable=row_tot, justify='center', font=entry_font)             #input rows total
    entry.delete(0, END)
    entry.insert(0, '>4')
    entry.grid(row=6, column=0, sticky=W+E, ipady=2)

    entry = Entry(master, textvariable=bomb, justify='center', font=entry_font)                 # input bomb rate
    entry.delete(0, END)
    entry.insert(0, '0-100')
    entry.grid(row=10, column=0, sticky=W+E, ipady=2)

    btn = Button(master, text=string, width=30, font=start_font, fg='blue', command=game_board)
    btn.grid(row=11, column=0)

    for children in master.winfo_children():
        try:
            children.disable()
        except:
            None

def game_board():
    for child in master.winfo_children():
        child.destroy()

    global col_total
    global row_total
    global bomb_rate
    try:
        col_total = (col_tot.get())
        row_total = (row_tot.get())
        bomb_rate = (bomb.get())
    except:
        game('Start Game')
        return
    for widget in master.winfo_children():
        widget.destroy()

    if row_total > 4 and col_total > 4 and bomb_rate in range(0, 101):
        row = 0
        col = 1
        col_list.append(0)
        presentation = Label(master, text='MINESWEEPER', width=22, font=small_font, fg='Red', bg='Grey85')
        presentation.grid(row=2)

        for i in range(1, (row_total * col_total+1)):
            random = randint(1, 100)
            if random > bomb_rate:
                btn = Button(master, width=3)                                #Create "safe" button
                btn.bind('<ButtonRelease-1>', lambda event, i=i: check_neigbors(i))
                btn.bind('<ButtonRelease-2>', lambda event, i=i: place_flag(i))
                btn.grid(row=row, column=col)
                button_list.append(i)
                col_list.append(col)
            if random <= bomb_rate:
                btn = Button(master, width=3)                                #Create "bomb" button
                btn.bind('<ButtonRelease-1>', bomb_trigger)
                btn.bind('<ButtonRelease-2>', lambda event, i=i: place_flag(i))
                btn.grid(row=row, column=col)
                bomb_positions.append(i)
                col_list.append(col)
                button_list.append(i)
            row += 1
            if row == row_total:
                row = 0
                col += 1

        for i in range (0,row_total):
            col_list.append(0)

        global tiles_count
        tiles_count = (row_total * col_total)-len(bomb_positions)
        global tiles_remaining
        tiles_remaining = Label(master, text='Tiles Left: ' + str(tiles_count), font=small_font, bg='Grey85', width=14)
        tiles_remaining.grid(row=3)
        reset_button = Button(master, text='Restart', command=restart, bg='Grey85')
        reset_button.grid(row=row_total+1, column=1, columnspan=int(col_total/2), sticky=W+E)
        quit_button = Button(master, text='Quit', command=quit, bg='Grey85')
        quit_button.grid(row=row_total+1, column=int(1+math.floor(col_total/2)), columnspan=int(col_total/2)+1, sticky=W+E)

    else:
        game('Start Game')

game('Start Game')
mainloop()