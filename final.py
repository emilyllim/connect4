from tkinter import*
import random

class Connect4:
    # Constructor
    def __init__(self, width, height, aiPlayer, window):
        # Game begins with player X
        self.player = 'X' # Player X is Red, Player O is Black
        self.aiPlayer = aiPlayer
        self.width = width # Width of board
        self.height = height # Height of board
        self.data = [] # Board data is a matrix
        self.gameOn = True

        # GUI
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.boardWidth = width * 100
        self.boardHeight = height * 110
        self.size = width
        self.messageSize = 25
        self.diameter = self.boardWidth/self.size
        self.col = 0
        self.row = 0

        # Creates quit button
        self.quitButton = Button(self.frame, text='Quit', command=self.quitGame)
        self.quitButton.pack(side=RIGHT)

        # Creates new game button
        self.newGameButton = Button(self.frame, text='New Game', command=self.newGame)
        self.newGameButton.pack(side=LEFT)

        # Draws game onto a canvas on the window, takes mouse input
        self.draw = Canvas(window, height=self.boardHeight, width=self.boardWidth, bg='yellow')
        self.draw.bind('<Button-1>', self.playGame)
        self.draw.pack()

        # Matrix that contains the colors of the circles
        self.circles = []

        y = 0 # x and y are coordinates in the canvas
        # Adds a white circles to the canvas and creates an empty board
        for row in range(self.height):
            circleRow = []
            dataRow = []
            x = 0
            for col in range(self.width):
                circleRow += [self.draw.create_oval(x,y,x+self.diameter,y+self.diameter,fill='white')]
                dataRow += [' ']
                x += self.diameter
            self.circles+= [circleRow]
            self.data += [dataRow]
            y+= self.diameter

        # Displays starting message at the beginning of the game
        self.message = self.draw.create_text(self.messageSize, self.boardHeight-self.messageSize,
            text='Starting game! Select a column.',
            anchor='w', font='Courier 24')

    # Returns string representation of board
    def __repr__(self):
        s = ''
        for row in range(self.height):
            s += '|'
            for col in range(self.width):
                s += self.data[row][col] + '|'
            s += "\n"

        s += '--'*self.width + '-\n'

        for col in range(self.width):
            s += ' ' + str(col % 10)
        s += '\n'

        return s

    # Plays game with AI player
    def playGame(self, event): # Mouse input event determines what move player X makes next
        # If it is X's turn and game is not over
        if self.player == 'X' and self.gameOn == True:
            self.draw.itemconfig(self.message, text='Select a column.')
            # Column on the board that the mouse chose
            self.col = int(event.x/self.diameter)
            if self.allowsMove(self.col) == True:
                # Adds and displays move in column that was chosen, if it is allowed
                self.addMove(self.col, 'X')
                self.draw.itemconfig(self.circles[self.row][self.col], fill='red')
                # If X gets a win, game ends. Winning message is printed
                if self.winsFor(self.player) == True:
                    self.gameOn = False
                    self.draw.itemconfig(self.message, text='Player Red has won the game!')
                else:
                    # Otherwise, player switches to O
                    self.player = self.aiPlayer.switchPlayer(self.player)
            else:
                # Prompts user that move is not allowed
                self.draw.itemconfig(self.message, text='Invalid move. Try again.')

        # If it is O's turn
        if self.player == 'O' and self.gameOn == True:
            # Gets O's move and adds it
            oMove = self.aiPlayer.nextMove(self)
            self.addMove(oMove, 'O')
            self.draw.itemconfig(self.circles[self.row][oMove], fill='black')
            # If O gets a win, game ends. Winning message is printed
            if self.winsFor(self.player) == True:
                self.gameOn = False
                self.draw.itemconfig(self.message, text='Player Black has won the game!')
            else:
                # Otherwise, player switches to X
                self.player = self.aiPlayer.switchPlayer(self.player)

        # If board is full, game ends. Message is printed
        if self.isFull() == True:
            self.draw.itemconfig(self.message, text='Tie! Game over.')

    # Closes window
    def quitGame(self):
        self.window.destroy()

    # Starts a new game by clearing board, changing start player to X,
    # and printing starting message
    def newGame(self):
        self.data = []
        self.player = 'X'
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' '] # one row
                self.draw.itemconfig(self.circles[row][col], fill='white')
                self.draw.itemconfig(self.message, text='Starting game! Select a column.')
            self.data += [boardRow] # adds row to matrix
        self.gameOn = True

    # Add moves to the game
    # ox input is either X or O (depending on the player)
    # Checks each row in column until a space is found. Puts an
    # X or an O in that space
    def addMove(self,col,ox):
        colLength = self.height - 1
        for row in range(self.height):
            if self.data[colLength-row][col] == ' ':
                # self.row is the next open spot in the column
                self.row = colLength-row
                self.data[colLength-row][col] = ox
                break

    # Checks if a move is allowed by going through
    # each row in the column to see if there's an empty space
    def allowsMove(self,col):
        for row in range(self.height):
            if self.data[row][col] == ' ':
                return True
        return False

    # Removes the most recent move in the column
    def delMove(self,col):
        for row in range(self.height):
            if self.data[row][col] in 'OX':
                self.data[row][col] = ' '
                break

    # Checks if every column is full
    def isFull(self):
        numFullColumns = 0
        for col in range(self.width):
            if self.allowsMove(col) == False:
                numFullColumns += 1
        if numFullColumns == self.width:
            return True
        return False

    # Checks for horizontal, vertical, and diagonal wins
    def winsFor(self,ox):
       	# Horizontal wins
        for row in range(0, self.height):
            for col in range(0, self.width-3):
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                    return True

        # Vertical wins
        for row in range(0, self.height-3):
            for col in range(0, self.width):
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    return True

        # Diagonal wins NE to SW
        for row in range(0, self.height):
            for col in range(0, self.width-3):
                if self.data[row][col] == ox and \
                self.data[row-1][col+1] == ox and \
                self.data[row-2][col+2] == ox and \
                self.data[row-3][col+3] == ox:
                    return True

        # Diagonal wins NW to SE
        for row in range(0, self.height-3):
            for col in range(0, self.width-3):
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    return True

        return False

