# 1219. Path with Maximum Gold

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/path-with-maximum-gold/>  
- **NeetCode:** <https://neetcode.io/problems/path-with-maximum-gold>  
- **Video:** <https://www.youtube.com/watch?v=I1wllM_pozY>  

[← Back to index](../INDEX.md)

## 1. Backtracking (DFS) - I

We want to collect the maximum amount of gold by traversing the grid. Since we can start from any cell containing gold and move in four directions without revisiting cells, this naturally fits a backtracking approach. We try starting from every gold cell and explore all possible paths, keeping track of the maximum gold collected. The key insight is that we need to "undo" our visit after exploring a path so other paths can use that cell.

```cpp
class Solution {
public:
    int ROWS, COLS;
    vector<vector<int>> directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    int getMaximumGold(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();
        int res = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] != 0) {
                    vector<vector<bool>> visit(ROWS, vector<bool>(COLS, false));
                    res = max(res, dfs(grid, r, c, visit));
                }
            }
        }
        return res;
    }

private:
    int dfs(vector<vector<int>>& grid, int r, int c, vector<vector<bool>>& visit) {
        if (r < 0 || c < 0 || r >= ROWS || c >= COLS || grid[r][c] == 0 || visit[r][c]) {
            return 0;
        }

        visit[r][c] = true;
        int res = grid[r][c];

        for (auto& d : directions) {
            res = max(res, grid[r][c] + dfs(grid, r + d[0], c + d[1], visit));
        }

        visit[r][c] = false;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(N * 3 ^ N)$
- Space complexity: $O(N)$

> Where $N$ is the number of cells which contain gold.

## 2. Backtracking (DFS) - II

Instead of using a separate visited set, we can mark cells as visited by temporarily setting them to zero. Since zero represents an empty cell (no gold), the `dfs` will naturally skip it. After exploring all paths from a cell, we restore its original value. This approach saves space and can be slightly faster since we avoid set operations.

```cpp
class Solution {
public:
    int ROWS, COLS;
    vector<vector<int>> directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    int getMaximumGold(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();
        int res = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] != 0) {
                    res = max(res, dfs(grid, r, c));
                }
            }
        }
        return res;
    }

private:
    int dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= ROWS || c >= COLS || grid[r][c] == 0) {
            return 0;
        }

        int gold = grid[r][c];
        grid[r][c] = 0;
        int res = 0;

        for (auto& d : directions) {
            res = max(res, dfs(grid, r + d[0], c + d[1]));
        }

        grid[r][c] = gold;
        return gold + res;
    }
};
```

**Complexity**

- Time complexity: $O(N * 3 ^ N)$
- Space complexity: $O(N)$ for recursion stack.

> Where $N$ is the number of cells which contain gold.

## 3. Backtracking (BFS)

We can also solve this problem using BFS with bitmask state tracking. Each cell containing gold is assigned a unique index, and we use a bitmask to track which cells have been visited along the current path. This allows us to explore all possible paths level by level while ensuring we do not revisit any cell within the same path.

```cpp
class Solution {
public:
    int getMaximumGold(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        vector<vector<int>> index(ROWS, vector<int>(COLS, 0));
        int idx = 0;
        int directions[] = {1, 0, -1, 0, 1};

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] != 0) {
                    index[r][c] = idx++;
                }
            }
        }

        int res = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] > 0) {
                    queue<tuple<int, int, int, int>> q;
                    q.push({r, c, grid[r][c], 1 << index[r][c]});

                    while (!q.empty()) {
                        auto [row, col, gold, mask] = q.front();q.pop();
                        res = max(res, gold);
                        for (int i = 0; i < 4; i++) {
                            int nr = row + directions[i], nc = col + directions[i + 1];
                            if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && grid[nr][nc] > 0) {
                                int newIdx = index[nr][nc];
                                if ((mask & (1 << newIdx)) == 0) {
                                    q.push({nr, nc, gold + grid[nr][nc], mask | (1 << newIdx)});
                                }
                            }
                        }
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(N * 3 ^ N)$
- Space complexity: $O(N)$

> Where $N$ is the number of cells which contain gold.
