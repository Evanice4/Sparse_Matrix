# Sparse Matrix Operations

This project implements sparse matrix operations such as addition, subtraction, and multiplication using custom data structures to optimize memory usage and runtime.

## Features

- Load two sparse matrices from input files
- Perform matrix addition, subtraction, and multiplication
- Save the result matrix to an output file in the same format
- Handle input variations such as whitespaces and invalid formats
- Implement custom exception handling for incorrect input formats

## Requirements

- Python 3.6+
- No external libraries required

## Project Structure

```
/dsa/sparse_matrix/
    ├── code/
    │   └── src/
    │       └── spmatrix.py    # Main source code
    ├── sample_inputs/         # Input files with sparse matrices
    ├── sample_outputs/        # Generated output files
    └── README.md              # This file
```

## Input File Format

Each sparse matrix input file should follow this format:

1. The first line specifies the number of rows (`rows=X`)
2. The second line specifies the number of columns (`cols=Y`)
3. Each subsequent line represents a non-zero element in the matrix in the format `(row, column, value)`

Example:

```
rows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)
```

## Usage

### Command-line Execution

Navigate to the `src/` folder and use the following command:

```bash
python spmatrix.py <operation> <input_file_1> <input_file_2> <output_file>
```

- `<operation>`: Specify one of the following: `add`, `subtract`, or `multiply`
- `<input_file_1>`: Path to the first matrix input file
- `<input_file_2>`: Path to the second matrix input file
- `<output_file>`: Path where the result matrix will be saved

Example:

```bash
python spmatrix.py add ../sample_inputs/matrix1.txt ../sample_inputs/matrix2.txt ../sample_outputs/result.txt
```

This command will add the matrices in `matrix1.txt` and `matrix2.txt`, and save the result to `result.txt`.

## Code Structure

- `SparseMatrix` Class: Handles the storage and manipulation of the sparse matrix
- `load_matrix`: Loads a matrix from a file
- `save_matrix`: Saves the result matrix to a file
- `add`: Adds two sparse matrices
- `subtract`: Subtracts the second matrix from the first
- `multiply`: Multiplies two sparse matrices

## Example Code Usage

```python
matrix1 = SparseMatrix('matrix1.txt')  # Load first matrix from file
matrix2 = SparseMatrix('matrix2.txt')  # Load second matrix from file

# Perform matrix addition
result_matrix = matrix1.add(matrix2)

# Save the result to a file
result_matrix.save_matrix('result.txt')
```

## Error Handling

The program handles:

- Invalid format: Raises `ValueError` if the input file does not conform to the expected format
- Dimension mismatches: Raises `ValueError` if the matrices cannot be added, subtracted, or multiplied due to incompatible dimensions


## Contributing

1. Fork this repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit them (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or issues, feel free to reach out.
