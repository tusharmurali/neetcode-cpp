# 329. Longest Increasing Path In a Matrix

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-increasing-path-in-a-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/longest-increasing-path-in-matrix>  
- **Video:** <https://www.youtube.com/watch?v=wCc_nd-GiEc>  
- **Video approach:** 2. Dynamic Programming (Top-Down)  

[← Back to index](../INDEX.md)

## 1. Recursion

We need the length of the longest path in the matrix where values strictly increase at every step. From any cell, we can move up, down, left, or right.

A natural way to solve this is to try starting from every cell and explore all increasing paths using DFS.
For a given cell, we keep walking to neighboring cells only if the next value is greater than the current one.

The recursive function represents:
**"What is the longest increasing path starting from cell `(r, c)`, given that the previous value was `prevVal`?"**

If the move goes out of bounds or the next value is not strictly larger than `prevVal`, that path ends.

```cpp
class Solution {
public:
    vector<vector<int>> directions = {{-1, 0}, {1, 0},
                                      {0, -1}, {0, 1}};

    int dfs(vector<vector<int>>& matrix, int r, int c, int prevVal) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        if (r < 0 || r >= ROWS || c < 0 ||
            c >= COLS || matrix[r][c] <= prevVal)
            return 0;

        int res = 1;
        for (auto d : directions)
            res = max(res, 1 + dfs(matrix, r + d[0],
                                   c + d[1], matrix[r][c]));
        return res;
    }

    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size(), LIP = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                LIP = max(LIP, dfs(matrix, r, c, INT_MIN));
            }
        }
        return LIP;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * 4 ^ {m * n})$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given $matrix$.

## 2. Dynamic Programming (Top-Down) ▶ video

We want the length of the longest path in a grid where every move goes to a **strictly larger** value, and we can move in 4 directions (up, down, left, right).

A plain `dfs` tries many paths repeatedly. The key improvement is to notice this:

**If we start from the same cell `(r, c)`, the best (longest) increasing path from that cell is always the same.**

So instead of recomputing it again and again, we store it in a cache (`dp`).

The recursive function is still `dfs`, but now it represents:
**"What is the longest increasing path starting from cell `(r, c)`?"**

We only move to neighbors that have a larger value than the current cell, and we memoize the result for each cell.

```cpp
class Solution {
public:
    vector<vector<int>> directions = {{-1, 0}, {1, 0},
                                      {0, -1}, {0, 1}};
    vector<vector<int>> dp;

    int dfs(vector<vector<int>>& matrix, int r, int c, int prevVal) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        if (r < 0 || r >= ROWS || c < 0 ||
            c >= COLS || matrix[r][c] <= prevVal) {
            return 0;
        }
        if (dp[r][c] != -1) return dp[r][c];

        int res = 1;
        for (vector<int> d : directions) {
            res = max(res, 1 + dfs(matrix, r + d[0],
                               c + d[1], matrix[r][c]));
        }
        dp[r][c] = res;
        return res;
    }

    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        dp = vector<vector<int>>(ROWS, vector<int>(COLS, -1));
        int LIP = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                LIP = max(LIP, dfs(matrix, r, c, INT_MIN));
            }
        }
        return LIP;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given $matrix$.

## 3. Topological Sort (Kahn's Algorithm)

We can think of the matrix as a directed graph:

- each cell is a node
- we draw a directed edge from a smaller value to a larger value (only for 4-direction neighbors)

Because edges always go from smaller to larger, the graph has **no cycles** (values must strictly increase), so it is a **DAG**.

In a DAG, the longest path length can be found using **topological order**.  
Kahn’s algorithm (BFS with indegrees) processes nodes level by level:

- nodes with indegree `0` are the “smallest” starting points (no smaller neighbor points into them)
- removing one layer may unlock the next larger layer

Each BFS layer corresponds to taking **one step forward** in an increasing path.  
So, the number of layers processed is exactly the length of the longest increasing path.

```cpp
class Solution {
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        vector<vector<int>> indegree(ROWS, vector<int>(COLS, 0));
        vector<vector<int>> directions = {{-1, 0}, {1, 0},
                                          {0, -1}, {0, 1}};

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                for (auto& d : directions) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < ROWS && nc >= 0 &&
                        nc < COLS && matrix[nr][nc] < matrix[r][c]) {
                        indegree[r][c]++;
                    }
                }
            }
        }

        queue<pair<int, int>> q;
        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                if (indegree[r][c] == 0) {
                    q.push({r, c});
                }
            }
        }

        int LIS = 0;
        while (!q.empty()) {
            int size = q.size();
            for (int i = 0; i < size; ++i) {
                auto [r, c] = q.front();
                q.pop();
                for (auto& d : directions) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < ROWS && nc >= 0 &&
                        nc < COLS && matrix[nr][nc] > matrix[r][c]) {
                        if (--indegree[nr][nc] == 0) {
                            q.push({nr, nc});
                        }
                    }
                }
            }
            LIS++;
        }
        return LIS;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given $matrix$.

## Standalone solution file (`cpp/0329-longest-increasing-path-in-a-matrix.cpp` in the NeetCode repo)

```cpp
/*
    Given matrix, return length of longest increasing path
    Ex. matrix = [[9,9,4],[6,6,8],[2,1,1]] -> 4, [1,2,6,9]

    DFS + memo, cache on indices, compare to prev for increasing check

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int m = matrix.size();
        int n = matrix[0].size();
        
        int result = 0;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                result = max(result, dfs(matrix, -1, i, j, m, n));
            }
        }
        
        return result;
    }
private:
    // {(i, j) -> longest increasing path at (i, j)}
    map<pair<int, int>, int> dp;
    
    int dfs(vector<vector<int>>& matrix, int prev, int i, int j, int m, int n) {
        if (i < 0 || i >= m || j < 0 || j >= n || matrix[i][j] <= prev) {
            return 0;
        }
        if (dp.find({i, j}) != dp.end()) {
            return dp[{i, j}];
        }
        
        int result = 1;
        result = max(result, 1 + dfs(matrix, matrix[i][j], i - 1, j, m, n));
        result = max(result, 1 + dfs(matrix, matrix[i][j], i + 1, j, m, n));
        result = max(result, 1 + dfs(matrix, matrix[i][j], i, j - 1, m, n));
        result = max(result, 1 + dfs(matrix, matrix[i][j], i, j + 1, m, n));
        dp[{i, j}] = result;
        
        return dp[{i, j}];
    }
};
```
