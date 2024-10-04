class SparseMatrix:
    def load_matrix(self, file_path):
        """
        Load the sparse matrix from a file.
        The file format contains the number of rows and columns followed by non-zero values.
        Each non-zero value is stored as (row, col, value).
        """
        matrix = {}
        try:
            # Open the file and read row and column counts
            with open(file_path, 'r') as file:
                rows = int(file.readline().split('=')[1])  # Extract the number of rows
                cols = int(file.readline().split('=')[1])  # Extract the number of columns

                self.numRows = rows
                self.numCols = cols

                # Read each non-zero matrix entry in the format (row, column, value)
                for line in file:
                    if line.strip():  # Ignore empty lines or whitespace
                        row, col, value = self.parse_entry(line)  # Parse the entry
                        if row not in matrix:
                            matrix[row] = {}  # Initialize a new row if not already present
                        matrix[row][col] = value  # Store the value at the specified position

        except Exception as e:
            # Raise a Python standard exception for format issues
            raise ValueError(f"Input file has wrong format: {e}")
        
        return matrix  # Return the constructed matrix

    def __init__(self, matrix_file=None, numRows=None, numCols=None):
        """
        Initialize the SparseMatrix class.
        - If `matrix_file` is provided, load the matrix from the file.
        - If `numRows` and `numCols` are provided, create an empty matrix with those dimensions.
        """
        if matrix_file:
            self.matrix = self.load_matrix(matrix_file)  # Load the matrix from the file
        else:
            self.matrix = {}  # Initialize an empty matrix
            self.numRows = numRows
            self.numCols = numCols



    def parse_entry(self, line):
        """
        Parse a line containing a matrix entry.
        Each line is in the format (row, column, value).
        """
        # Remove parentheses and split the entry by commas
        entry = line.strip()[1:-1].split(',')
        return int(entry[0]), int(entry[1]), int(entry[2])  # Return the parsed row, column, and value

    def get_element(self, row, col):
        """
        Get the value of an element at a specific row and column.
        If the element is not explicitly stored (i.e., it's zero), return 0.
        """
        return self.matrix.get(row, {}).get(col, 0)  # Return the element if it exists, else return 0

    def set_element(self, row, col, value):
        """
        Set a value at a specific row and column in the matrix.
        If the row or column doesn't exist, it will be initialized.
        """
        if row not in self.matrix:
            self.matrix[row] = {}  # Initialize a new row if not present
        self.matrix[row][col] = value  # Set the value at the specified position

    def add(self, other_matrix):
        """
        Add this matrix to another sparse matrix.
        This operation adds non-zero elements and stores the result in a new matrix.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)  # Create a result matrix

        # Iterate through every position in the matrix
        for row in range(self.numRows):
            for col in range(self.numCols):
                # Add corresponding elements from both matrices
                result.set_element(row, col, self.get_element(row, col) + other_matrix.get_element(row, col))
        
        return result  # Return the result of the addition

    def subtract(self, other_matrix):
        """
        Subtract another sparse matrix from this matrix.
        This operation subtracts non-zero elements and stores the result in a new matrix.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)  # Create a result matrix

        # Iterate through every position in the matrix
        for row in range(self.numRows):
            for col in range(self.numCols):
                # Subtract corresponding elements from both matrices
                result.set_element(row, col, self.get_element(row, col) - other_matrix.get_element(row, col))
        
        return result  # Return the result of the subtraction

    def multiply(self, other_matrix):
        """
        Multiply this matrix with another sparse matrix.
        The operation follows matrix multiplication rules: The number of columns in the first matrix
        must be equal to the number of rows in the second matrix.
        """
        if self.numCols != other_matrix.numRows:
            raise ValueError("Matrix multiplication not possible with incompatible sizes.")  # Check matrix size compatibility

        result = SparseMatrix(numRows=self.numRows, numCols=other_matrix.numCols)  # Create a result matrix

        # Perform multiplication (row by column dot product)
        for row in self.matrix:
            for col in other_matrix.matrix:
                if col in self.matrix[row]:  # Only process non-zero elements
                    # Sum of product of corresponding elements
                    result.set_element(row, col, sum(self.get_element(row, k) * other_matrix.get_element(k, col) 
                                                     for k in range(self.numCols)))
        
        return result  # Return the result of the multiplication

    def save_to_file(self, file_path):
        """
        Save the sparse matrix to a file.
        The format will be similar to the input: number of rows, number of columns,
        followed by non-zero elements in (row, col, value) format.
        """
        with open(file_path, 'w') as file:
            # Write the number of rows and columns
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            
            # Write each non-zero element in the matrix
            for row in self.matrix:
                for col, value in self.matrix[row].items():
                    file.write(f"({row}, {col}, {value})\n")


# Main execution block for user interaction
if __name__ == "__main__":
    # Load two matrices from files
    matrix1 = SparseMatrix(matrix_file='./easy_sample_01_3.txt')
    matrix2 = SparseMatrix(matrix_file='./easy_sample_03_1.txt')

    # Menu for selecting the matrix operation
    print("Choose a matrix operation:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    choice = int(input("Enter your choice (1/2/3): "))

    # Perform the selected operation
    if choice == 1:
        result = matrix1.add(matrix2)
        print("Matrices added successfully!")
    elif choice == 2:
        result = matrix1.subtract(matrix2)
        print("Matrices subtracted successfully!")
    elif choice == 3:
        result = matrix1.multiply(matrix2)
        print("Matrices multiplied successfully!")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

    # Ask the user to save the result to a file
    output_file = input("Enter the output file path to save the result: ")
    result.save_to_file(output_file)
    print(f"Result saved to {output_file}.")
