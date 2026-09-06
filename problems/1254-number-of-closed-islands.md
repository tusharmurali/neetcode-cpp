# 1254. Number of Closed Islands

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-closed-islands/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-closed-islands>  
- **Video:** <https://www.youtube.com/watch?v=X8k48xek8g8>  

[← Back to index](../INDEX.md)

## 1. Depth First Search - I

A closed island is a group of land cells (`0`s) that is completely surrounded by water (`1`s) and does not touch the grid boundary. The key observation is that any island touching the boundary cannot be closed. We use `dfs` to explore each island, and during exploration, if we ever go out of bounds, we know this island is not closed. We return a boolean indicating whether the entire island stayed within bounds.

```cpp
class Solution {
    int ROWS, COLS;
    vector<vector<int>> directions;
    vector<vector<bool>> visit;

public:
    int closedIsland(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();
        directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        visit.assign(ROWS, vector<bool>(COLS, false));

        int res = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 0 && !visit[r][c]) {
                    if (dfs(grid, r, c)) {
                        res++;
                    }
                }
            }
        }
        return res;
    }

private:
    bool dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r == ROWS || c == COLS) {
            return false;
        }
        if (grid[r][c] == 1 || visit[r][c]) {
            return true;
        }

        visit[r][c] = true;
        bool res = true;
        for (auto& d : directions) {
            if (!dfs(grid, r + d[0], c + d[1])) {
                res = false;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.

## 2. Depth First Search - II

Instead of tracking whether each island is closed during `dfs`, we can first eliminate all islands that touch the boundary. By running `dfs` from every boundary land cell and marking those cells as water, we effectively remove all non-closed islands. After this preprocessing, any remaining land cells must belong to closed islands, so we simply count them.

```cpp
class Solution {
    const int directions[5] = {0, 1, 0, -1, 0};
    int ROWS, COLS;

public:
    int closedIsland(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();

        for (int r = 0; r < ROWS; r++) {
            dfs(grid, r, 0);
            dfs(grid, r, COLS - 1);
        }
        for (int c = 0; c < COLS; c++) {
            dfs(grid, 0, c);
            dfs(grid, ROWS - 1, c);
        }

        int res = 0;
        for (int r = 1; r < ROWS - 1; r++) {
            for (int c = 1; c < COLS - 1; c++) {
                if (grid[r][c] == 0) {
                    dfs(grid, r, c);
                    res++;
                }
            }
        }
        return res;
    }

private:
    void dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= ROWS || c >= COLS || grid[r][c] == 1) {
            return;
        }
        grid[r][c] = 1;
        for (int d = 0; d < 4; d++) {
            dfs(grid, r + directions[d], c + directions[d + 1]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.

## 3. Breadth First Search

BFS provides an iterative alternative to `dfs` for exploring islands. Starting from a land cell, we use a queue to visit all connected land cells level by level. While exploring, if any neighbor would take us out of bounds, we know the island is not closed. We track this with a flag and only count the island if it never touched the boundary.

```cpp
class Solution {
    int directions[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    int ROWS, COLS;
    vector<vector<bool>> visit;

public:
    int closedIsland(vector<vector<int>>& grid) {
        ROWS = grid.size();
        COLS = grid[0].size();
        visit.assign(ROWS, vector<bool>(COLS, false));
        int res = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 0 && !visit[r][c]) {
                    if (bfs(grid, r, c)) res++;
                }
            }
        }
        return res;
    }

private:
    bool bfs(vector<vector<int>>& grid, int r, int c) {
        queue<pair<int, int>> q;
        q.push({r, c});
        visit[r][c] = true;
        bool isClosed = true;

        while (!q.empty()) {
            auto [x, y] = q.front();q.pop();
            for (auto& d : directions) {
                int nx = x + d[0], ny = y + d[1];
                if (nx < 0 || ny < 0 || nx >= ROWS || ny >= COLS) {
                    isClosed = false;
                    continue;
                }
                if (grid[nx][ny] == 1 || visit[nx][ny]) continue;
                visit[nx][ny] = true;
                q.push({nx, ny});
            }
        }
        return isClosed;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.

## 4. Disjoint Set Union

We can model this problem using Union-Find (DSU). Each land cell belongs to a component, and we union adjacent land cells together. The trick is to also create a virtual "boundary" node. Whenever a land cell is on the boundary or adjacent to the grid edge, we union it with this boundary node. After processing, any land component that shares the same root as the boundary node is not closed. We count components whose root differs from the boundary node's root.

```cpp
class DSU {
public:
    vector<int> Parent, Size;

    DSU(int n) {
        Parent.resize(n + 1);
        Size.resize(n + 1, 1);
        for (int i = 0; i <= n; i++) {
            Parent[i] = i;
        }
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionSets(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (Size[pu] >= Size[pv]) {
            Size[pu] += Size[pv];
            Parent[pv] = pu;
        } else {
            Size[pv] += Size[pu];
            Parent[pu] = pv;
        }
        return true;
    }
};

class Solution {
public:
    int closedIsland(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int N = ROWS * COLS;

        DSU dsu(N);
        int directions[5] = {0, 1, 0, -1, 0};

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 0) {
                    for (int d = 0; d < 4; d++) {
                        int nr = r + directions[d], nc = c + directions[d + 1];
                        if (nr < 0 || nc < 0 || nr == ROWS || nc == COLS) {
                            dsu.unionSets(N, r * COLS + c);
                        } else if (grid[nr][nc] == 0) {
                            dsu.unionSets(r * COLS + c, nr * COLS + nc);
                        }
                    }
                }
            }
        }

        int res = 0, rootN = dsu.find(N);
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 0) {
                    int node = r * COLS + c;
                    int root = dsu.find(node);
                    if (root == node && root != rootN) {
                        res++;
                    }
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

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.
