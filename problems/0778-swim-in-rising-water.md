# 778. Swim In Rising Water

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/swim-in-rising-water/>  
- **NeetCode:** <https://neetcode.io/problems/swim-in-rising-water>  
- **Video:** <https://www.youtube.com/watch?v=amvrKlMLuGY>  
- **Video approach:** 4. Dijkstra's Algorithm  

[← Back to index](../INDEX.md)

## 1. Brute Force

This brute force tries **every possible path** from the top-left to the bottom-right.

While walking, your “time” is not the number of steps — it’s the **maximum height value you have stepped on so far**, because you must wait until water rises to at least that height to pass those cells.

So for each path:
- The cost of the path = **max cell value on that path**
- We want the path with the **minimum** such cost (minimize the worst height you had to cross).

The DFS explores all routes, keeps a `visited` grid to avoid looping, and returns the best (minimum) possible maximum-height value among all paths.

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<vector<bool>> visit(n, vector<bool>(n, false));
        return dfs(grid, visit, 0, 0, 0);
    }

private:
    int dfs(vector<vector<int>>& grid, vector<vector<bool>>& visit,
            int r, int c, int t) {
        int n = grid.size();
        if (r < 0 || c < 0 || r >= n || c >= n || visit[r][c]) {
            return 1000000;
        }
        if (r == n - 1 && c == n - 1) {
            return max(t, grid[r][c]);
        }
        visit[r][c] = true;
        t = max(t, grid[r][c]);
        int res = min(min(dfs(grid, visit, r + 1, c, t),
                                     dfs(grid, visit, r - 1, c, t)),
                           min(dfs(grid, visit, r, c + 1, t),
                                    dfs(grid, visit, r, c - 1, t)));
        visit[r][c] = false;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(4 ^ {n ^ 2})$
- Space complexity: $O(n ^ 2)$

## 2. Depth First Search

Here we turn the problem into a **yes/no question**:

> “If the water level is `t`, can I reach the bottom-right?”

At water level `t`, you are only allowed to step on cells with `grid[r][c] <= t`.  
So we try a DFS that only walks through “allowed” cells.  
Then we **increase `t` gradually** from the smallest possible height to the largest, and return the first `t` where reaching the end becomes possible.

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<vector<bool>> visit(n, vector<bool>(n, false));
        int minH = grid[0][0], maxH = grid[0][0];
        for (int row = 0; row < n; row++) {
            for (int col = 0; col < n; col++) {
                maxH = max(maxH, grid[row][col]);
                minH = min(minH, grid[row][col]);
            }
        }

        for (int t = minH; t < maxH; t++) {
            if (dfs(grid, visit, 0, 0, t)) {
                return t;
            }
            for (int r = 0; r < n; r++) {
                fill(visit[r].begin(), visit[r].end(), false);
            }
        }
        return maxH;
    }

private:
    bool dfs(vector<vector<int>>& grid, vector<vector<bool>>& visit,
                                        int r, int c, int t) {
        if (r < 0 || c < 0 || r >= grid.size() ||
            c >= grid.size() || visit[r][c] || grid[r][c] > t) {
            return false;
        }
        if (r == grid.size() - 1 && c == grid.size() - 1) {
            return true;
        }
        visit[r][c] = true;
        return dfs(grid, visit, r + 1, c, t) ||
               dfs(grid, visit, r - 1, c, t) ||
               dfs(grid, visit, r, c + 1, t) ||
               dfs(grid, visit, r, c - 1, t);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 4)$
- Space complexity: $O(n ^ 2)$

## 3. Binary Search + DFS

Instead of trying every water level `t` one by one, we **binary search the answer**.

Key idea:
- If you **can** reach the bottom-right at water level `t`, then you can also reach it at any **higher** level (`t+1, t+2, ...`).  
- If you **cannot** reach at `t`, you also cannot reach at any **lower** level.

So the condition “reachable at `t`” is **monotonic** → perfect for binary search.

To test a fixed `t`, run a **DFS** from `(0,0)` and only move through cells with `height <= t`.

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<vector<bool>> visit(n, vector<bool>(n, false));
        int minH = grid[0][0], maxH = grid[0][0];
        for (int row = 0; row < n; row++) {
            for (int col = 0; col < n; col++) {
                maxH = max(maxH, grid[row][col]);
                minH = min(minH, grid[row][col]);
            }
        }

        int l = minH, r = maxH;
        while (l < r) {
            int m = (l + r) >> 1;
            if (dfs(grid, visit, 0, 0, m)) {
                r = m;
            } else {
                l = m + 1;
            }
            for (int row = 0; row < n; row++) {
                fill(visit[row].begin(), visit[row].end(), false);
            }
        }
        return r;
    }

