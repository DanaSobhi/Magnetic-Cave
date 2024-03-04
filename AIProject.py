import time

#Define the Constants
PLAYER_1 = '■'
PLAYER_2 = '□'
TIMEOUT = 3  #Timeout in seconds
AVAILABLE_PLACE = '˽' #Empty places in the board

class MagneticCave: #The game class: 
    def __init__(self):
        self.gameBoard = [[AVAILABLE_PLACE] * 8 for _ in range(8)] #The board range 8x8

    def showBoard(self):
        for row in self.gameBoard: 
            print(' '.join(row))
        print()

    def chosenMove(self, row, col, player): #Choose the available move in the board
        if 0 <= row < 8 and 0 <= col < 8 and self.gameBoard[row][col] == AVAILABLE_PLACE:
            self.gameBoard[row][col] = player
            return True
        return False

    def taken(self): #Check if the place in the board is taken or available
        for row in self.gameBoard:
            if AVAILABLE_PLACE in row:
                return False
        return True

    def theWinner(self, player): #Shows who's the winner of the game
        #Check rows
        for row in self.gameBoard:
            if ''.join(row).count(player * 5) > 0:
                return True

        #Check  the columns
        for col in range(8):
            column = ''.join([self.gameBoard[row][col] for row in range(8)])
            if column.count(player * 5) > 0:
                return True

        #Check the  diagonals
        for row in range(4):
            for col in range(4):
                diagonal1 = ''.join([self.gameBoard[row+i][col+i] for i in range(5)])
                diagonal2 = ''.join([self.gameBoard[row+i][col+4-i] for i in range(5)])
                if diagonal1.count(player * 5) > 0 or diagonal2.count(player * 5) > 0:
                    return True

        return False

    def evaluatePosition(self):
        #Heuristic evaluation function
        if self.theWinner(PLAYER_2):
            return 1  #Player 2 wins
        elif self.theWinner(PLAYER_1):
            return -1  #Player 1 wins
        else:
            return 0  #It's a draw

    def minimax(self, depth, maximizing_player, start_time): #Minimax function depends on the depth
        if depth == 0 or self.taken() or self.theWinner(PLAYER_1) or self.theWinner(PLAYER_2) or time.time() - start_time >= TIMEOUT:
            return self.evaluatePosition()

        if maximizing_player:
            maxmum_evaluation = float('-inf')
            for row in range(8):
                for col in range(8):
                    if self.gameBoard[row][col] == AVAILABLE_PLACE: #Check if the place is available "empty"
                        self.gameBoard[row][col] = PLAYER_2 #Place the player 2
                        evaluationScore = self.minimax(depth - 1, False, start_time)
                        self.gameBoard[row][col] = AVAILABLE_PLACE
                        maxmum_evaluation = max(maxmum_evaluation, evaluationScore)
            return maxmum_evaluation #Return the maximum evaluation score for player 2, which will be the Max player
        else:
            minmum_evaluation = float('inf') 
            for row in range(8):
                for col in range(8):
                    if self.gameBoard[row][col] == AVAILABLE_PLACE: #Check if the place is available "empty"
                        self.gameBoard[row][col] = PLAYER_1 #Place the player 1
                        evaluationScore = self.minimax(depth - 1, True, start_time)
                        self.gameBoard[row][col] = AVAILABLE_PLACE
                        minmum_evaluation = min(minmum_evaluation, evaluationScore)
            return minmum_evaluation #Return the minmum evaluation score for player 1, which is the min player

    def optimalMovement(self, player):
        initialTime = time.time()
        bestScore = float('-inf') 
        #Used from negative infinity score to compare it to get a better next movement
        bestMove = None

        for row in range(8): 
            for col in range(8):
                if self.gameBoard[row][col] == AVAILABLE_PLACE:
                    self.gameBoard[row][col] = player
                    score = self.minimax(1, False, initialTime) #Using depth as 1, because we need to run the automatic move faster
                    self.gameBoard[row][col] = AVAILABLE_PLACE 

                    if score > bestScore: #As we here compare it to the previous best score
                        bestScore = score #Assign best score as score 
                        bestMove = (row, col) #The replacement of best move. 

        return bestMove #Return the best move



    def play_game(self):
        print("Welcome to Magnetic Cave game!")
        print("Game mode:")
        print("1. Player vs. Player")
        print("2. Player vs. Automatic")
        print("3. Automatic vs. Player")

        while True:
            choice = input("Enter your choice (1-2-3): ")
            if choice == '1':
                self.playerVsPlayer()
                break
            elif choice == '2':
                self.playVsAuto()
                break
            elif choice == '3':
                self.autoVsPlayer()
                break
            else:
                print("Invalid choice! Please try again.")

    def playerVsPlayer(self):
        current_player = PLAYER_1
        while True:
            self.showBoard()

            while True: #While there's a move is made by player
                row = int(input("Player " + current_player + ", enter the row (0-7): "))
                col = int(input("Player " + current_player + ", enter the column (0-7): "))
                if self.chosenMove(row, col, current_player):
                    break
                print("Invalid move! Try again.") 

            if self.theWinner(current_player):
                self.showBoard()
                print(f"Player {current_player} wins!")
                break
            elif self.taken():
                self.showBoard()
                print("It's a tie!")
                break

            current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1 #Switching players

    def playVsAuto(self):
        current_player = PLAYER_1
        while True:
            self.showBoard()

            if current_player == PLAYER_1:
                while True:
                    row = int(input("Player " + current_player + ", enter the row (0-7): "))
                    col = int(input("Player " + current_player + ", enter the column (0-7): "))
                    if self.chosenMove(row, col, current_player):
                        break
                    print("Invalid move! Try again.") 
            else:
                print("Automatic player is Choosing a move!")
                start_time = time.time() #Start the timer
                best_move = self.optimalMovement(current_player)
                #The termination of the movement 
                end_time = time.time() 

                print(f"Automatic player took {end_time - start_time:.2f} seconds.")
                self.chosenMove(best_move[0], best_move[1], current_player)

            if self.theWinner(current_player):
                self.showBoard()
                print(f"Player {current_player} wins!")
                break
            elif self.taken():
                self.showBoard()
                print("It's a tie!") #Neither of the players won the game
                break

            current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1

    def autoVsPlayer(self):
        current_player = PLAYER_2
        while True:
            self.showBoard()

            if current_player == PLAYER_2:
                print("Automatic player is Choosing a move!")
                start_time = time.time() #Start the timer
                best_move = self.optimalMovement(current_player)
                #The termination of the movement 
                end_time = time.time() 

                print(f"Automatic player took {end_time - start_time:.2f} seconds.")
                self.chosenMove(best_move[0], best_move[1], current_player)
            else:
                while True:
                    row = int(input("Player " + current_player + ", enter the row (0-7): "))
                    col = int(input("Player " + current_player + ", enter the column (0-7): "))
                    if self.chosenMove(row, col, current_player):
                        break
                    print("Invalid move! Try again.") 

            if self.theWinner(current_player):
                self.showBoard()
                print(f"Player {current_player} wins!")
                break
            elif self.taken():
                self.showBoard()
                print("It's a tie!") #Neither of the players won the game
                break

            current_player = PLAYER_1 if current_player == PLAYER_2 else PLAYER_2


#Test the game
    def menu(self):
        while True:
            game = MagneticCave() #Get the class
            game.play_game() #Play the game to choose a mood
            answer = str(input("Do you want to play again or quit? y/n \n")) #Ask the user if they want to play again
            if answer == 'y': #If yes continue
                continue
            elif answer == 'n': #Else quit
                break

start = MagneticCave() #Get the class
start.menu() #Run the menu

########################################################################################