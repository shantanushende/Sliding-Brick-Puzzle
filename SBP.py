import copy
import os.path
import random
import time
from enum import Enum
import SBP



#part1
class State:

    # Define a class for the game state
    def __init__(self, matrix=None, parentState=None, fromMove=None, level=0, isNormalized=False):

        # Property for the state matrix
        self.matrix = matrix
        if matrix != None:
            # Property for the width of the matrix
            self.width = len(matrix[0])
            # Property for the height of the matrix
            if self.width > 0:
                self.height = len(matrix)
        # Property for the reference to the parent state
        self.parentState = parentState
        # Property for the current depth of the state
        self.level = level
        # Property for the reference to the move resulting in this state
        self.fromMove = fromMove
        # Property for whether the state has been normalized
        self.isNormalized = isNormalized
        # Property for the priority of this state
        self.priority = 0

    # 1A : State representation
    # Loading a gamestate from the file
    def loadFromFile(self, fileName):


        self.matrix = []
        self.width = 0
        self.height = 0

        # Load the file
        file = open(fileName)

        # Save the lines from the files
        fileLines = file.readlines()

        # Close the file buffer
        file.close()

        for index, line in enumerate(fileLines):
            # Split the line by the comma
            parsedValues = line.split(',')
            if index == 0:
                # Save the width and height of the puzzle
                self.width = int(parsedValues[0])
                self.height = int(parsedValues[1])
            else:
                pRow = []
                # Save the values
                for value in parsedValues:
                    if isNumeric(value):
                        pRow.append(int(value))
                # Add the row to the state
                self.matrix.append(pRow)


    # Apply the specified move to this state and return a clone
    def applyMoveCloning(self, move):
        # Clone the state
        stateClone = self.clone()

        # Apply the move
        stateClone.applyMove(move)

        # Return the clone
        return stateClone


    # Clone a game state
    def clone(self):
        return State(copy.deepcopy(self.matrix), self.parentState, self.fromMove, self.level, self.isNormalized)


    # Print the game state
    def print(self):
        # Concatenate the values in each row using "," as a delimiter
        joinedArray = []
        for row in self.matrix:
            joinedArray.append(', '.join(str(value) for value in row))
        # Concatenate the width, the height, and the rows using "\n" as a delimiter
        print(str(self.width) + ', ' + str(self.height) +
              ',\n' + ',\n'.join(joinedArray) + ',\n')





    # 1B
    # Check whether the game state is solved
    def puzzleCompleteCheck(self):
        # Go through the state 2-dimensional list to check whether a value of -1 exists
        # If yes, not solved. Otherwise, solved.
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.matrix[row][col] == -1:
                    return False
        return True

    # 1C 
    #Move generation    

    # Get all the possible moves of the state
    def getAllPossibleMoves(self):
        checkedpiece = []
        possibleMoves = []
        brickNumber = 0

        # Go through each cell to get the brick number,
        # then get the possible move of each number
        for row in range(0, self.height):
            for col in range(0, self.width):
                piecen = self.matrix[row][col]

                # Don't get moves for Wall, Empty, and Goal cells
                # For number that occupies more than one cell, don't get possible moves more than once
                if piecen < 2 or piecen in checkedpiece:
                    continue

                # Record the moves of the current brick number
                possibleMoves = possibleMoves + \
                    Piece(self, piecen).getAllPossibleMoves()

                # Record the brick number that has been checked
                checkedpiece.append(piecen)

        return possibleMoves

    # Get all the possible child states of this state
    def getAllPossibleNextStates(self):
        allPossibleNextStates = []
        # Get all the possible moves of the state
        apm = self.getAllPossibleMoves()
        possibleState = None

        # Apply each move and save the new states
        for move in apm:
            possibleState = self.applyMoveCloning(move)
            possibleState.parentState = self
            possibleState.fromMove = move
            possibleState.level = self.level + 1
            allPossibleNextStates.append(possibleState)

        return allPossibleNextStates

    # Apply the specified move to this state
    def applyMove(self, move):
        # Init the brick
        brick = Piece(self, move.piecen)

        # Set the cells of the brick to empty
        for cell in brick.occupiedCells:
            self.matrix[cell.row][cell.col] = 0

        # Apply the move to the current state
        for cell in brick.occupiedCells:
            if move.moveDirection == MoveDir.up.value:
                self.matrix[cell.row-1][cell.col] = move.piecen
            elif move.moveDirection == MoveDir.right.value:
                self.matrix[cell.row][cell.col+1] = move.piecen
            elif move.moveDirection == MoveDir.down.value:
                self.matrix[cell.row+1][cell.col] = move.piecen
            elif move.moveDirection == MoveDir.left.value:
                self.matrix[cell.row][cell.col-1] = move.piecen

        # Mark the state is not normalized anymore
        self.isNormalized = False









    #1d
    # Check whether this state equals to the specified state
    def equals(self, state):
        # Make sure two states have the same dimensions
        if self.width != state.width or self.height != state.height:
            return False

        # If the states are not normalized, normalize them before comparing
        if not self.isNormalized:
            self.normalize()

        if not state.isNormalized:
            state.normalize()

        # If there is a cell mismatch between the 2 states, return false
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.matrix[row][col] != state.matrix[row][col]:
                    return False

        # All cells match, return true
        return True

    #1e
    #Normalization

    # Normalize a puzzle state
    def normalize(self):
        # Only update piece number greater than 2
        nId = 2 + 1

        # Rearrange the brick number in incremental order from top left to bottom right of the matrix
        for r in range(0, self.height):
            for c in range(0, self.width):
                if self.matrix[r][c] == nId:
                    nId += 1
                elif self.matrix[r][c] > nId:
                    self.swapIdx(nId, self.matrix[r][c])
                    nId += 1

        self.isNormalized = True

    # Swap the brick numbers of two bricks
    def swapIdx(self, idx1, idx2):
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.matrix[row][col] == idx1:
                    self.matrix[row][col] = idx2
                elif self.matrix[row][col] == idx2:
                    self.matrix[row][col] = idx1


