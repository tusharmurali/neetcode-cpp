# 934. Shortest Bridge

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shortest-bridge/>  
- **NeetCode:** <https://neetcode.io/problems/shortest-bridge>  
- **Video:** <https://www.youtube.com/watch?v=gkINMhbbIbU>  

[← Back to index](../INDEX.md)

## 1. Depth First Search + Breadth First Search - I

The problem asks for the minimum number of 0s to flip to connect two islands. This is essentially finding the shortest path between the two islands across water.

First, we identify one island completely using DFS and mark all its cells as visited. Then, we use BFS to expand outward from this island. BFS naturally finds the shortest path because it explores all cells at distance 1 before distance 2, and so on. The moment we reach a cell belonging to the second island, we have found the minimum bridge length.

```cpp
class Solution {
public:
    int N;
    vector<vector<bool>> visited;
    vector<vector<int>> direct = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    int shortestBridge(vector<vector<int>>& grid) {
        N = grid.size();
        visited = vector<vector<bool>>(N, vector<bool>(N, false));

        bool found = false;
        for (int r = 0; r < N; r++) {
            if (found) break;
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    dfs(grid, r, c);
                    found = true;
                    break;
                }
            }
        }

        return bfs(grid);
    }

private:
    void dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= N || c >= N || grid[r][c] == 0 || visited[r][c])
            return;

        visited[r][c] = true;
        for (auto& d : direct) {
            dfs(grid, r + d[0], c + d[1]);
        }
    }

    int bfs(vector<vector<int>>& grid) {
        queue<pair<int, int>> q;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (visited[r][c]) {
                    q.push({r, c});
                }
            }
        }

        int res = 0;
        while (!q.empty()) {
            for (int i = q.size(); i > 0; i--) {
                auto [r, c] = q.front(); q.pop();

                for (auto& d : direct) {
                    int curR = r + d[0], curC = c + d[1];

                    if (curR < 0 || curC < 0 || curR >= N || curC >= N || visited[curR][curC])
                        continue;

                    if (grid[curR][curC] == 1) return res;
                    q.push({curR, curC});
                    visited[curR][curC] = true;
                }
            }
            res++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Depth First Search + Breadth First Search - II

This is a space-optimized version of the previous approach. Instead of using a separate visited set, we modify the grid directly by marking visited land cells with the value 2. This distinguishes them from unvisited land (value 1) and water (value 0).

During BFS expansion, water cells are also marked as 2 when visited. When we encounter a cell with value 1, we know it belongs to the second island.

```cpp
class Solution {
    vector<vector<int>> direct;

public:
    int shortestBridge(vector<vector<int>>& grid) {
        int N = grid.size();
        direct = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        queue<pair<int, int>> q;

        bool found = false;
        for (int r = 0; r < N; r++) {
            if (found) break;
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    dfs(grid, r, c, q);
                    found = true;
                    break;
                }
            }
        }

        int res = 0;
        while (!q.empty()) {
            for (int i = q.size(); i > 0; i--) {
                auto [r, c] = q.front(); q.pop();

                for (auto& d : direct) {
                    int nr = r + d[0], nc = c + d[1];

                    if (nr < 0 || nc < 0 || nr >= N || nc >= N) continue;
                    if (grid[nr][nc] == 1) return res;

                    if (grid[nr][nc] == 0) {
                        grid[nr][nc] = 2;
                        q.push({nr, nc});
                    }
                }
            }
            res++;
        }
        return res;
    }

