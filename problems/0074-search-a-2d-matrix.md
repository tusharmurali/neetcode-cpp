# 74. Search a 2D Matrix

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/search-a-2d-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/search-2d-matrix>  
- **Video:** <https://www.youtube.com/watch?v=Ber2pi2C0j0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The brute force approach simply checks every element in the matrix one by one.
Since the matrix is sorted but we're ignoring that structure, we just scan through all rows and all columns until we either find the target or finish searching.

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        for (int r = 0; r < matrix.size(); r++) {
            for (int c = 0; c < matrix[r].size(); c++) {
                if (matrix[r][c] == target) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns of matrix.

## 2. Staircase Search

Since each row is sorted left-to-right **and** each column is sorted top-to-bottom, we can search smartly instead of checking every cell.

Start at the **top-right corner**:

- If the current value is **greater** than the target → move **left** (values decrease).
- If it is **smaller** than the target → move **down** (values increase).

This works like walking down a staircase—each step eliminates an entire row or column.
We keep moving until we either find the target or move out of bounds.

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), n = matrix[0].size();
        int r = 0, c = n - 1;

        while (r < m && c >= 0) {
            if (matrix[r][c] > target) {
                c--;
            } else if (matrix[r][c] < target) {
                r++;
            } else {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns of matrix.

## 3. Binary Search

Because each row of the matrix is sorted, and the rows themselves are sorted by their first and last elements, we can apply **binary search twice**:

1. **First search over the rows**
   We find the single row where the target _could_ exist by comparing the target with the row's first and last elements.
   Binary search helps us quickly narrow down to that one row.

2. **Then search inside that row**
   Once the correct row is found, we perform a normal binary search within that row to check if the target is present.

This eliminates large portions of the matrix at each step and uses the sorted structure fully.

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int ROWS = matrix.size();
        int COLS = matrix[0].size();

        int top = 0, bot = ROWS - 1;
        while (top <= bot) {
            int row = (top + bot) / 2;
            if (target > matrix[row][COLS - 1]) {
                top = row + 1;
            } else if (target < matrix[row][0]) {
                bot = row - 1;
            } else {
                break;
            }
        }

        if (!(top <= bot)) {
            return false;
        }
        int row = (top + bot) / 2;
        int l = 0, r = COLS - 1;
        while (l <= r) {
            int m = (l + r) / 2;
            if (target > matrix[row][m]) {
                l = m + 1;
            } else if (target < matrix[row][m]) {
                r = m - 1;
            } else {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(\log m + \log n)$ (which reduces to $O(\log(m * n))$)
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns of matrix.

## 4. Binary Search (One Pass)

Because the matrix is sorted row-wise and each row is sorted left-to-right, the entire matrix behaves like **one big sorted array**.
If we imagine flattening the matrix into a single list, the order of elements doesn't change.

This means we can run **one binary search** from index `0` to `ROWS * COLS - 1`.
For any mid index `m`, we can map it back to the matrix using:

- `row = m // COLS`
- `col = m % COLS`

This lets us access the correct matrix element without actually flattening the matrix.

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int ROWS = matrix.size(), COLS = matrix[0].size();

        int l = 0, r = ROWS * COLS - 1;
        while (l <= r) {
            int m = l + (r - l) / 2;
            int row = m / COLS, col = m % COLS;
            if (target > matrix[row][col]) {
                l = m + 1;
            } else if (target < matrix[row][col]) {
                r = m - 1;
            } else {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(\log(m * n))$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns of matrix.

## Standalone solution file (`cpp/0074-search-a-2d-matrix.cpp` in the NeetCode repo)

```cpp
/*
    Search for target value in matrix where every row & col is sorted

    Perform 2 binary searches: 1 to find row, then another to find col

    Time: O(log m + log n)
    Space: O(1)
*/

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int lowRow = 0;
        int highRow = matrix.size() - 1;
        
        while (lowRow < highRow) {
            int mid = lowRow + (highRow - lowRow) / 2;
            if (matrix[mid][0] == target) {
                return true;
            }
            if (matrix[mid][0] < target && target < matrix[mid + 1][0]) {
                lowRow = mid;
                break;
            }
            if (matrix[mid][0] < target) {
                lowRow = mid + 1;
            } else {
                highRow = mid - 1;
            }
        }
        
        int lowCol = 0;
        int highCol = matrix[0].size() - 1;
        
        while (lowCol <= highCol) {
            int mid = lowCol + (highCol - lowCol) / 2;
            if (matrix[lowRow][mid] == target) {
                return true;
            }
            if (matrix[lowRow][mid] < target) {
                lowCol = mid + 1;
            } else {
                highCol = mid - 1;
            }
        }
        
        return false;
    }
};
```
