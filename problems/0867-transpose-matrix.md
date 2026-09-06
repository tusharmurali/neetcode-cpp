# 867. Transpose Matrix

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/transpose-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/transpose-matrix>  
- **Video:** <https://www.youtube.com/watch?v=DzMT3bDgVn0>  

[← Back to index](../INDEX.md)

## 1. Iteration - I

Transposing a matrix means flipping it over its main diagonal, turning rows into columns and columns into rows. The element at position `(r, c)` in the original matrix moves to position `(c, r)` in the transposed matrix.

Since the dimensions may change (an `m x n` matrix becomes `n x m`), we need to create a new result matrix with swapped dimensions. Then we simply copy each element to its new position.

```cpp
class Solution {
public:
    vector<vector<int>> transpose(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        vector<vector<int>> res(COLS, vector<int>(ROWS));

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                res[c][r] = matrix[r][c];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$ for the output array.

> Where $n$ is the number of rows and $m$ is the number of columns in the matrix.

## 2. Iteration - II

For square matrices, we can transpose in-place by swapping elements across the main diagonal. We only need to process elements above (or below) the diagonal to avoid swapping twice.

However, for non-square matrices, in-place transposition is not possible since the dimensions change. In this case, we fall back to creating a new matrix. This approach optimizes memory usage when the input is square.

```cpp
class Solution {
public:
    vector<vector<int>> transpose(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();

        if (ROWS == COLS) {
            for (int r = 0; r < ROWS; r++) {
                for (int c = 0; c < r; c++) {
                    swap(matrix[r][c], matrix[c][r]);
                }
            }

            return matrix;
        }

        vector<vector<int>> res(COLS, vector<int>(ROWS));

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                res[c][r] = matrix[r][c];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of rows and $m$ is the number of columns in the matrix.
