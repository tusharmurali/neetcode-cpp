# 59. Spiral Matrix II

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/spiral-matrix-ii/>  
- **NeetCode:** <https://neetcode.io/problems/spiral-matrix-ii>  
- **Video:** <https://www.youtube.com/watch?v=RvLrWFBJ9fM>  

[← Back to index](../INDEX.md)

## 1. Iteration

We fill an n x n matrix with values from 1 to n^2 in spiral order. Think of peeling an onion layer by layer. We maintain four boundaries (top, bottom, left, right) and fill each layer by moving right along the top row, down the right column, left along the bottom row, and up the left column. After completing each direction, we shrink the corresponding boundary inward.

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> mat(n, vector<int>(n, 0));
        int left = 0, right = n - 1, top = 0, bottom = n - 1, val = 1;

        while (left <= right) {
            // Fill every val in top row
            for (int c = left; c <= right; c++) {
                mat[top][c] = val++;
            }
            top++;

            // Fill every val in right col
            for (int r = top; r <= bottom; r++) {
                mat[r][right] = val++;
            }
            right--;

            // Fill every val in bottom row (reverse order)
            for (int c = right; c >= left; c--) {
                mat[bottom][c] = val++;
            }
            bottom--;

            // Fill every val in the left col (reverse order)
            for (int r = bottom; r >= top; r--) {
                mat[r][left] = val++;
            }
            left++;
        }

        return mat;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$ for the output matrix.

## 2. Recursion

The recursive approach mirrors the iterative one but uses function calls to handle each layer. We fill one complete ring of the spiral (top row, right column, bottom row, left column) and then recursively fill the inner portion. The base case is when the boundaries cross, meaning the entire matrix is filled.

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> mat(n, vector<int>(n, 0));
        fill(mat, 0, n - 1, 0, n - 1, 1);
        return mat;
    }

private:
    void fill(vector<vector<int>> &mat, int left, int right, int top, int bottom, int val) {
        if (left > right || top > bottom) return;

        // Fill every val in top row
        for (int c = left; c <= right; c++) {
            mat[top][c] = val++;
        }
        top++;

        // Fill every val in right col
        for (int r = top; r <= bottom; r++) {
            mat[r][right] = val++;
        }
        right--;

        // Fill every val in bottom row (reverse order)
        for (int c = right; c >= left; c--) {
            mat[bottom][c] = val++;
        }
        bottom--;

        // Fill every val in the left col (reverse order)
        for (int r = bottom; r >= top; r--) {
            mat[r][left] = val++;
        }
        left++;

        // Recur for the inner layer
        fill(mat, left, right, top, bottom, val);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity:
    - $O(n)$ space for recursion stack.
    - $O(n ^ 2)$ space for the output matrix.

## 3. Iteration (Optimal)

Instead of tracking four boundaries, we can use direction vectors to navigate the spiral. We start moving right and change direction (right -> down -> left -> up -> right...) whenever we hit a boundary or an already-filled cell. The direction change follows the pattern of rotating 90 degrees clockwise, which can be computed mathematically: if current direction is `(dr, dc)`, the next direction is `(dc, -dr)`.

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> mat(n, vector<int>(n, 0));
        int r = 0, c = 0, dr = 0, dc = 1;

        for (int val = 0; val < n * n; val++) {
            mat[r][c] = val + 1;
            int nextR = (r + dr) % n, nextC = (c + dc) % n;
            if (nextR < 0) nextR += n;
            if (nextC < 0) nextC += n;
            if (mat[nextR][nextC] != 0) {
                int temp = dr;
                dr = dc;
                dc = -temp;
            }
            r += dr;
            c += dc;
        }

        return mat;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$ for the output matrix.

## Standalone solution file (`cpp/0059-spiral-matrix-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given a positive integer n, generate an n x n matrix filled with elements from 1 to n2 in spiral order.
    Ex: Input  -> n = 3
        Output -> [[1,2,3],[8,9,4],[7,6,5]]

    Fill matrix layer by layer in four directions.

    Time - O(n^2)
    Space - O(1)
*/

class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        int left = 0, right = n - 1, top = 0, bottom = n - 1;
        int val = 1;
        vector<vector<int>> matrix(n, vector<int> (n));

        while (left <= right && top <= bottom) {
            for (int j = left; j <= right; j++) {
                matrix[top][j] = val++;
            }
            top++;
            
            for (int i = top; i <= bottom; i++) {
                matrix[i][right] = val++;
            }
            right--;
            
            for (int j = right; j >= left; j--) {
                matrix[bottom][j] = val++;
            }
            bottom--;
            
            for (int i = bottom; i >= top; i--) {
                matrix[i][left] = val++;
            }
            left++;
        }
        
        return matrix;
    }
};
```
