# 286. Walls And Gates

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/walls-and-gates/>  
- **NeetCode:** <https://neetcode.io/problems/islands-and-treasure>  
- **Video:** <https://www.youtube.com/watch?v=e69C6xhiSQE>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Backtracking)

For every empty cell (`INF`), we try to **find the shortest path to any treasure (`0`)** by exploring all 4 directions using backtracking DFS.

- DFS explores **all possible paths** from the cell until it hits a treasure (distance `0`), a wall (`-1`), or goes out of bounds.
- We use a `visited` grid so the current path doesn't revisit cells (prevents infinite loops in cycles).
- The answer for that cell is the **minimum** distance found among all DFS paths.

This works but is slow because we repeat DFS from many cells and re-explore the same areas again and again.

```cpp
class Solution {
public:
    vector<vector<int>> directions = {{1, 0}, {-1, 0},
                                      {0, 1}, {0, -1}};
    int INF = 2147483647;
    vector<vector<bool>> visit;
    int ROWS, COLS;

    int dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= ROWS ||
            c >= COLS || grid[r][c] == -1 || visit[r][c]) {
            return INF;
        }
        if (grid[r][c] == 0) {
            return 0;
        }
        visit[r][c] = true;
        int res = INF;
        for (auto& dir : directions) {
            int cur = dfs(grid, r + dir[0], c + dir[1]);
            if (cur != INF) {
                res = min(res, 1 + cur);
            }
        }
        visit[r][c] = false;
        return res;
    }

    void islandsAndTreasure(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();
        visit.assign(ROWS, vector<bool>(COLS, false));

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                if (grid[r][c] == INF) {
                    grid[r][c] = dfs(grid, r, c);
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n * 4 ^ {m * n})$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## 2. Breadth First Search

BFS is perfect for **shortest path in an unweighted grid**.
From one empty cell (`INF`), we expand level-by-level (distance `0`, `1`, `2`, ...). The **first time** we reach a treasure cell (`0`), we are guaranteed that distance is the **minimum steps** needed.

This approach runs a BFS **separately for every `INF` cell**, so it's simpler to think about, but can still be slow because many BFS runs repeat the same work.

```cpp
class Solution {
public:
    int ROWS, COLS;
    vector<vector<int>> directions = {{1, 0}, {-1, 0},
                                      {0, 1}, {0, -1}};
    int INF = INT_MAX;

    int bfs(vector<vector<int>>& grid, int r, int c) {
        queue<pair<int, int>> q;
        q.push({r, c});
        vector<vector<bool>> visit(ROWS, vector<bool>(COLS, false));
        visit[r][c] = true;
        int steps = 0;

        while (!q.empty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                auto [row, col] = q.front();
                q.pop();
                if (grid[row][col] == 0) return steps;
                for (auto& dir : directions) {
                    int nr = row + dir[0], nc = col + dir[1];
                    if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS &&
                        !visit[nr][nc] && grid[nr][nc] != -1) {
                        visit[nr][nc] = true;
                        q.push({nr, nc});
                    }
                }
            }
            steps++;
        }
        return INF;
    }

    void islandsAndTreasure(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == INF) {
                    grid[r][c] = bfs(grid, r, c);
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O((m * n) ^ 2)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## 3. Multi Source BFS

Instead of running BFS from **every empty room**, run BFS **once** starting from **all treasures (`0` cells) at the same time**.

Why this works:

- BFS spreads out in "waves" of distance `0`, `1`, `2`, ...
- If we start the queue with **all treasures**, the first time the wave reaches an empty cell, it must be from the **closest treasure** (because BFS guarantees the first visit is the shortest distance in an unweighted grid).
  So each cell gets filled with its minimum distance to **any** treasure.

This avoids repeated work and is the optimal approach.

```cpp
class Solution {
public:
    void islandsAndTreasure(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();

        queue<pair<int, int>> q;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 0) {
                    q.push({i, j});
                }
            }
        }

        vector<vector<int>> dirs = {{-1, 0}, {1, 0},
                                    {0, -1}, {0, 1}};
        while (!q.empty()) {
            int row = q.front().first;
            int col = q.front().second;
            q.pop();

            for (int i = 0; i < 4; i++) {
                int r = row + dirs[i][0];
                int c = col + dirs[i][1];

                if (r < 0 || r >= m || c < 0 ||
                    c >= n || grid[r][c] != INT_MAX) {
                    continue;
                }

                grid[r][c] = grid[row][col] + 1;
                q.push({r, c});
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## Standalone solution file (`cpp/0286-walls-and-gates.cpp` in the NeetCode repo)

```cpp
/*
    Given grid: -1 wall, 0 gate, INF empty, fill each empty w/ dist to nearest gate

    BFS traversal, shortest path from each gate to all empty rooms
    Each gate only looks at within 1 space, then next gate, guarantees shortest

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    void wallsAndGates(vector<vector<int>>& rooms) {
        int m = rooms.size();
        int n = rooms[0].size();
        
        queue<pair<int, int>> q;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (rooms[i][j] == 0) {
                    q.push({i, j});
                }
            }
        }
        
        while (!q.empty()) {
            int row = q.front().first;
            int col = q.front().second;
            q.pop();
            
            for (int i = 0; i < 4; i++) {
                int x = row + dirs[i][0];
                int y = col + dirs[i][1];
                
                if (x < 0 || x >= m || y < 0 || y >= n || rooms[x][y] != INT_MAX) {
                    continue;
                }
                
                rooms[x][y] = rooms[row][col] + 1;
                q.push({x, y});
            }
        }
    }
private:
    vector<vector<int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
};
```
