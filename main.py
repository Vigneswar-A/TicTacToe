# imports - os, sys, tkinter-*,font, functools-partial, random-shuffle,randint,random
import os
import sys
from tkinter import *
from tkinter import font
from functools import partial
from random import shuffle, randint, random

# get path


def path(rp):
    try:
        bp = sys._MEIPASS
    except:
        bp = os.path.abspath('.')
    return os.path.join(bp, rp)

# configuation


def create_window():
    root = Tk()
    root.title('TicTacToe')
    root.resizable(0, 0)
    root.minsize(500, 600)
    root.maxsize(500, 600)
    return root


root = create_window()
# root.iconbitmap(path('icon.ico'))

# constants
BLUE = '#6785b5'
RED = '#673444'
DARKRED = '#540d0f'
GREEN = '#399e18'
FONT = font.Font(root, size=40)
BUTTONFONT = font.Font(root, size=25)
UIFONT = font.Font(root, size=20)
YELLOW = '#c2a62d'
LEVEL = 10

# configurations
CONFIGURATION = {
    'height': 1,
    'width': 3,
    'borderwidth': 20,
    'background': BLUE,
    'activebackground': BLUE,
    'font': FONT,
    'fg': DARKRED
}

# game board


class Board:
    PLAYERS = ['X', 'O']

    def __init__(self, bot=True):
        shuffle(Board.PLAYERS)
        # make board
        self.board = [None] * 9
        self.bot = bot
        for i in range(9):
            self.board[i] = Button(root, CONFIGURATION,
                                   command=partial(self.move, i))
            self.board[i].grid(row=i//3, column=i % 3)

        # configure game settings
        self.gameover = False
        self.moves = 0
        self.single = bot

        # multiplayer
        self.player = 'X'
        self.next = {'X': 'O', 'O': 'X'}

        # singleplayer
        if self.single:
            self.player, self.bot = Board.PLAYERS
            self.level = LEVEL
            if self.bot == 'X':
                self.board[self.bot_move()]['text'] = 'X'
                self.moves += 1

        self.uis = []

    def move(self, i):
        # if game over, no more moves
        if self.gameover or self.board[i]['text'] != '':
            return None

        # place a move
        self.moves += 1
        self.board[i]['text'] = self.player
        self.board[i]['activebackground'] = RED

        # if any one won then game over (first check)
        if self.condition() is not None:
            self.gameover = True
            self.reset()
            return

        # if 8 moves are done with no winner then its game over (first check)
        elif self.moves == 9:
            self.gameover = True
            for box in self.board:
                box['background'] = YELLOW
            self.reset()
            return

        # bot move if single player
        if self.single:
            botmove = self.bot_move()
            self.board[botmove]['text'] = self.bot
            self.board[botmove]['activebackground'] = RED
            self.moves += 1
            # if any one won then game over (second check)
            if self.condition() is not None:
                self.gameover = True
                self.reset()
                return

            # if 8 moves are done with no winner then its game over (second check)
            elif self.moves == 9:
                self.gameover = True
                for box in self.board:
                    box['background'] = YELLOW
                self.reset()
                return

        # other player move if multiplayer
        else:
            self.player = self.next[self.player]

    def condition(self):
        # horizontal and vertical check
        for i in range(3):
            if self.board[i*3]['text'] and self.board[i*3]['text'] == self.board[i*3+1]['text'] == self.board[i*3+2]['text']:
                self.board[i*3]['background'] = self.board[i*3 +
                                                           1]['background'] = self.board[i*3+2]['background'] = GREEN
                return self.player

            if self.board[i]['text'] and self.board[i]['text'] == self.board[i+1*3]['text'] == self.board[i+2*3]['text']:
                self.board[i]['background'] = self.board[i+1 *
                                                         3]['background'] = self.board[i+2*3]['background'] = GREEN
                return self.player

        # diagonal check
        if self.board[0]['text'] and self.board[0]['text'] == self.board[4]['text'] == self.board[8]['text']:
            self.board[0]['background'] = self.board[4]['background'] = self.board[8]['background'] = GREEN
            return self.player

        # anti-diagonal check
        if self.board[2]['text'] and self.board[2]['text'] == self.board[4]['text'] == self.board[6]['text']:
            self.board[2]['background'] = self.board[4]['background'] = self.board[6]['background'] = GREEN
            return self.player

        return None

    def bot_move(self):
        # prepare a list model of board for easier processing
        board = []
        for i in range(9):
            board.append(self.board[i]['text'])

        def evaluate(board):  # gets score for given board
            for i in range(3):
                if board[i*3] and board[i*3] == board[i*3+1] == board[i*3+2]:
                    return 1 if board[i*3] == self.bot else -1

                if board[i] and board[i] == board[i+1*3] == board[i+2*3]:
                    return 1 if board[i] == self.bot else -1

            if board[4] and ((board[0] == board[4] == board[8]) or (board[2] and board[2] == board[4] == board[6])):
                return 1 if board[4] == self.bot else -1

            return 0

        def minimax(board, ismax, depth):  # minimax algorithm to maximise winning condition
            score = evaluate(board)
            if score:
                return score, depth
            elif all(board):
                return 0, depth

            if ismax:
                best = -float('inf')
                mindepth = float('inf')
                for i in range(9):
                    if not board[i]:
                        board[i] = self.bot
                        score, depth = minimax(board, not ismax, mindepth+1)
                        if score > best:
                            best = score
                            mindepth = depth
                        elif score == best and mindepth < depth:
                            mindepth = depth
                        board[i] = ''
                return best, mindepth

            best = float('inf')
            mindepth = float('inf')
            for i in range(9):
                if not board[i]:
                    board[i] = self.player
                    score, depth = minimax(board, not ismax, mindepth+1)
                    if score < best:
                        best = score
                        mindepth = depth
                    elif score == best and mindepth < depth:
                        mindepth = depth
                    board[i] = ''
            return best, depth

        # initialising variables
        bestmove = None
        worstmove = None
        worstscore = float('inf')
        bestscore = -float('inf')
        mindepth = float('inf')

        # get worst and best moves
        for i in range(9):
            if not board[i]:
                board[i] = self.bot
                score, depth = minimax(board, False, 0)

                if score > bestscore:
                    bestscore = score
                    bestmove = i
                elif score == bestscore and depth < mindepth:
                    bestscore = score
                    mindepth = depth
                    bestmove = i
                elif score == bestscore and depth == mindepth and randint(0, 1):
                    bestmove = i

                if score < worstscore:
                    worstscore = score
                    worstmove = i
                elif score == worstscore and depth > mindepth:
                    worstscore = score
                    mindepth = depth
                    worstmove = i
                elif score == worstscore and depth == mindepth and randint(0, 1):
                    worstmove = i

                board[i] = ''

        if random() > self.level/10:  # randomly choose to let win or lose
            return worstmove
        return bestmove

    def reset(self):
        reset = Button(root, text='Reset', font=UIFONT, background=RED, command=lambda: (
            self.destroy(), self.__init__(self.single)), activebackground=RED)
        reset.grid(row=3, column=2)
        menu = Button(root, text='Menu', font=UIFONT, background=GREEN, command=lambda: (
            self.destroy(), create_ui()), activebackground=GREEN)
        menu.grid(row=3, column=0)
        self.uis.append(reset)
        self.uis.append(menu)

    def destroy(self):
        for box in self.board:
            box.destroy()
        for ui in self.uis+UI:
            ui.destroy()


UI = []


def play():
    global LEVEL
    try:
        LEVEL = level.get()
    except:
        pass
    for ui in UI:
        ui.destroy()
    UI.clear()
    root['padx'] = root['pady'] = 50
    Board(mode.get() == 'Single Player')


# game loop
mode = StringVar()
mode.set('Single Player')


def create_level():
    if mode.get() == ' Multi Player ':
        return
    global level, levellabel
    levellabel = Label(text='Level', font=UIFONT, background=GREEN)
    levellabel.grid(row=3, column=0, columnspan=6)
    level = Scale(root, from_=1, to=10, orient=HORIZONTAL, background=GREEN, troughcolor=RED, font=UIFONT,
                  sliderlength=25, length=200, relief=RAISED, sliderrelief=FLAT, activebackground=BLUE)
    level.grid(row=4, column=0, columnspan=6)
    level.set(LEVEL)
    UI.append(level)
    UI.append(levellabel)


def destroy_level():
    global level, levellabel
    UI.remove(level)
    UI.remove(levellabel)
    level.destroy()
    levellabel.destroy()


def modechange():
    if mode.get() == 'Single Player':
        mode.set(' Multi Player ')
        destroy_level()
    else:
        mode.set('Single Player')
        create_level()


def create_ui():
    root.configure(padx=100, pady=100)
    title = Label(text='Tic Tac Toe', font=FONT, fg=RED)
    title.grid(row=0, column=0, columnspan=6)
    playbutton = Button(text='Play', font=UIFONT, background=GREEN,
                        height=1, width=7, command=play, activebackground=GREEN)
    playbutton.grid(row=1, columnspan=6)
    gamemode = Label(textvariable=mode, font=UIFONT,
                     background=GREEN, width=10)
    gamemode.grid(row=2, column=1)
    leftarrow = Button(width=3, text='<', font=BUTTONFONT,
                       command=modechange, background=BLUE, activebackground=BLUE)
    rightarrow = Button(width=3, text='>', font=BUTTONFONT,
                        command=modechange, background=BLUE, activebackground=BLUE)
    leftarrow.grid(row=2, column=0)
    rightarrow.grid(row=2, column=3)
    create_level()

    UI.append(title)
    UI.append(playbutton)
    UI.append(leftarrow)
    UI.append(rightarrow)
    UI.append(gamemode)


create_ui()
root.mainloop()
