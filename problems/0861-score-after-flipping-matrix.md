# 861. Score After Flipping Matrix

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/score-after-flipping-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/score-after-flipping-matrix>  
- **Video:** <https://www.youtube.com/watch?v=FbhzRA5den8>  

[← Back to index](../INDEX.md)

## 1. Greedy (Overwriting the Input)

Each row represents a binary number, and higher-order bits contribute more to the total score. The leftmost bit has the highest value, so we want it to be 1 in every row. First, flip any row where the first bit is 0. After that, for each column, we want to maximize the number of 1s. If a column has more 0s than 1s, flip it. This greedy strategy ensures we maximize the score by prioritizing high-value bits.

```cpp
class Solution {
public:
    int matrixScore(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();

        for (int r = 0; r < ROWS; r++) {
            if (grid[r][0] == 0) {
                for (int c = 0; c < COLS; c++) {
                    grid[r][c] ^= 1;
                }
            }
        }

        for (int c = 0; c < COLS; c++) {
            int oneCnt = 0;
            for (int r = 0; r < ROWS; r++) {
                oneCnt += grid[r][c];
            }
            if (oneCnt < ROWS - oneCnt) {
                for (int r = 0; r < ROWS; r++) {
                    grid[r][c] ^= 1;
                }
            }
        }

        int res = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                res += grid[r][c] << (COLS - c - 1);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Greedy (Optimal)

We can compute the score without modifying the grid. After row flips to ensure all first bits are 1, we know every row contributes `2^(COLS - 1)` from the first column. For other columns, instead of tracking the actual values, we count how many cells would be 1 after both row and column optimizations. A cell is effectively 1 if it differs from the first cell in its row (since the first cell becomes 1 after row flip). We then take the maximum of this count and its complement for each column.

```cpp
class Solution {
public:
    int matrixScore(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int res = ROWS * (1 << (COLS - 1));

        for (int c = 1; c < COLS; c++) {
            int cnt = 0;
            for (int r = 0; r < ROWS; r++) {
                if (grid[r][c] != grid[r][0]) {
                    cnt++;
                }
            }
            cnt = max(cnt, ROWS - cnt);
            res += cnt * (1 << (COLS - c - 1));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns.
