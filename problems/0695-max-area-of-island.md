# 695. Max Area of Island

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/max-area-of-island/>  
- **NeetCode:** <https://neetcode.io/problems/max-area-of-island>  
- **Video:** <https://www.youtube.com/watch?v=iJGr1OtmH0c>  
- **Video approach:** 1. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search ▶ video

An island is a group of connected `1`s.
To find the **maximum area**, we explore each island fully and count how many cells it contains.

Depth First Search (`dfs`) helps us:

- Start from a land cell
- Visit all connected land cells (up, down, left, right)
- Count the size of that island
- Keep track of the largest size seen

We mark cells as visited so we don't count the same cell twice.

```cpp
class Solution {
    int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int area = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1) {
                    area = max(area, dfs(grid, r, c));
                }
            }
        }

        return area;
    }

    int dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= grid.size() ||
            c >= grid[0].size() || grid[r][c] == 0) {
            return 0;
        }

        grid[r][c] = 0;
        int res = 1;
        for (int i = 0; i < 4; i++) {
            res += dfs(grid, r + directions[i][0],
                             c + directions[i][1]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## 2. Breadth First Search

An island is a group of connected `1`s.
To find the **maximum area**, we explore each island completely and count how many cells it has.

Using **Breadth First Search (`bfs`)**:

- Start from a land cell (`1`)
- Visit all connected land cells level by level
- Count each visited cell as part of the island
- Mark cells as `0` to avoid revisiting
- Track the largest island size found

```cpp
class Solution {
    int directions[4][2] = {{1, 0}, {-1, 0},
                            {0, 1}, {0, -1}};
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int area = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1) {
                    area = max(area, bfs(grid, r, c));
                }
            }
        }

        return area;
    }

    int bfs(vector<vector<int>>& grid, int r, int c) {
        queue<pair<int, int>> q;
        grid[r][c] = 0;
        q.push({r, c});
        int res = 1;

        while (!q.empty()) {
            auto node = q.front();q.pop();
            int row = node.first, col = node.second;
            for (int i = 0; i < 4; i++) {
                int nr = row + directions[i][0];
                int nc = col + directions[i][1];
                if (nr >= 0 && nc >= 0 && nr < grid.size() &&
                    nc < grid[0].size() && grid[nr][nc] == 1) {
                    q.push({nr, nc});
                    grid[nr][nc] = 0;
                    res++;
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

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## 3. Disjoint Set Union

Think of each land cell (`1`) as a node in a graph.  
If two land cells are adjacent (up, down, left, right), they belong to the **same island**.

Using **Disjoint Set Union (Union-Find)**:

- Each land cell starts as its own component
- When two neighboring land cells are found, we **union** them
- The size of a connected component represents the **area of that island**
- Track the maximum component size

This approach is useful when you want to group connected components efficiently.

```cpp
class DSU {
    vector<int> Parent, Size;
public:
    DSU(int n) {
        Parent.resize(n + 1);
        Size.resize(n + 1);
        for (int i = 0; i <= n; i++) {
            Parent[i] = i;
            Size[i] = 1;
        }
    }

    int find(int node) {
        if (node != Parent[node]) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionBySize(int u, int v) {
        int pu = find(u);
        int pv = find(v);
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

    int getSize(int node) {
        return Size[find(node)];
    }
};

class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int ROWS = grid.size();
        int COLS = grid[0].size();
        DSU dsu(ROWS * COLS);

        int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        int area = 0;

        auto index = [&](int r, int c) {
            return r * COLS + c;
        };

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1) {
                    for (auto& d : directions) {
                        int nr = r + d[0];
                        int nc = c + d[1];
                        if (nr >= 0 && nc >= 0 && nr < ROWS &&
                            nc < COLS && grid[nr][nc] == 1) {
                            dsu.unionBySize(index(r, c), index(nr, nc));
                        }
                    }
                    area = max(area, dsu.getSize(index(r, c)));
                }
            }
        }

        return area;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## Standalone solution file (`cpp/0695-max-area-of-island.cpp` in the NeetCode repo)

```cpp
/*
    Given grid where '1' is land & '0' is water, return largest island

    DFS, set visited land to '0' to not visit it again, store biggest

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        
        int result = 0;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    result = max(result, dfs(grid, i, j, m, n));
                }
            }
        }
        
        return result;
    }
private:
    int dfs(vector<vector<int>>& grid, int i, int j, int m, int n) {
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == 0) {
            return 0;
        }
        grid[i][j] = 0;
        
        return 1 + dfs(grid, i - 1, j, m, n) + dfs(grid, i + 1, j, m, n)
            + dfs(grid, i, j - 1, m, n) + dfs(grid, i, j + 1, m, n);
    }
};
```
