# 1463. Cherry Pickup II

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/cherry-pickup-ii/>  
- **NeetCode:** <https://neetcode.io/problems/cherry-pickup-ii>  
- **Video:** <https://www.youtube.com/watch?v=c1stwk2TbNk>  

[← Back to index](../INDEX.md)

## 1. Recursion

Two robots start at the top corners of the grid and move down simultaneously, one row at a time. At each row, each robot can move diagonally left, straight down, or diagonally right. We track both robot positions and explore all 9 combinations of moves (3 choices for robot 1 times 3 choices for robot 2). If both robots land on the same cell, we only count the cherries once. We enforce `c1 <= c2` to avoid duplicate states since the robots are interchangeable.

```cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        return dfs(0, 0, COLS - 1, grid, ROWS, COLS);
    }

private:
    int dfs(int r, int c1, int c2, vector<vector<int>>& grid, int ROWS, int COLS) {
        if (c1 < 0 || c2 < 0 || c1 >= COLS || c2 >= COLS || c1 > c2) {
            return 0;
        }
        if (r == ROWS - 1) {
            return grid[r][c1] + (c1 == c2 ? 0 : grid[r][c2]);
        }

        int res = 0;
        for (int c1_d = -1; c1_d <= 1; c1_d++) {
            for (int c2_d = -1; c2_d <= 1; c2_d++) {
                res = max(res, dfs(r + 1, c1 + c1_d, c2 + c2_d, grid, ROWS, COLS));
            }
        }
        return res + grid[r][c1] + (c1 == c2 ? 0 : grid[r][c2]);
    }
};
```

**Complexity**

- Time complexity: $O(m * 9 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

> Where $n$ is the number of rows and $m$ is the number of columns in the grid.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same states multiple times. Since the state is defined by `(r, c1, c2)`, we can use a 3D cache to store results for previously visited states. When we encounter a state we have already solved, we return the cached value instead of recomputing it.

```cpp
class Solution {
    vector<vector<vector<int>>> cache;

public:
    int cherryPickup(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        cache.assign(ROWS, vector<vector<int>>(COLS, vector<int>(COLS, -1)));
        return dfs(0, 0, COLS - 1, grid);
    }

private:
    int dfs(int r, int c1, int c2, vector<vector<int>>& grid) {
        if (min(c1, c2) < 0 || max(c1, c2) >= grid[0].size()) {
            return 0;
        }
        if (cache[r][c1][c2] != -1) {
            return cache[r][c1][c2];
        }
        if (r == grid.size() - 1) {
            return cache[r][c1][c2] = grid[r][c1] + (c1 == c2 ? 0 : grid[r][c2]);
        }

        int res = 0;
        for (int c1_d = -1; c1_d <= 1; c1_d++) {
            for (int c2_d = -1; c2_d <= 1; c2_d++) {
                res = max(res, dfs(r + 1, c1 + c1_d, c2 + c2_d, grid));
            }
        }
        return cache[r][c1][c2] = res + grid[r][c1] + (c1 == c2 ? 0 : grid[r][c2]);
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(n * m ^ 2)$

> Where $n$ is the number of rows and $m$ is the number of columns in the grid.

## 3. Dynamic Programming (Bottom-Up)

Instead of using recursion with memoization, we can build the solution iteratively from the bottom row up. For each cell combination at row `r`, we look at all possible transitions from row `r+1` and take the maximum. This eliminates recursion overhead and makes the computation order explicit.

```cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int dp[ROWS][COLS][COLS];

        for (int r = ROWS - 1; r >= 0; r--) {
            for (int c1 = 0; c1 < COLS; c1++) {
                for (int c2 = 0; c2 < COLS; c2++) {
                    int res = grid[r][c1];
                    if (c1 != c2) {
                        res += grid[r][c2];
                    }

                    if (r != ROWS - 1) {
                        int maxCherries = 0;
                        for (int d1 = -1; d1 <= 1; d1++) {
                            for (int d2 = -1; d2 <= 1; d2++) {
                                int nc1 = c1 + d1, nc2 = c2 + d2;
                                if (nc1 >= 0 && nc1 < COLS && nc2 >= 0 && nc2 < COLS) {
                                    maxCherries = max(maxCherries, dp[r + 1][nc1][nc2]);
                                }
                            }
                        }
                        res += maxCherries;
                    }

                    dp[r][c1][c2] = res;
                }
            }
        }

        return dp[0][0][COLS - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(n * m ^ 2)$

> Where $n$ is the number of rows and $m$ is the number of columns in the grid.

## 4. Dynamic Programming (Space Optimized)

Since each row's computation only depends on the row below it, we do not need to store the entire 3D array. We can use two 2D arrays: one for the current row and one for the previous row (the row below). After processing each row, we swap them. This reduces space complexity from `O(n * m^2)` to `O(m^2)`.

```cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        vector<vector<int>> dp(COLS, vector<int>(COLS, 0));

        for (int r = ROWS - 1; r >= 0; r--) {
            vector<vector<int>> cur_dp(COLS, vector<int>(COLS, 0));
            for (int c1 = 0; c1 < COLS; c1++) {
                for (int c2 = c1; c2 < COLS; c2++) {
                    int maxCherries = 0;
                    int cherries = grid[r][c1] + (c1 == c2 ? 0 : grid[r][c2]);
                    for (int d1 = -1; d1 <= 1; d1++) {
                        for (int d2 = -1; d2 <= 1; d2++) {
                            int nc1 = c1 + d1, nc2 = c2 + d2;
                            if (nc1 >= 0 && nc1 < COLS && nc2 >= 0 && nc2 < COLS) {
                                maxCherries = max(maxCherries, cherries + dp[nc1][nc2]);
                            }
                        }
                    }
                    cur_dp[c1][c2] = maxCherries;
                }
            }
            dp = cur_dp;
        }
        return dp[0][COLS - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(m ^ 2)$

> Where $n$ is the number of rows and $m$ is the number of columns in the grid.

## Standalone solution file (`cpp/1463-cherry-pickup-ii.cpp` in the NeetCode repo)

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();

        vector<vector<vector<int>>> dp(rows, vector<vector<int>>(cols, vector<int>(cols, 0)));

        for (int i = rows - 1; i >= 0; --i) {
            for (int j = 0; j < cols; ++j) {
                for (int k = 0; k < cols; ++k) {
                    int cherries = grid[i][j] + (j != k ? grid[i][k] : 0);
                    if (i == rows - 1) {
                        dp[i][j][k] = cherries;
                    } else {
                        int maxCherries = 0;
                        for (int dj = -1; dj <= 1; ++dj) {
                            for (int dk = -1; dk <= 1; ++dk) {
                                int nj = j + dj;
                                int nk = k + dk;
                                if (nj >= 0 && nj < cols && nk >= 0 && nk < cols) {
                                    maxCherries = max(maxCherries, dp[i + 1][nj][nk]);
                                }
                            }
                        }
                        dp[i][j][k] = cherries + maxCherries;
                    }
                }
            }
        }
        
        return dp[0][0][cols - 1];
    }
};
```