private:
    void dfs(vector<vector<int>>& grid, int r, int c, queue<pair<int, int>>& q) {
        if (r < 0 || c < 0 || r >= grid.size() || c >= grid.size() || grid[r][c] != 1)
            return;

        grid[r][c] = 2;
        q.push({r, c});
        for (auto& d : direct) {
            dfs(grid, r + d[0], c + d[1], q);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Breadth First Search

We can use BFS for both phases: identifying the first island and expanding to find the bridge. This avoids the recursive overhead of DFS and may be preferable for very large islands.

The first BFS explores all connected land cells starting from the first land cell found, marking them as visited. The second BFS then expands from all boundary cells of the first island simultaneously, searching for the second island.

```cpp
class Solution {
public:
    int shortestBridge(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>> direct = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        queue<pair<int, int>> q2;

        bool found = false;
        for (int r = 0; r < N; r++) {
            if (found) break;
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    queue<pair<int, int>> q1;
                    q1.push({r, c});
                    grid[r][c] = 2;

                    while (!q1.empty()) {
                        auto [x, y] = q1.front(); q1.pop();
                        q2.push({x, y});

                        for (auto& d : direct) {
                            int nx = x + d[0], ny = y + d[1];
                            if (nx >= 0 && ny >= 0 && nx < N && ny < N && grid[nx][ny] == 1) {
                                grid[nx][ny] = 2;
                                q1.push({nx, ny});
                            }
                        }
                    }
                    found = true;
                    break;
                }
            }
        }

        int res = 0;
        while (!q2.empty()) {
            for (int i = q2.size(); i > 0; i--) {
                auto [x, y] = q2.front(); q2.pop();

                for (auto& d : direct) {
                    int nx = x + d[0], ny = y + d[1];

                    if (nx >= 0 && ny >= 0 && nx < N && ny < N) {
                        if (grid[nx][ny] == 1) return res;
                        if (grid[nx][ny] == 0) {
                            grid[nx][ny] = 2;
                            q2.push({nx, ny});
                        }
                    }
                }
            }
            res++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Disjoint Set Union + Breadth First Search

A Disjoint Set Union (DSU) data structure can identify connected components. By scanning the grid and unioning adjacent land cells, we naturally group cells into their respective islands.

Once we know which cells belong to the first island (tracked during the initial union phase), we start BFS from the boundary cells of that island. As we expand, we union newly visited cells with the first island. When a union operation connects to a cell that was already land (value 1) but in a different component, we have found the bridge.

```cpp
class DSU {
public:
    vector<int> parent, rank;

    DSU(int n) : parent(n), rank(n, 1) {
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int node) {
        if (parent[node] != node)
            parent[node] = find(parent[node]);
        return parent[node];
    }

    bool unionSet(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (rank[pv] > rank[pu]) swap(pu, pv);
        parent[pv] = pu;
        rank[pu] += rank[pv];
        return true;
    }
};

class Solution {
public:
    int shortestBridge(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>> direct = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        DSU dsu(N * N + 1);
        queue<pair<int, int>> q;

        auto idx = [&](int r, int c) {
            return r * N + c + 1;
        };

        int firstIsland = -1;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    firstIsland = dsu.find(idx(r, c));
                    if (c + 1 < N && grid[r][c + 1] == 1)
                        dsu.unionSet(idx(r, c), idx(r, c + 1));
                    if (r + 1 < N && grid[r + 1][c] == 1)
                        dsu.unionSet(idx(r, c), idx(r + 1, c));
                }
            }
        }

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1 && dsu.find(idx(r, c)) == firstIsland) {
                    for (auto& d : direct) {
                        int nr = r + d[0], nc = c + d[1];
                        if (nr >= 0 && nc >= 0 && nr < N && nc < N && grid[nr][nc] == 0) {
                            q.push({r, c});
                            break;
                        }
                    }
                }
            }
        }

        int res = 0;
        while (!q.empty()) {
            for (int i = q.size(); i > 0; i--) {
                auto [r, c] = q.front();q.pop();
                for (auto& d : direct) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nc >= 0 && nr < N && nc < N) {
                        if (grid[nr][nc] == 1 && dsu.unionSet(idx(r, c), idx(nr, nc)))
                            return res;
                        if (grid[nr][nc] == 0) {
                            grid[nr][nc] = 1;
                            dsu.unionSet(idx(r, c), idx(nr, nc));
                            q.push({nr, nc});
                        }
                    }
                }
            }
            res++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$
