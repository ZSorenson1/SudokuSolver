import pygame
import time
from sudokuSolver import *

pygame.init()

class gameBoard:

    def __init__(self, rows, cols, width, height, win):
        self.board = sudokuGenerator()
        self.rows = rows
        self.cols = cols
        self.cubes =[[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
        
        #is your input correct?
            if solveSudoku(self.model):
                return True
        
        #if not clear the box
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        #draws the game board
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                #lines to define inner boxes
                thick = 4
            else:
                thick = 1
            
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win,(0,0,0), (i*gap, 0), (i * gap, self.height), thick)

        #draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        #Reset previous selection
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        # pos is position
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            #return the exact coordinates of the cube you clicked
            return (int(y),int(x))
        else:
            #if you didn't click the board
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
    
    def solve(self):
        self.update_model()
        idx = [0, 0]
        find = findEmpty(self.model, idx)
        if not find:
            return True
        
        row = idx[0]
        col = idx[1]

        for i in range(1,10):
            if safeLocation(self.model, row, col, i):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].showChange(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].showChange(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
    

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap, gap), 3)
    
    def set(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.temp = val
    
    def showChange(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw Time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (20, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    #Draw board
    board.draw(win)

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    timeString = " " + str(minute) + ":" + str(sec)
    return timeString

def findEmptyCube(arr, idx):
    for row in range(9):
        for col in range(9):
            if arr[row][col].value == 0:
                idx[0] = row
                idx[1] = col
                return True
    return False

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = gameBoard(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    play_time = round(time.time() - start)
    
    while run:
        
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8 :
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    if board.selected != None:
                        i, j = board.selected
                        if board.cubes[i][j].temp != 0:
                            if board.place(board.cubes[i][j].temp):
                                print("Success")
                            else:
                                print("Wrong")
                                strikes += 1
                            key = None

                            if board.is_finished():
                                print("Game over")
                                run = False
                
                if event.key == pygame.K_SPACE:
                    board.solve()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
    
        if board.selected and key != None:
            board.sketch(key)
            key = None
        
        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()