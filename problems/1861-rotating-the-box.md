# 1861. Rotating the Box

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/rotating-the-box/>  
- **NeetCode:** <https://neetcode.io/problems/rotating-the-box>  
- **Video:** <https://www.youtube.com/watch?v=LZr1w0LVzFw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

When the `box` is rotated 90 degrees clockwise, gravity pulls stones downward in the new orientation. Before rotation, rows become columns, so stones in each row should fall to the right (toward the end of the row). We simulate gravity by moving each stone as far right as possible until it hits another stone, an obstacle, or the boundary. After simulating gravity, we perform the rotation by transposing and reversing the row order.

```cpp
class Solution {
public:
    vector<vector<char>> rotateTheBox(vector<vector<char>>& boxGrid) {
        int ROWS = boxGrid.size(), COLS = boxGrid[0].size();

        for (int r = ROWS - 1; r >= 0; r--) {
            for (int c1 = COLS - 1; c1 >= 0; c1--) {
                if (boxGrid[r][c1] == '#') {
                    int c2 = c1 + 1;
                    while (c2 < COLS && boxGrid[r][c2] == '.') {
                        c2++;
                    }
                    boxGrid[r][c1] = '.';
                    boxGrid[r][c2 - 1] = '#';
                }
            }
        }

        vector<vector<char>> res(COLS, vector<char>(ROWS));
        for (int c = 0; c < COLS; c++) {
            for (int r = ROWS - 1; r >= 0; r--) {
                res[c][ROWS - 1 - r] = boxGrid[r][c];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ 2)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Two Pointers - I

Instead of scanning rightward for each stone, we can use a two-pointer technique. Maintain a pointer `i` that tracks the rightmost available position for a stone. Scan from right to left: when we see a stone, swap it with position `i` and decrement `i`. When we see an obstacle, reset `i` to just before the obstacle. This avoids redundant scanning and processes each cell at most twice.

```cpp
class Solution {
public:
    vector<vector<char>> rotateTheBox(vector<vector<char>>& boxGrid) {
        int ROWS = boxGrid.size(), COLS = boxGrid[0].size();
        for (int r = 0; r < ROWS; ++r) {
            int i = COLS - 1;
            for (int c = COLS - 1; c >= 0; --c) {
                if (boxGrid[r][c] == '#') {
                    swap(boxGrid[r][c], boxGrid[r][i]);
                    i--;
                } else if (boxGrid[r][c] == '*') {
                    i = c - 1;
                }
            }
        }
        vector<vector<char>> res(COLS, vector<char>(ROWS));
        for (int c = 0; c < COLS; ++c) {
            for (int r = ROWS - 1; r >= 0; --r) {
                res[c][ROWS - 1 - r] = boxGrid[r][c];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Two Pointers - II

We can combine the gravity simulation and rotation into a single pass. Instead of modifying the original `grid` and then rotating, we directly write stones and obstacles to their final positions in the rotated result `grid`. This eliminates the need to modify the input and performs both operations simultaneously.

```cpp
class Solution {
public:
    vector<vector<char>> rotateTheBox(vector<vector<char>>& boxGrid) {
        int ROWS = boxGrid.size(), COLS = boxGrid[0].size();
        vector<vector<char>> res(COLS, vector<char>(ROWS, '.'));
        for (int r = 0; r < ROWS; ++r) {
            int i = COLS - 1;
            for (int c = COLS - 1; c >= 0; --c) {
                if (boxGrid[r][c] == '#') {
                    res[i][ROWS - r - 1] = '#';
                    --i;
                } else if (boxGrid[r][c] == '*') {
                    res[c][ROWS - r - 1] = '*';
                    i = c - 1;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.
