class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None


class Matrix:
    def __init__(self, numRows, numCols):
        self.numrows = numRows
        self.numCols = numCols
        self.head = None
    #todo def getValue(self, currentRow, currentCol):
    #todo setMatrix(self, row, col, value)
    todo def multiply(self, Matrix)