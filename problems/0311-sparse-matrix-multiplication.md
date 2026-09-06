# 311. Sparse Matrix Multiplication

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sparse-matrix-multiplication/>  
- **NeetCode:** <https://neetcode.io/problems/sparse-matrix-multiplication>  

[← Back to index](../INDEX.md)

## 1. Naive Iteration

Standard matrix multiplication computes each element of the result by taking the dot product of a row from the first matrix and a column from the second. For sparse matrices (matrices with many zeros), we can skip computations involving zero elements since they contribute nothing to the result. By checking if an element in mat1 is non-zero before processing, we avoid unnecessary multiplications.

```cpp
class Solution {
public:
    vector<vector<int>> multiply(vector<vector<int>>& mat1, vector<vector<int>>& mat2) {
        int n = mat1.size();
        int k = mat1[0].size();
        int m = mat2[0].size();

        // Product matrix will have 'n x m' size.
        vector<vector<int>> ans (n, vector<int>(m, 0));

        for (int rowIndex = 0; rowIndex < n; ++rowIndex) {
            for (int elementIndex = 0; elementIndex < k; ++elementIndex) {
                // If current element of mat1 is non-zero then iterate over all columns of mat2.
                if (mat1[rowIndex][elementIndex] != 0)  {
                    for (int colIndex = 0; colIndex < m; ++colIndex) {
                        ans[rowIndex][colIndex] += mat1[rowIndex][elementIndex] * mat2[elementIndex][colIndex];
                    }
                }
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot k \cdot n)$
- Space complexity: $O(1)$

> Where $m$ and $k$ represent the number of rows and columns in `mat1`, respectively and $k$ and $n$ represent the number of rows and columns in `mat2`, respectively.

## 2. List of Lists

To further optimize sparse matrix multiplication, we can preprocess both matrices to store only their non-zero elements. For each row, we keep a list of (value, column) pairs representing non-zero entries. This compressed representation allows us to iterate only over non-zero elements when computing the product, making the algorithm efficient for highly sparse matrices.

```cpp
class Solution {
public:
    vector<vector<pair<int, int>>> compressMatrix(vector<vector<int>>& matrix) {
        int rows = matrix.size();
        int cols = matrix[0].size();
        vector<vector<pair<int, int>>> compressedMatrix(rows);

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (matrix[row][col] != 0) {
                    compressedMatrix[row].push_back({matrix[row][col], col});
                }
            }
        }
        return compressedMatrix;
    }

    vector<vector<int>> multiply(vector<vector<int>>& mat1, vector<vector<int>>& mat2) {
        int m = mat1.size();
        int k = mat1[0].size();
        int n = mat2[0].size();

        // Store the non-zero values of each matrix.
        vector<vector<pair<int, int>>> A = compressMatrix(mat1);
        vector<vector<pair<int, int>>> B = compressMatrix(mat2);

        vector<vector<int>> ans(m, vector<int>(n, 0));

        for (int mat1Row = 0; mat1Row < m; ++mat1Row) {
            // Iterate on all current 'row' non-zero elements of mat1.
            for (auto [element1, mat1Col] : A[mat1Row]) {

                // Multiply and add all non-zero elements of mat2
                // where the row is equal to col of current element of mat1.
                for (auto [element2, mat2Col] : B[mat1Col]) {
                    ans[mat1Row][mat2Col] += element1 * element2;
                }
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot k \cdot n)$
- Space complexity: $O(m \cdot k + k \cdot n)$

> Where $m$ and $k$ represent the number of rows and columns in `mat1`, respectively and $k$ and $n$ represent the number of rows and columns in `mat2`, respectively.

## 3. Yale Format

The Yale format (also known as Compressed Sparse Row/Column) is a standard way to represent sparse matrices efficiently. It uses three arrays: values (non-zero elements), column/row indices, and row/column pointers that mark where each row/column starts in the values array. By compressing mat1 row-wise and mat2 column-wise, we can efficiently compute dot products by merging two sorted lists of indices.

```cpp
class SparseMatrix {
public:
    int cols = 0, rows = 0;
    vector<int> values, colIndex, rowIndex;

    // Compressed Sparse Row
    SparseMatrix(vector<vector<int>>& matrix) {
        rows = matrix.size();
        cols = matrix[0].size();
        rowIndex.push_back(0);

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (matrix[row][col]) {
                    values.push_back(matrix[row][col]);
                    colIndex.push_back(col);
                }
            }
            rowIndex.push_back(values.size());
        }
    }

    // Compressed Sparse Column
    SparseMatrix(vector<vector<int>>& matrix, bool colWise) {
        rows = matrix.size();
        cols = matrix[0].size();
        colIndex.push_back(0);

        for (int col = 0; col < cols; ++col) {
            for (int row = 0; row < rows; ++row) {
                if (matrix[row][col]) {
                    values.push_back(matrix[row][col]);
                    rowIndex.push_back(row);
                }
            }
            colIndex.push_back(values.size());
        }
    }
};

class Solution {
public:
    vector<vector<int>> multiply(vector<vector<int>>& mat1, vector<vector<int>>& mat2) {
        SparseMatrix A (mat1);
        SparseMatrix B (mat2, true);

        vector<vector<int>> ans(mat1.size(), vector<int>(mat2[0].size(), 0));

        for (int row = 0; row < ans.size(); ++row) {
            for (int col = 0; col < ans[0].size(); ++col) {

                // Row element range indices
                int matrixOneRowStart = A.rowIndex[row];
                int matrixOneRowEnd = A.rowIndex[row + 1];

                // Column element range indices
                int matrixTwoColStart = B.colIndex[col];
                int matrixTwoColEnd = B.colIndex[col + 1];

                // Iterate over both row and column.
                while (matrixOneRowStart < matrixOneRowEnd && matrixTwoColStart < matrixTwoColEnd) {
                    if (A.colIndex[matrixOneRowStart] < B.rowIndex[matrixTwoColStart]) {
                        matrixOneRowStart++;
                    } else if (A.colIndex[matrixOneRowStart] > B.rowIndex[matrixTwoColStart]) {
                        matrixTwoColStart++;
                    } else {
                        // Row index and col index are same so we can multiply these elements.
                        ans[row][col] += A.values[matrixOneRowStart] * B.values[matrixTwoColStart];
                        matrixOneRowStart++;
                        matrixTwoColStart++;
                    }
                }
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n \cdot k)$
- Space complexity: $O(m \cdot k + k \cdot n)$

> Where $m$ and $k$ represent the number of rows and columns in `mat1`, respectively and $k$ and $n$ represent the number of rows and columns in `mat2`, respectively.
