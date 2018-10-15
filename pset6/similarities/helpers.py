from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    newA = " " + a
    newB = " " + b
    rowsA = len(newA)
    colsB = len(newB)
    
    #1 Set Up List
    matrix = [None] * rowsA
    for row in range(rowsA):
        matrix[row] = [None] * colsB

    #2 Base Case Insertion
    for row in range(rowsA):
        matrix[row][0] = (row, Operation.DELETED)
    
    for col in range(colsB):
        matrix[0][col] = (col, Operation.INSERTED)
    
    matrix[0][0] = (0, None)

    #3 Recursive Table Creation
    for row in range(rowsA):
        for col in range(colsB):
            if matrix[row][col] == None:
                deletionCost = int(matrix[row - 1][col][0]) + 1
                insertionCost = int(matrix[row][col - 1][0]) + 1
                if newA[row] == newB[col]:
                    subCost = int(matrix[row - 1][col - 1][0])
                else:
                    subCost = int(matrix[row - 1][col - 1][0]) + 1
                
                chosen = min(deletionCost, insertionCost, subCost)
                if chosen == deletionCost:
                    matrix[row][col] = (deletionCost, Operation.DELETED)
                elif chosen == insertionCost:
                    matrix[row][col] = (insertionCost, Operation.INSERTED)
                elif chosen == subCost:
                    matrix[row][col] = (subCost, Operation.SUBSTITUTED)
    
    # TODO

    return matrix
