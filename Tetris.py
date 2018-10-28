########
# Tetris
# Jifeng Yu
#######

from tkinter import *
import random

######
# Helper functions for math floating point
######

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

####################################
# TETRIS
####################################

#this sets how many rows, cols, and window size
def playTetris(rows=15, cols=10):
    cellSize=20
    margin=25
    windowWidth=2*margin+cols*cellSize
    windowHeight=2*margin+rows*cellSize
    #calls main run function to play game
    run(windowWidth, windowHeight)

def init(data):
    #needed for drawing board
    data.emptyColor='blue'
    data.margin, data.cellSize = 25, 20
    data.rows=roundHalfUp((data.height-2*data.margin)/data.cellSize)
    data.cols=roundHalfUp((data.width-2*data.margin)/data.cellSize)
    data.board=[([data.emptyColor]*data.cols) for row in range(data.rows)]
    #needed for making falling pieces
    iPiece = [[True,  True,  True,  True]]
    jPiece = [[True, False, False],[True,  True,  True]]
    lPiece = [[False, False,  True],[True,  True,  True]]
    oPiece = [[True, True],[True, True]]
    sPiece = [[False,  True,  True],[True,  True, False]]
    tPiece = [[False,  True, False],[True,  True,  True]]
    zPiece = [[True,  True, False],[False,  True,  True]]
    data.tetrisPieces=[iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieceColors=["red", "yellow", "magenta", "pink", "cyan", "green",
                            "orange"]
    #immediately creates new falling piece at he start of the game
    newFallingPiece(data)
    data.isGameOver=False
    data.score=0

def mousePressed(event, data):
    #only allows mouse clicks to create new piece if the game isn't over
    if data.isGameOver == False:
        newFallingPiece(data)

def keyPressed(event, data):
    #only registers key press if game isn't over
    if data.isGameOver == False:
        keyPressed=event.keysym
    else:
        keyPressed=""
    #up rotates the piece
    if keyPressed == "Up":
        rotateFallingPiece(data)
    elif keyPressed == "Down":
        moveFallingPiece(data, +1, 0)
    elif keyPressed == "Left":
        moveFallingPiece(data, 0, -1)
    elif keyPressed == "Right":
        moveFallingPiece(data, 0, +1)
    #r restarts the whole game and score
    elif keyPressed == 'r':
        init(data)

def timerFired(data):
    if data.isGameOver == False:
        #falling piece moves every time increment until it can't anymore
        if moveFallingPiece(data, +1, 0) == False:
            placeFallingPiece(data)
            newFallingPiece(data)
            #tests if the piece is illegal as soon as it appears
            if moveFallingPiece(data, 0, 0) != True:
                data.isGameOver=True

def placeFallingPiece(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            #changes the board to the falling piece's color at specified place
            if data.fallingPiece[i][j] == True:
                data.board[data.fallingPieceRow+i][data.fallingPieceCol+j]=\
                data.fallingPieceColor
    #need to check if there's a full row after every piece placement
    removeFullRows(data)
    
def newFallingPiece(data):
    #randomly selects a new falling piece
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece=data.tetrisPieces[randomIndex]
    data.fallingPieceColor=data.tetrisPieceColors[randomIndex]
    #piece starts at first row of board and is centered 
    data.fallingPieceRow=0
    data.fallingPieceCol=roundHalfUp(data.cols/2-len(data.fallingPiece[0])//2)

def fallingPieceIsLegal(data, drow, dcol):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True:
                #the piece can't go off the board
                if data.fallingPieceRow < 0:
                    return False
                elif data.fallingPieceRow+i >= len(data.board):
                    return False
                elif data.fallingPieceCol < 0:
                    return False
                elif data.fallingPieceCol+j >= len(data.board[0]):
                    return False
                #square the piece is going to can't be filled already
                else:
                    testRow=data.fallingPieceRow+i
                    testCol=data.fallingPieceCol+j
                    if data.board[testRow][testCol] != data.emptyColor:
                        return False
    #if all the conditions above are satisfied, it's a valid piece
    return True

def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow+=drow
    data.fallingPieceCol+=dcol
    #if the place you're moving to isn't legal, undo the drow dcol
    if not fallingPieceIsLegal(data, drow, dcol):
        data.fallingPieceRow-=drow
        data.fallingPieceCol-=dcol
        #returns false for not doing the move 
        return False
    #returns true for doing the move successfully
    return True

def rotateFallingPiece(data):
    #placeholders for piece before rotation just in case rotation isn't valid
    oldPiece=data.fallingPiece
    oldNumRows, oldNumCols = len(oldPiece), len(oldPiece[0])
    oldRow, oldCol = data.fallingPieceRow, data.fallingPieceCol
    #the new piece's location and dimensions are calculated with these formulas
    newNumRows, newNumCols = oldNumCols, oldNumRows
    newRow=oldRow+oldNumRows//2-newNumRows//2
    newCol=oldCol+oldNumCols//2-newNumCols//2
    #creates new list with rotated dimensions
    rotatedPiece=[([None]*newNumCols) for row in range(newNumRows)]
    for i in range(oldNumRows):
        for j in range(oldNumCols):
            #new col is old row, new row is this formula
            rotatedPiece[newNumRows-j-1][i]=oldPiece[i][j]
    data.fallingPiece=rotatedPiece
    data.fallingPieceRow, data.fallingPieceCol = newRow, newCol
    #if new rotated piece isn't legal, undo the rotation and restore old one
    if not (fallingPieceIsLegal(data, 0, 0)):
        data.fallingPiece=oldPiece
        data.fallingPieceRow, data.fallingPieceCol = oldRow, oldCol

def drawCell(canvas, data, i, j, color):
    #draws cell at specified row and col in the canvas with margin offset
    canvas.create_rectangle(data.margin+j*data.cellSize, data.margin+
        i*data.cellSize,data.margin+(j+1)*data.cellSize, 
        data.margin+(i+1)*data.cellSize, fill=color)

def drawBoard(canvas, data):
    #draws the board with specified rows and cols
    for i in range(data.rows):
        for j in range(data.cols):
            drawCell(canvas, data, i, j, data.board[i][j])

def drawFallingPiece(canvas, data):
    #draws the falling piece on top of the grid/board in specified color
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True:
                drawCell(canvas, data, data.fallingPieceRow+i, 
                data.fallingPieceCol+j,data.fallingPieceColor)

def removeFullRows(data):
    newBoard=[]
    rowsRemoved=0
    emptyRow=[data.emptyColor]*data.cols
    for row in range(data.rows):
        #the row is full is it doesn't contain the empty color at all
        if not (data.board[row].count(data.emptyColor) == 0):
            newBoard.extend([data.board[row]])
        else:
            rowsRemoved+=1
    #if we removed x rows, we need x empty rows at the very top of board
    if rowsRemoved != 0:
        for count in range(rowsRemoved):
            newBoard.insert(0, emptyRow)
    data.board=newBoard
    #score increments by square of rows removed
    data.score+=(rowsRemoved**2)

def gameOverMsg(canvas, data):
    fontStyle="Helvetica %d bold" % data.cellSize
    #banner for game over message
    canvas.create_rectangle(0, data.height/2-data.margin, data.width,
                data.height/2+data.margin, fill='black')
    #actual game over message itself
    canvas.create_text(data.width/2, data.height/2, text="Game Over!", 
            fill='white', font=fontStyle)

def displayScore(canvas, data):
    #this prints the score up at the very top of the canvas in margin
    fontStyle="Helvetica %d bold" % (data.margin//2)
    scoreText="Score: "+str(data.score)
    canvas.create_text(data.width/2, data.margin//2, text=scoreText, 
            font=fontStyle)

def redrawAll(canvas, data):
    #basic background with orange margin showing
    canvas.create_rectangle(0,0, data.width, data.height, fill='orange')
    #draws rest of the board and score
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    displayScore(canvas, data)
    #checks if game is over every redraw to see if message needs to be printed
    if data.isGameOver == True:
        gameOverMsg(canvas, data)

####################################
# run function
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 300 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
    
playTetris()
