# 576. Out of Boundary Paths

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/out-of-boundary-paths/>  
- **NeetCode:** <https://neetcode.io/problems/out-of-boundary-paths>  
- **Video:** <https://www.youtube.com/watch?v=Bg5CLRqtNmk>  

[← Back to index](../INDEX.md)

## 1. Recursion

We want to count all paths that start from a given cell and eventually move out of the grid, using at most `maxMove` moves. At each cell, we can move in four directions, and each move decrements our remaining moves.

The base cases are: if we step outside the grid, we found one valid path; if we run out of moves while still inside, this path does not count. We recursively explore all four directions and sum up the results.

```cpp
class Solution {
private:
    int MOD = 1'000'000'007;

    int dfs(int r, int c, int moves, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n) return 1;
        if (moves == 0) return 0;

        return (
            (dfs(r + 1, c, moves - 1, m, n) + dfs(r - 1, c, moves - 1, m, n)) % MOD +
            (dfs(r, c + 1, moves - 1, m, n) + dfs(r, c - 1, moves - 1, m, n)) % MOD
        ) % MOD;
    }

public:
    int findPaths(int m, int n, int maxMove, int startRow, int startColumn) {
        return dfs(startRow, startColumn, maxMove, m, n);
    }
};
```

**Complexity**

- Time complexity: $O(4 ^ N)$
- Space complexity: $O(N)$

> Where $m$ is the number of rows, $n$ is the number of columns, and $N$ is the maximum number of allowed moves.

## 2. Dynamic Programming (Top-Down)

The recursive solution has many overlapping subproblems since the same (row, col, moves) state can be reached through different paths. We can use memoization to cache results and avoid redundant computation.

Each state is defined by three parameters: current position (r, c) and remaining moves. Since there are m _ n _ maxMove possible states, memoization reduces the time complexity dramatically.

```cpp
class Solution {
private:
    vector<vector<vector<int>>> dp;
    int MOD = 1'000'000'007;

    int dfs(int r, int c, int moves, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n) return 1;
        if (moves == 0) return 0;
        if (dp[r][c][moves] != -1) return dp[r][c][moves];

        dp[r][c][moves] = (
            (dfs(r + 1, c, moves - 1, m, n) + dfs(r - 1, c, moves - 1, m, n)) % MOD +
            (dfs(r, c + 1, moves - 1, m, n) + dfs(r, c - 1, moves - 1, m, n)) % MOD
        ) % MOD;
        return dp[r][c][moves];
    }

public:
    int findPaths(int m, int n, int maxMove, int startRow, int startColumn) {
        dp = vector<vector<vector<int>>>(m, vector<vector<int>>(n, vector<int>(maxMove + 1, -1)));
        return dfs(startRow, startColumn, maxMove, m, n);
    }
};
```

**Complexity**

- Time complexity: $O(m * n * N)$
- Space complexity: $O(m * n * N)$

> Where $m$ is the number of rows, $n$ is the number of columns, and $N$ is the maximum number of allowed moves.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we can fill the DP table iteratively. We build up from 1 move to maxMove, computing how many ways each cell can reach the boundary with exactly that many moves remaining.

For each cell, we look at its four neighbors. If a neighbor is out of bounds, that contributes 1 path. If the neighbor is valid, we add its value from the previous move count.

```cpp
class Solution {
public:
    int findPaths(int m, int n, int maxMove, int startRow, int startColumn) {
        const int MOD = 1'000'000'007;
        vector<vector<vector<uint>>> dp(m, vector<vector<uint>>(n, vector<uint>(maxMove + 1, 0)));

        for (int moves = 1; moves <= maxMove; moves++) {
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) {
                    dp[r][c][moves] = (
                        (r > 0 ? dp[r - 1][c][moves - 1] : 1) +
                        (r < m - 1 ? dp[r + 1][c][moves - 1] : 1) +
                        (c > 0 ? dp[r][c - 1][moves - 1] : 1) +
                        (c < n - 1 ? dp[r][c + 1][moves - 1] : 1)
                    ) % MOD;
                }
            }
        }

        return dp[startRow][startColumn][maxMove];
    }
};
```

**Complexity**

- Time complexity: $O(m * n * N)$
- Space complexity: $O(m * n * N)$

> Where $m$ is the number of rows, $n$ is the number of columns, and $N$ is the maximum number of allowed moves.

## 4. Dynamic Programming (Space Optimized)

Since each move layer only depends on the previous move layer, we do not need the full 3D array. We can use two 2D arrays: one for the current move count and one for the previous. After processing each move, we swap them.

This reduces space from O(m _ n _ maxMove) to O(m \* n).

```cpp
class Solution {
public:
    int findPaths(int m, int n, int maxMove, int startRow, int startColumn) {
        const int MOD = 1'000'000'007;
        vector<vector<int>> dp(m, vector<int>(n, 0));

        for (int moves = 1; moves <= maxMove; moves++) {
            vector<vector<int>> tmp(m, vector<int>(n, 0));
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) {
                    if (r + 1 == m) {
                        tmp[r][c] = (tmp[r][c] + 1) % MOD;
                    } else {
                        tmp[r][c] = (tmp[r][c] + dp[r + 1][c]) % MOD;
                    }
                    if (r - 1 < 0) {
                        tmp[r][c] = (tmp[r][c] + 1) % MOD;
                    } else {
                        tmp[r][c] = (tmp[r][c] + dp[r - 1][c]) % MOD;
                    }
                    if (c + 1 == n) {
                        tmp[r][c] = (tmp[r][c] + 1) % MOD;
                    } else {
                        tmp[r][c] = (tmp[r][c] + dp[r][c + 1]) % MOD;
                    }
                    if (c - 1 < 0) {
                        tmp[r][c] = (tmp[r][c] + 1) % MOD;
                    } else {
                        tmp[r][c] = (tmp[r][c] + dp[r][c - 1]) % MOD;
                    }
                }
            }
            dp = tmp;
        }

        return dp[startRow][startColumn];
    }
};
```

**Complexity**

- Time complexity: $O(m * n * N)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows, $n$ is the number of columns, and $N$ is the maximum number of allowed moves.
