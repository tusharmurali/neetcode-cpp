# 73. Set Matrix Zeroes

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/set-matrix-zeroes/>  
- **NeetCode:** <https://neetcode.io/problems/set-zeroes-in-matrix>  
- **Video:** <https://www.youtube.com/watch?v=T41rL0L3Pnw>  
- **Video approach:** 3. Iteration (Space Optimized)  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to modify the matrix so that if any cell is `0`, then its **entire row and entire column** become `0`.

The main challenge is that if we change cells to `0` while scanning, those newly created zeros could incorrectly force more rows/columns to be zeroed.

To avoid this, the brute force approach uses a **separate copy** of the matrix:

- we read zeros from the original matrix
- we write the row/column changes into the copy
- at the end, we copy the final values back

This keeps the logic simple and prevents accidental cascading updates.

```cpp
class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        vector<vector<int>> mark = matrix;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (matrix[r][c] == 0) {
                    for (int col = 0; col < COLS; col++) {
                        mark[r][col] = 0;
                    }
                    for (int row = 0; row < ROWS; row++) {
                        mark[row][c] = 0;
                    }
                }
            }
        }

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                matrix[r][c] = mark[r][c];
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O((m * n) * (m + n))$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Iteration

We need to update the matrix so that if a cell is `0`, then **its entire row and entire column** are set to `0`.

The key challenge is to avoid modifying the matrix **too early**.
If we directly set rows and columns to `0` while scanning, newly created zeros could incorrectly trigger more rows and columns to be zeroed.

To handle this safely, we split the process into **two passes**:

1. First pass: **record** which rows and columns need to be zeroed using `rows` and `cols` flags
2. Second pass: **apply** the zeroing based on that record

We use two helper arrays:

- `rows[r]` → whether row `r` should be zeroed
- `cols[c]` → whether column `c` should be zeroed

This keeps the logic clean and easy to reason about.

```cpp
class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int rows = matrix.size(), cols = matrix[0].size();
        vector<bool> rowZero(rows, false);
        vector<bool> colZero(cols, false);

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (matrix[r][c] == 0) {
                    rowZero[r] = true;
                    colZero[c] = true;
                }
            }
        }

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (rowZero[r] || colZero[c]) {
                    matrix[r][c] = 0;
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Iteration (Space Optimized) ▶ video

We need to set an entire row and column to `0` if any cell in that row or column is `0`.

The common two-array solution uses extra space to remember which rows/columns should be zeroed.
To optimize space, we can reuse the matrix itself as the "marker storage":

- Use the **first row** to mark which columns should become zero
- Use the **first column** to mark which rows should become zero

One complication:

- `matrix[0][0]` sits at the intersection of the first row and first column, so it can't independently represent both.
- Also, we must separately track whether the **first row** originally contained a zero.

That's why we keep a boolean `rowZero`:

- `rowZero = true` means the first row must be zeroed at the end.

```cpp
class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        bool rowZero = false;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (matrix[r][c] == 0) {
                    matrix[0][c] = 0;
                    if (r > 0) {
                        matrix[r][0] = 0;
                    } else {
                        rowZero = true;
                    }
                }
            }
        }

        for (int r = 1; r < ROWS; r++) {
            for (int c = 1; c < COLS; c++) {
                if (matrix[0][c] == 0 || matrix[r][0] == 0) {
                    matrix[r][c] = 0;
                }
            }
        }

        if (matrix[0][0] == 0) {
            for (int r = 0; r < ROWS; r++) {
                matrix[r][0] = 0;
            }
        }

        if (rowZero) {
            for (int c = 0; c < COLS; c++) {
                matrix[0][c] = 0;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## Standalone solution file (`cpp/0073-set-matrix-zeroes.cpp` in the NeetCode repo)

```cpp
/*
    Given matrix, if element 0, set entire row/col to 0

    Use 1st row/col as flag to determine if entire row/col 0

    Time: O(mn)
    Space: O(1)
*/

class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size();
        int n = matrix[0].size();
        
        bool isFirstRowZero = false;
        bool isFirstColZero = false;
        
        for (int i = 0; i < m; i++) {
            if (matrix[i][0] == 0) {
                isFirstColZero = true;
                break;
            }
        }
        
        for (int j = 0; j < n; j++) {
            if (matrix[0][j] == 0) {
                isFirstRowZero = true;
                break;
            }
        }
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = 0;
                    matrix[0][j] = 0;
                }
            }
        }
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                    matrix[i][j] = 0;
                }
            }
        }
        
        if (isFirstColZero) {
            for (int i = 0; i < m; i++) {
                matrix[i][0] = 0;
            }
        }
        
        if (isFirstRowZero) {
            for (int j = 0; j < n; j++) {
                matrix[0][j] = 0;
            }
        }
    }
};
```