# Generates moves for AI
class Player:
    def __init__(self, ox, tbt, ply):
        # Sets player, tiebreaker, and ply
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    # Prints out ply and tiebreaker
    def __repr__(self):
        return 'Ply: %d\nTiebreaker: %s' % (self.ply, self.tbt)

    # Switches the player
    def switchPlayer(self, player):
        if player == 'X':
            return 'O'
        else:
            return'X'

    #Returns a list of possible scores for each column
    def scoresFor(self, b, ox, ply):
        # Each index is a column's score for making a move
        scores = []

        # Base case
        if ply == 0:
            for col in range(b.width):
                if b.allowsMove(col) == False:
                    scores.append(-1)
                else:
                    scores.append(50.0)
            return scores

        # Goes through each column
        for col in range(b.width):
            # Adds move to column if it is allowed
            if b.allowsMove(col) == True:
                b.addMove(col, ox)
                # If move causes a win, add 100.0 as score to that column
                if b.winsFor(ox) == True:
                    scores.append(100.0)
                # If move is not a win and ply is greater than 1
                elif ply > 1:
                    # Check the next ply (opponent's move)
                    scores.append(100-max(self.scoresFor(b, self.switchPlayer(ox), ply-1)))
                # If move doesn't cause win or lose
                # and ply is less than 1
                else:
                    scores.append(50.0)
                # Delete move after it's added and checked
                b.delMove(col)
            # If move is not allowed, score for the column is -1
            else:
                scores.append(-1)

        return scores

    # Returns column number that is the best move
    def nextMove(self, b):
        scoreList = self.scoresFor(b, self.ox, self.ply)
        return self.tiebreakMove(scoreList)

    # Checks for tiebreakers, returns result based on tbt
    def tiebreakMove(self, scores):
        # Looks for first occurence of the greatest score (100.0),
        # if not found, looks for first occurence of 50.0, and then
        # 0.0 if 50.0 not found
        if self.tbt == 'Left':
            for i in range(len(scores)):
                if scores[i] == 100.0:
                    return i
            for i in range(len(scores)):
                if scores[i] == 50.0:
                    return i
            for i in range(len(scores)):
                if scores[i] == 0.0:
                    return i

        # Does what left tiebreaker does, except looks for last
        # occurence of that score.
        if self.tbt == 'Right':
            for i in range(len(scores)):
                if scores[len(scores)-1-i] == 100.0:
                    return len(scores)-1-i
            for i in range(len(scores)):
                if scores[len(scores)-1-i] == 50.0:
                    return len(scores)-1-i
            for i in range(len(scores)):
                if scores[len(scores)-1-i] == 0.0:
                    return len(scores)-1-i

        # Find occurences of the largest score and randomly chooses
        # a column that has that score.
        if self.tbt == 'Random':
            bestScores = []

            if 100.0 in scores:
                for i in range(len(scores)):
                    if scores[i] == 100.0:
                        bestScores.append(i)
            elif 50.0 in scores:
                for i in range(len(scores)):
                    if scores[i] == 50.0:
                        bestScores.append(i)
            else:
                for i in range(len(scores)):
                    if scores[i] == 0.0:
                        bestScores.append(i)

            return random.choice(bestScores)

def main():
    # Creates a window where the game will be displayed
    root = Tk()
    root.title('Connect 4')

    # Creates an AI player and starts a new game with it
    aiPlayer = Player('O', 'Random', 4)
    game1 = Connect4(7, 6, aiPlayer, root)

    # Continuously displays the window
    root.mainloop()

if __name__ == '__main__':
    main()
