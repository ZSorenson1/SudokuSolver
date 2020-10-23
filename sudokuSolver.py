import random

def prettyPrint(arr):
    print('\n')
    for i in range(9): 
        for j in range(9): 
            print(arr[i][j]) 
        print ("\n") 
#finds first empty index
#idx is our current index passed from our solve function so it may be edited
#return false if all values != 0
def findEmpty(arr, idx):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                idx[0] = row
                idx[1] = col
                return True
    return False


#check for number in row
def usedInRow(arr, row, num):
    for i in range(9):
        if arr[row][i] == num:
            return True
    return False

#check for number in column
def usedInCol(arr, col, num):
    for i in range(9):
        if arr[i][col] == num:
            return True
    return False

#row and column are subtracted by modulus 3 to ensure we are at the top left of the box we are checking
def usedInBox(arr, row, col, num):
    row -= row % 3
    col -= col % 3
    for i in range(3):
        for j in range(3):
            if(arr[row + i][col + j] == num):
                return True
    return False

#consolidated checker for our solving algo
def safeLocation(arr, row, col, num):
    return not usedInRow(arr, row, num) and not usedInCol(arr, col, num) and not usedInBox(arr, row, col, num)

def solveSudoku(arr, creator=False):
    
    #idx holds our current row and column
    idx = [0,0]

    #Here we check if the sudoku is already solved or get our first empty value
    if not findEmpty(arr, idx):
        return True

    row = idx[0]
    col = idx[1]

    for num in range(1, 10):
        if safeLocation(arr, row, col, num):
            arr[row][col] = num
            
            if solveSudoku(arr):
                    return True

            
            #failure to solve, try again with next num
            #this is where we backtrack once one of our recursive solveSudoku functions returns false
            arr[row][col] = 0

    #out of options no possible answers
    return False



def sudokuGenerator():
    newSudoku = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    rand = random.randint(1, 9)
    for i in range(9):
        for j in range(9):
            val = rand
            if safeLocation(newSudoku, i, j, val):
                newSudoku[i][j] = val
            
                while not solveSudoku(newSudoku):
                    val = rand
                    if safeLocation(newSudoku, i, j, val):
                        newSudoku[i][j] = val
    count = 0
    #the fewest values a sudoku can have and still have a single unique answer is 17. 81 - 17 leaves 64 blank spaces
    while count != 64:
        x = random.randint(0,8)
        y = random.randint(0,8)
        newSudoku[x][y] = 0
        count += 1
        


    return newSudoku