class MoveDir(Enum):
    # using integers in order to represent moves
    up = 1
    right = 2
    down = 3
    left = 4


class Piece:

    # Define a piece in the game
    def __init__(self, state, piecen):
        # Property for the reference of the game state
        self.state = state

        # Property for the piece number
        self.number = piecen

        # Record all the cells that this piece occupies
        self.occupiedCells = []
        for row in range(0, self.state.height):
            for col in range(0, self.state.width):
                if state.matrix[row][col] == piecen:
                    self.occupiedCells.append(CL(row, col))

    # Return all possible moves of the piece
    def getAllPossibleMoves(self):
        possibleMoves = []

        # Loop through all the possible directions
        # If the piece can move in the direction, record it
        for direction in MoveDir:
            if self.canMoveToDirection(direction.value):
                possibleMoves.append(Move(self.number, direction.value))

        return possibleMoves

    # Check whether the piece can move in certain direction
    def canMoveToDirection(self, direction):
        for cell in self.occupiedCells:
            moveToRow = 0
            moveToCol = 0
            toCellValue = 0

            # Check whether the cell can move to adjacent cell in the selected direction
            if direction == MoveDir.up.value:
                moveToRow = cell.row - 1
                moveToCol = cell.col
            elif direction == MoveDir.down.value:
                moveToRow = cell.row + 1
                moveToCol = cell.col
            elif direction == MoveDir.left.value:
                moveToRow = cell.row
                moveToCol = cell.col - 1
            elif direction == MoveDir.right.value:
                moveToRow = cell.row
                moveToCol = cell.col + 1

            # Get the value of the selected adjacent cell
            toCellValue = self.state.matrix[moveToRow][moveToCol]

            # If one cell of the piece cannot move in the selected direction, the whole piece cannot move in that direction
            # The target cell must be empty
            # Unless, a master piece is trying to move to the goal, or cell overlap other cells of the same piece
            if toCellValue != 0 and not (toCellValue == -1 and self.number == 2) and not toCellValue == self.number:
                return False

        return True


class CL:

    # Define a cell location in the state matrix
    def __init__(self, row, col):
        # Property for the row index of the cell
        self.row = row
        # Property for the column index of the cell
        self.col = col


class Move:

    # Define a move
    def __init__(self, piecen, moveDirection):
        # Property for the piece number
        self.piecen = piecen
        # Property for the numeric value of the direction
        self.moveDirection = moveDirection

    # Return the string describing the move
    def getmove(self):
        return '(' + str(self.piecen) + ', ' + MoveDir(self.moveDirection).name + ')'





def isNumeric(value):
    # Define check whether the specified value is a numeric value
    try:
        float(value)
        return True
    except ValueError:
        return False

#1f
# implementing random walks
def randomWalk(maxTurns, puzzleState):
    # Perform random walk on a game state
    isGoalReached = False
    currentTurn = 0
    possibleMoves = []

    # Print the game state
    puzzleState.print()

    # Keep doing random walk until either a goal is found or the max turn is exceeded
    while not isGoalReached and currentTurn < maxTurns:
        # Generate all possible moves on the board
        possibleMoves = puzzleState.getAllPossibleMoves()

        # Pick a random move
        randomMove = random.choice(possibleMoves)

        # Apply the move
        puzzleState.applyMove(randomMove)

        print(randomMove.getmove() + '\n')

        # Normalize the state
        puzzleState.normalize()

        # Print the normalized state
        puzzleState.print()

        # Check whether the goal is reached
        # If not, repeat. Otherwise, stop
        isGoalReached = puzzleState.puzzleCompleteCheck()

        # Increment the turn counter
        currentTurn += 1

