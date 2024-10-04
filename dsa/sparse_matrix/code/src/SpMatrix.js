const fs = require('fs').promises;
const path = require('path');
const readline = require('readline');

class SparseMatrix {
    constructor(rows, cols) {
        this.rows = rows;
        this.cols = cols;
        this.elements = new Map();
    }

    static async fromFile(filepath) {
        const fileContent = await fs.readFile(filepath, 'utf8');
        const lines = fileContent.split('\n');
        const rows = parseInt(lines[0].split('=')[1]);
        const cols = parseInt(lines[1].split('=')[1]);
        const matrix = new SparseMatrix(rows, cols);

        for (let i = 2; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line) {
                const match = line.match(/\((\d+),\s*(\d+),\s*(-?\d+)\)/);
                if (match) {
                    const [, row, col, value] = match;
                    matrix.setElement(parseInt(row), parseInt(col), parseInt(value));
                } else {
                    throw new Error("Input file has wrong format");
                }
            }
        }
        return matrix;
    }

    getElement(row, col) {
        return this.elements.get(`${row},${col}`) || 0;
    }

    setElement(row, col, value) {
        if (row < 0 || row >= this.rows || col < 0 || col >= this.cols) {
            throw new Error("Invalid row or column index");
        }
        if (value !== 0) {
            this.elements.set(`${row},${col}`, value);
        } else {
            this.elements.delete(`${row},${col}`);
        }
    }

    add(other) {
        if (this.rows !== other.rows || this.cols !== other.cols) {
            throw new Error("Matrix dimensions do not match for addition");
        }
        const result = new SparseMatrix(this.rows, this.cols);
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const sum = this.getElement(row, col) + other.getElement(row, col);
                if (sum !== 0) {
                    result.setElement(row, col, sum);
                }
            }
        }
        return result;
    }

    subtract(other) {
        if (this.rows !== other.rows || this.cols !== other.cols) {
            throw new Error("Matrix dimensions do not match for subtraction");
        }
        const result = new SparseMatrix(this.rows, this.cols);
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const diff = this.getElement(row, col) - other.getElement(row, col);
                if (diff !== 0) {
                    result.setElement(row, col, diff);
                }
            }
        }
        return result;
    }

    multiply(other) {
        if (this.cols !== other.rows) {
            throw new Error("Matrix dimensions are not compatible for multiplication");
        }
        const result = new SparseMatrix(this.rows, other.cols);
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < other.cols; col++) {
                let sum = 0;
                for (let k = 0; k < this.cols; k++) {
                    sum += this.getElement(row, k) * other.getElement(k, col);
                }
                if (sum !== 0) {
                    result.setElement(row, col, sum);
                }
            }
        }
        return result;
    }

    async toFile(filepath) {
        let content = `rows=${this.rows}\ncols=${this.cols}\n`;
        for (const [key, value] of this.elements) {
            const [row, col] = key.split(',');
            content += `(${row}, ${col}, ${value})\n`;
        }
        await fs.writeFile(filepath, content);
    }
}

async function ensureDirectoryExists(dirPath) {
    try {
        await fs.access(dirPath);
    } catch (error) {
        await fs.mkdir(dirPath, { recursive: true });
    }
}

async function main() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    const question = (query) => new Promise((resolve) => rl.question(query, resolve));

    // Define paths according to the specified structure
    const baseDir = '/dsa/sparse_matrix'; // Base directory for the sparse matrix
    const inputDir = path.join(baseDir, 'sample_inputs'); // Input files directory
    const outputDir = path.join(baseDir, 'output'); // Output files directory

    // Ensure the output directory exists
    await ensureDirectoryExists(outputDir);

    try {
        while (true) {
            const operation = await question("Select operation (add/subtract/multiply) or 'quit' to exit: ");
            if (operation.toLowerCase() === 'quit') {
                break;
            }
            if (!['add', 'subtract', 'multiply'].includes(operation.toLowerCase())) {
                console.log("Invalid operation. Please try again.");
                continue;
            }

            const file1 = 'matrix1.txt'; // Specify the first input file directly
            const file2 = 'matrix2.txt'; // Specify the second input file directly
            const outputFile = `result_${operation}_${path.basename(file1)}_${path.basename(file2)}`;

            try {
                const matrix1 = await SparseMatrix.fromFile(path.join(inputDir, file1));
                const matrix2 = await SparseMatrix.fromFile(path.join(inputDir, file2));

                let result;
                switch (operation.toLowerCase()) {
                    case 'add':
                        result = matrix1.add(matrix2);
                        break;
                    case 'subtract':
                        result = matrix1.subtract(matrix2);
                        break;
                    case 'multiply':
                        result = matrix1.multiply(matrix2);
                        break;
                }

                const outputPath = path.join(outputDir, outputFile);
                await result.toFile(outputPath);
                console.log(`Operation completed. Result written to ${outputPath}`);
            } catch (error) {
                console.error("An error occurred:", error.message);
            }
        }
    } finally {
        rl.close();
    }
}

main().catch(console.error);