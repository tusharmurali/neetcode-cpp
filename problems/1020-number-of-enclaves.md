# 1020. Number of Enclaves

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-enclaves/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-enclaves>  
- **Video:** <https://www.youtube.com/watch?v=gf0zsh1FIgE>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

An enclave is a land cell that cannot reach the grid boundary by walking only on land. Any land cell connected to the boundary can eventually "walk off" the grid, so it is not an enclave. Our strategy is to count total land cells, then subtract those connected to the boundary. We find boundary-connected land by starting `dfs` from every land cell on the boundary and counting all reachable land cells.

```cpp
class Solution {
public:
    int ROWS, COLS;
    vector<vector<bool>> visit;
    vector<vector<int>> direct = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    int numEnclaves(vector<vector<int>>& grid) {
        this->ROWS = grid.size();
        this->COLS = grid[0].size();
        this->visit = vector<vector<bool>>(ROWS, vector<bool>(COLS, false));

        int land = 0, borderLand = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                land += grid[r][c];
                if (grid[r][c] == 1 && !visit[r][c] &&
                    (r == 0 || r == ROWS - 1 || c == 0 || c == COLS - 1)) {
                    borderLand += dfs(r, c, grid);
                }
            }
        }
        return land - borderLand;
    }

private:
    int dfs(int r, int c, vector<vector<int>>& grid) {
        if (r < 0 || c < 0 || r == ROWS || c == COLS ||
            grid[r][c] == 0 || visit[r][c]) {
            return 0;
        }
        visit[r][c] = true;
        int res = 1;
        for (auto& d : direct) {
            res += dfs(r + d[0], c + d[1], grid);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.

## 2. Breadth First Search

`bfs` offers an iterative approach to the same problem. Instead of recursive `dfs`, we use a queue to explore boundary-connected land cells. We first add all boundary land cells to the queue, then process them level by level, marking visited cells. After `bfs` completes, we have counted all land that can reach the boundary. The remaining land cells are enclaves.

```cpp
class Solution {
public:
    int ROWS, COLS;
    vector<vector<bool>> visit;
    vector<vector<int>> direct = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    int numEnclaves(vector<vector<int>>& grid) {
        this->ROWS = grid.size();
        this->COLS = grid[0].size();
        this->visit = vector<vector<bool>>(ROWS, vector<bool>(COLS, false));

        int land = 0, borderLand = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                land += grid[r][c];
                if (grid[r][c] == 1 && !visit[r][c] &&
                    (r == 0 || r == ROWS - 1 || c == 0 || c == COLS - 1)) {
                    borderLand += dfs(r, c, grid);
                }
            }
        }
        return land - borderLand;
    }

private:
    int dfs(int r, int c, vector<vector<int>>& grid) {
        if (r < 0 || c < 0 || r == ROWS || c == COLS ||
            grid[r][c] == 0 || visit[r][c]) {
            return 0;
        }
        visit[r][c] = true;
        int res = 1;
        for (auto& d : direct) {
            res += dfs(r + d[0], c + d[1], grid);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.

## 3. Disjoint Set Union

Union-Find provides another perspective on this problem. We create a virtual boundary node and union all boundary land cells with it. We also union adjacent land cells together. After processing, the size of the boundary node's component tells us how many land cells can reach the boundary. The answer is total land minus this count (plus 1 to account for the virtual node itself being counted in the size).

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
    int numEnclaves(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int N = ROWS * COLS;
        DSU dsu(N);
        vector<int> directions = {0, 1, 0, -1, 0};
        int land = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 0) continue;
                land++;
                for (int d = 0; d < 4; d++) {
                    int nr = r + directions[d], nc = c + directions[d + 1];
                    if (nr >= 0 && nc >= 0 && nr < ROWS && nc < COLS) {
                        if (grid[nr][nc] == 1) {
                            dsu.unionSets(r * COLS + c, nr * COLS + nc);
                        }
                    } else {
                        dsu.unionSets(N, r * COLS + c);
                    }
                }
            }
        }

        int borderLand = dsu.Size[dsu.find(N)];
        return land - borderLand + 1;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given grid.