#part2
# solve using BFS

def BFSsolution(puzzleState):


    # Record the starting time
    startTime = time.time()

    # A queue of states to check
    statesToCheck = [puzzleState]

    # A list of checked states
    checkedStates = []

    # Check if there are states to check
    while len(statesToCheck) > 0:
        # Check the next state in the queue
        state = statesToCheck.pop(0)
        # Save the checked state
        checkedStates.append(state)
        # Check whether the state has been resolved
        if state.puzzleCompleteCheck():
            # Print the solution
            printSearchSolution(state, len(checkedStates),
                                round(time.time() - startTime, 2))
            return
        # Get all the children of the current state to check later
        for nextState in state.getAllPossibleNextStates():
            # If a state has been checked, skip it
            if not checkStateInList(nextState, statesToCheck) and not checkStateInList(nextState, checkedStates):
                statesToCheck.append(nextState)




def DFSsolution(puzzleState):
    # Solve the game state using depth first search

    # Record the starting time
    startTime = time.time()

    # A stack of states to check
    statesToCheck = [puzzleState]

    # A list of checked states
    checkedStates = []

    while len(statesToCheck) > 0:
        # Check the next state in the queue
        state = statesToCheck.pop()
        # Save the checked state
        checkedStates.append(state)
        # Check whether the state has been resolved
        if state.puzzleCompleteCheck():
            # Print the solution
            printSearchSolution(state, len(checkedStates),
                                round(time.time() - startTime, 2))

            return
        # Get all the children of the current state to check later
        for nextState in state.getAllPossibleNextStates():
            # If a state has been checked, skip it
            if not checkStateInList(nextState, statesToCheck) and not checkStateInList(nextState, checkedStates):
                statesToCheck.append(nextState)


def IDSsolution(puzzleState):
    # Solve the puzzle using depth limit search

    # Record the starting time
    startTime = time.time()

    # A list of checked state
    checkedStates = []

    # First depth limit
    depthLimit = 0

    # Variable for the solved state
    solvedState = None

    # Total number of visited nodes
    totalVisitedNodes = 0

    # Keeps increasing the depth limit as long as the solution is not found yet
    while solvedState == None:
        solvedState, checkedStates = findSolutionUsingDepthLimitSearch(
            puzzleState, depthLimit)
        totalVisitedNodes += len(checkedStates)
        depthLimit += 1

    # Print the solution
    printSearchSolution(solvedState, totalVisitedNodes,
                        round(time.time() - startTime, 2))

def findSolutionUsingDepthLimitSearch(puzzleState, depthLimit):
    # Find a solved state of the puzzle within the specified depth limit
    # A stack of states to check
    statesToCheck = [puzzleState]
    checkedStates = []
    state = None

    # Check if we still have states to check
    while len(statesToCheck) > 0:
        # Remove an item from the stack
        state = statesToCheck.pop()

        # Record checked state
        checkedStates.append(state)

        # If this is the solution, return
        if state.puzzleCompleteCheck():
            return state, checkedStates

        # If this node is within the limit, add more children to check
        if state.level < depthLimit:
            # Get all possible child states
            for nextState in state.getAllPossibleNextStates():
                # If the child state has been checked, skip it
                # unless the child state's level is lower than the one in the record lists
                if not checkStateInList(nextState, checkedStates + statesToCheck, True):
                    statesToCheck.append(nextState)

    return None, checkedStates

def checkStateInList(state, stateList, skipLowerLevelItem=False):
    # Check whether a state is in a list of state
    for item in stateList:
        if (not skipLowerLevelItem or state.level >= item.level) and state.equals(item):
            return True
    return False


def printSearchSolution(solvedState, totalVisitedNodes, solvingTime):
    # A list of solution moves
    solutionMoves = []
    state = solvedState

    # Keep traversing up the state tree and record the move
    while state.parentState != None:
        solutionMoves.insert(0, state.fromMove)
        state = state.parentState

    # Print the moves
    for move in solutionMoves:
        print(move.getmove())

    # Print the solved state
    solvedState.print()

    # Print the solution stat
    print(str(totalVisitedNodes) + ' ' +
          str(solvingTime) + ' ' + str(len(solutionMoves)) + '\n')



def main():
    # Main function using which we call the BFS, DFS, IDS

    ps = SBP.State()

    # Load a game level from the file
    ps.loadFromFile("SBP-level0.txt")
    # Perform 3 random walks
    print("result of random walks")
    SBP.randomWalk(3, ps)

    # Load a state from file
    ps.loadFromFile("SBP-level1.txt")
    ps.loadFromFile("SBP-level2.txt")
    ps.loadFromFile("SBP-level3.txt")

    print("The result using BFS")

    SBP.BFSsolution(ps)

    print("The result using DFS:-")

    SBP.DFSsolution(ps)

    print("The result using IDS:-")

    SBP.IDSsolution(ps)

main()