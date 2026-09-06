# 63. Unique Paths II

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/unique-paths-ii/>  
- **NeetCode:** <https://neetcode.io/problems/unique-paths-ii>  
- **Video:** <https://www.youtube.com/watch?v=d3UOz7zdE4I>  
- **Video approach:** 3. Dynamic Programming (Space Optimized)  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We want to count all possible paths from the top-left corner to the bottom-right corner, but some cells are blocked by obstacles. At any cell, we can only move right or down. This naturally leads to a recursive approach: the number of paths from a cell equals the sum of paths from the cell below and the cell to the right. If we hit an obstacle or go out of bounds, that path contributes `0`. Since many subproblems overlap (the same cell gets visited through different routes), we use memoization to avoid redundant calculations.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int uniquePathsWithObstacles(vector<vector<int>>& grid) {
        int M = grid.size(), N = grid[0].size();
        dp.resize(M, vector<int>(N, -1));
        return dfs(0, 0, grid, M, N);
    }

private:
    int dfs(int r, int c, vector<vector<int>>& grid, int M, int N) {
        if (r == M || c == N || grid[r][c] == 1) {
            return 0;
        }
        if (r == M - 1 && c == N - 1) {
            return 1;
        }
        if (dp[r][c] != -1) {
            return dp[r][c];
        }
        dp[r][c] = dfs(r + 1, c, grid, M, N) + dfs(r, c + 1, grid, M, N);
        return dp[r][c];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Dynamic Programming (Bottom-Up)

Instead of solving recursively from the start, we can build the solution iteratively from the destination back to the start. Each cell stores the number of ways to reach the destination from that cell. For any cell, this count is the sum of the counts from the cell below and the cell to the right. Obstacles simply have a count of `0` since no path can go through them.

```cpp
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& grid) {
        int M = grid.size(), N = grid[0].size();
        if (grid[0][0] == 1 || grid[M - 1][N - 1] == 1) {
            return 0;
        }

        vector<vector<uint>> dp(M + 1, vector<uint>(N + 1, 0));
        dp[M - 1][N - 1] = 1;

        for (int r = M - 1; r >= 0; r--) {
            for (int c = N - 1; c >= 0; c--) {
                if (grid[r][c] == 1) {
                    dp[r][c] = 0;
                } else {
                    dp[r][c] += dp[r + 1][c];
                    dp[r][c] += dp[r][c + 1];
                }
            }
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Dynamic Programming (Space Optimized) ▶ video

Looking at the bottom-up approach, we notice that each cell only depends on the cell directly below it and the cell to its right. Since we process row by row from bottom to top, we only need to keep track of one row at a time. The value `dp[c]` before updating represents the count from the row below, and `dp[c+1]` after updating represents the count from the right. This reduces space from `O(m * n)` to `O(n)`.

```cpp
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& grid) {
        int M = grid.size(), N = grid[0].size();
        vector<uint> dp(N + 1, 0);
        dp[N - 1] = 1;

        for (int r = M - 1; r >= 0; r--) {
            for (int c = N - 1; c >= 0; c--) {
                if (grid[r][c] == 1) {
                    dp[c] = 0;
                } else {
                    dp[c] += dp[c + 1];
                }
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 4. Dynamic Programming (In-Place)

We can avoid using any extra space by reusing the input grid itself to store the path counts. The key insight is that once we process a cell, we no longer need its original value (which was just `0` or `1` for obstacle). We transform `grid` so each cell holds the number of paths from that cell to the destination. Obstacles get converted to `0` since no path passes through them.

```cpp
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& grid) {
        int M = grid.size(), N = grid[0].size();
        if (grid[0][0] == 1 || grid[M - 1][N - 1] == 1) {
            return 0;
        }

        grid[M - 1][N - 1] = 1;

        for (int r = M - 1; r >= 0; r--) {
            for (int c = N - 1; c >= 0; c--) {
                if (r == M - 1 && c == N - 1) {
                    continue;
                }

                if (grid[r][c] == 1) {
                    grid[r][c] = 0;
                } else {
                    uint down = (r + 1 < M) ? grid[r + 1][c] : 0;
                    uint right = (c + 1 < N) ? grid[r][c + 1] : 0;
                    grid[r][c] = down + right;
                }
            }
        }

        return grid[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns.

## Standalone solution file (`cpp/0063-unique-paths-ii.cpp` in the NeetCode repo)

```cpp
/*

Given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]).
The robot can only move either down or right at any point in time. An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

Example. obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
	 There is one obstacle in the middle of the 3x3 grid above.
	 There are two ways to reach the bottom-right corner:
         1. Right -> Right -> Down -> Down
         2. Down -> Down -> Right -> Right
	 So, the number of unique paths the robot can take is 2. Hence we return 2 as our answer.


Time: O(m * n)
Space: O(n)

*/


class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& grid) {

        int m = grid.size(), n = grid[0].size();
        if(grid[m-1][n-1] == 1 || grid[0][0] == 1) return 0;
        vector<long long> dp(n);
        dp[n-1] = 1;
        for(int i=m-1; i>=0; i--) {
            for(int j=n-1; j>=0; j--) {
                if(grid[i][j] == 1) dp[j] = 0;
                else if(j == n-1) continue;
                else dp[j] = dp[j] + dp[j+1];
            }
        }
        return dp[0];

    }
};
```