private:
    bool dfs(vector<vector<int>>& grid, vector<vector<bool>>& visit,
                                        int r, int c, int t) {
        if (r < 0 || c < 0 || r >= grid.size() ||
            c >= grid.size() || visit[r][c] || grid[r][c] > t) {
            return false;
        }
        if (r == grid.size() - 1 && c == grid.size() - 1) {
            return true;
        }
        visit[r][c] = true;
        return dfs(grid, visit, r + 1, c, t) ||
               dfs(grid, visit, r - 1, c, t) ||
               dfs(grid, visit, r, c + 1, t) ||
               dfs(grid, visit, r, c - 1, t);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
    - The binary search runs for $O(\log(n ^ 2))$ iterations because the height range contains at most $n ^ 2$ values. Since $\log(n ^ 2) = 2\log n$, this simplifies to $O(\log n)$ iterations, with each DFS taking $O(n ^ 2)$ time.
- Space complexity: $O(n ^ 2)$

## 4. Dijkstra's Algorithm ▶ video

Think of each cell’s height as the **earliest time** you’re allowed to stand on it (water must be at least that high).  
While moving from start to end, the **total time of a path** is not the sum — it’s the **maximum height** you ever step on (because water must rise to that max).

So the problem becomes:
> Find a path from (0,0) to (n-1,n-1) that **minimizes the maximum cell height** along the path.

That is exactly what Dijkstra can solve if we define:
- **cost to reach a cell** = smallest possible “maximum height so far”.

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int N = grid.size();
        set<pair<int, int>> visit;
        priority_queue<vector<int>,
                       vector<vector<int>>, greater<>> minHeap;
        vector<vector<int>> directions = {
            {0, 1}, {0, -1}, {1, 0}, {-1, 0}
        };

        minHeap.push({grid[0][0], 0, 0});
        visit.insert({0, 0});

        while (!minHeap.empty()) {
            auto curr = minHeap.top();
            minHeap.pop();
            int t = curr[0], r = curr[1], c = curr[2];
            if (r == N - 1 && c == N - 1) {
                return t;
            }
            for (const auto& dir : directions) {
                int neiR = r + dir[0], neiC = c + dir[1];
                if (neiR < 0 || neiC < 0 || neiR == N ||
                    neiC == N || visit.count({neiR, neiC})) {
                    continue;
                }
                visit.insert({neiR, neiC});
                minHeap.push({
                    max(t, grid[neiR][neiC]), neiR, neiC
                });
            }
        }

        return N * N;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 5. Kruskal's Algorithm

Water level `t` rises over time. At time `t`, you’re allowed to step only on cells with height `<= t`.  
So as `t` increases, **more cells become “open”** and neighboring open cells form bigger connected regions.

We want the **earliest time `t`** when the start cell `(0,0)` and end cell `(N-1,N-1)` become part of the **same connected component**.

DSU (Union-Find) is perfect for this: it quickly merges neighboring open cells and checks if start and end are connected.

```cpp
class DSU {
    vector<int> Parent, Size;
public:
    DSU(int n) : Parent(n + 1), Size(n + 1, 1) {
        for (int i = 0; i <= n; i++) Parent[i] = i;
    }

    int find(int node) {
        if (Parent[node] != node)
            Parent[node] = find(Parent[node]);
        return Parent[node];
    }

    bool unionSets(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (Size[pu] < Size[pv]) swap(pu, pv);
        Size[pu] += Size[pv];
        Parent[pv] = pu;
        return true;
    }

    bool connected(int u, int v) {
        return find(u) == find(v);
    }
};

class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int N = grid.size();
        DSU dsu(N * N);
        vector<tuple<int, int, int>> positions;
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++)
                positions.emplace_back(grid[r][c], r, c);

        sort(positions.begin(), positions.end());
        vector<pair<int, int>> directions = {
            {0, 1}, {1, 0}, {0, -1}, {-1, 0}
        };

        for (auto& [t, r, c] : positions) {
            for (auto& [dr, dc] : directions) {
                int nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < N && nc >= 0 &&
                    nc < N && grid[nr][nc] <= t) {
                    dsu.unionSets(r * N + c, nr * N + nc);
                }
            }
            if (dsu.connected(0, N * N - 1)) return t;
        }
        return N * N;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## Standalone solution file (`cpp/0778-swim-in-rising-water.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer elevation matrix, rain falls, at time t, depth everywhere is t
    Can swim iff elevation at most t, return least time get from top left to bottom right

    Shortest path w/ min heap: at every step, find lowest water level to move forward

    Time: O(n^2 log n)
    Space: O(n^2)
*/

class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        if (n == 1) {
            return 0;
        }
        
        vector<vector<bool>> visited(n, vector<bool>(n));
        visited[0][0] = true;
        
        int result = max(grid[0][0], grid[n - 1][n - 1]);
        
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq;
        pq.push({result, 0, 0});
        
        while (!pq.empty()) {
            vector<int> curr = pq.top();
            pq.pop();
            
            result = max(result, curr[0]);
            
            for (int i = 0; i < 4; i++) {
                int x = curr[1] + dirs[i][0];
                int y = curr[2] + dirs[i][1];
                
                if (x < 0 || x >= n || y < 0 || y >= n || visited[x][y]) {
                    continue;
                }
                
                if (x == n - 1 && y == n - 1) {
                    return result;
                }

                pq.push({grid[x][y], x, y});
                visited[x][y] = true;
            }
        }
        
        return -1;
    }
private:
    vector<vector<int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
};
```
