# 54. Spiral Matrix

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/spiral-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/spiral-matrix>  
- **Video:** <https://www.youtube.com/watch?v=BJnMZNwUk1M>  

[← Back to index](../INDEX.md)

## 1. Recursion

We want to print the matrix in **spiral order** (right → down → left → up, repeating).

This solution treats the spiral as a sequence of smaller and smaller “rings”.
Each ring can be described by:

- how many rows are left to cover
- how many columns are left to cover
- a current position `(r, c)`
- a direction `(dr, dc)` that tells us where to move next

At each step, we do two things:

1. **Walk straight** in the current direction and append all elements along that edge.
2. **Shrink the problem** and rotate direction for the next edge.

After moving along one edge, the remaining unvisited area becomes a smaller rectangle, and the next direction is obtained by “turning right” (changing `(dr, dc)`).

```cpp
class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<int> res;

        // append all the elements in the given direction
        dfs(m, n, 0, -1, 0, 1, matrix, res);
        return res;
    }

    void dfs(int row, int col, int r, int c, int dr, int dc,
             vector<vector<int>>& matrix, vector<int>& res) {
        if (row == 0 || col == 0) return;

        for (int i = 0; i < col; i++) {
            r += dr;
            c += dc;
            res.push_back(matrix[r][c]);
        }

        // sub-problem
        dfs(col, row - 1, r, c, dc, -dr, matrix, res);
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(min(m, n))$ space for recursion stack.
    - $O(m * n)$ space for the output list.

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Iteration

We want to traverse a matrix in **spiral order**:  
right → down → left → up, repeatedly, moving inward layer by layer.

A clean iterative way to do this is to maintain **four boundaries**:

- `top` → the topmost unvisited row
- `bottom` → one past the bottommost unvisited row
- `left` → the leftmost unvisited column
- `right` → one past the rightmost unvisited column

At each step, we walk along the current outer boundary in four directions:

1. left → right across the top row
2. top → bottom down the right column
3. right → left across the bottom row
4. bottom → top up the left column

After each pass, we shrink the boundaries inward.

```cpp
class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> res;
        int left = 0, right = matrix[0].size();
        int top = 0, bottom = matrix.size();

        while (left < right && top < bottom) {
            for (int i = left; i < right; i++) {
                res.push_back(matrix[top][i]);
            }
            top++;
            for (int i = top; i < bottom; i++) {
                res.push_back(matrix[i][right - 1]);
            }
            right--;
            if (!(left < right && top < bottom)) {
                break;
            }
            for (int i = right - 1; i >= left; i--) {
                res.push_back(matrix[bottom - 1][i]);
            }
            bottom--;
            for (int i = bottom - 1; i >= top; i--) {
                res.push_back(matrix[i][left]);
            }
            left++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(m * n)$ space for the output list.

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Iteration (Optimal)

We want to read the matrix in **spiral order**: right → down → left → up, repeating.

Instead of keeping four boundaries (`top`, `bottom`, `left`, `right`), this approach tracks:

- the **current direction** (right, down, left, up)
- how many **steps** we can take in the current direction before turning

Key idea:

- Spiral traversal alternates between moving along a **row length** and a **column length**
    - first we move right `cols` steps
    - then down `rows - 1` steps
    - then left `cols - 1` steps
    - then up `rows - 2` steps
    - and so on...
- After completing a direction, the available steps in that “dimension” shrink by 1.

We store the remaining step counts in an array:

- `steps[0]` = how many moves left in the horizontal direction
- `steps[1]` = how many moves left in the vertical direction

`d & 1` tells us whether the current direction is horizontal (`0`) or vertical (`1`).

```cpp
class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> res;
        vector<pair<int, int>> directions = {{0, 1}, {1, 0},
                                             {0, -1}, {-1, 0}};
        vector<int> steps = {matrix[0].size(), matrix.size() - 1};

        int r = 0, c = -1, d = 0;
        while (steps[d % 2]) {
            for (int i = 0; i < steps[d % 2]; i++) {
                r += directions[d].first;
                c += directions[d].second;
                res.push_back(matrix[r][c]);
            }
            steps[d % 2]--;
            d = (d + 1) % 4;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(m * n)$ space for the output list.

> Where $m$ is the number of rows and $n$ is the number of columns.

## Standalone solution file (`cpp/0054-spiral-matrix.cpp` in the NeetCode repo)

```cpp
/*
    Given a matrix, return all elements in spiral order

    Set up boundaries, go outside in CW: top->right->bottom->left

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        int left = 0;
        int top = 0;
        int right = matrix[0].size() - 1;
        int bottom = matrix.size() - 1;
        
        vector<int> result;
        
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) {
                result.push_back(matrix[top][j]);
            }
            top++;
            
            for (int i = top; i <= bottom; i++) {
                result.push_back(matrix[i][right]);
            }
            right--;
            
            if (top <= bottom) {
                for (int j = right; j >= left; j--) {
                    result.push_back(matrix[bottom][j]);
                }
            }
            bottom--;
            
            if (left <= right) {
                for (int i = bottom; i >= top; i--) {
                    result.push_back(matrix[i][left]);
                }
            }
            left++;
        }
        
        return result;
    }
};
```
