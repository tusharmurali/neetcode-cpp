# 1631. Path with Minimum Effort

- **Difficulty:** Medium  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/path-with-minimum-effort/>  
- **NeetCode:** <https://neetcode.io/problems/path-with-minimum-effort>  
- **Video:** <https://www.youtube.com/watch?v=XQlxCCx2vI4>  

[← Back to index](../INDEX.md)

## 1. Dijkstra's Algorithm

The effort of a path is defined as the maximum absolute difference between consecutive cells along that path. We want to minimize this maximum difference. Dijkstra's algorithm fits well because we can treat the "effort so far" as the cost and always expand the path with the smallest maximum effort. When we reach the destination, we have found the path with minimum effort.

```cpp
class Solution {
public:
    int minimumEffortPath(vector<vector<int>>& heights) {
        int rows = heights.size(), cols = heights[0].size();
        vector<vector<int>> dist(rows, vector<int>(cols, INT_MAX));
        dist[0][0] = 0;

        priority_queue<vector<int>, vector<vector<int>>, greater<>> minHeap;
        minHeap.push({0, 0, 0}); // {diff, row, col}

        vector<vector<int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

        while (!minHeap.empty()) {
            auto curr = minHeap.top();
            minHeap.pop();
            int diff = curr[0], r = curr[1], c = curr[2];

            if (r == rows - 1 && c == cols - 1) return diff;
            if (dist[r][c] < diff) continue;

            for (auto& dir : directions) {
                int newR = r + dir[0], newC = c + dir[1];
                if (newR < 0 || newC < 0 || newR >= rows || newC >= cols) {
                    continue;
                }

                int newDiff = max(diff, abs(heights[r][c] - heights[newR][newC]));
                if (newDiff < dist[newR][newC]) {
                    dist[newR][newC] = newDiff;
                    minHeap.push({newDiff, newR, newC});
                }
            }
        }

        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * \log (m * n))$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given matrix.

## 2. Binary Search + DFS

We can binary search on the answer. For a given effort limit, we check whether it is possible to reach the destination using only edges with absolute differences at most that limit. `dfs` explores if a valid path exists under the constraint. If a path exists, we try a smaller limit; otherwise, we try a larger one.

```cpp
class Solution {
private:
    int ROWS, COLS;
    vector<vector<int>> heights;
    vector<vector<bool>> visited;
    vector<vector<int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

public:
    int minimumEffortPath(vector<vector<int>>& heights) {
        this->heights = heights;
        this->ROWS = heights.size();
        this->COLS = heights[0].size();
        this->visited = vector<vector<bool>>(ROWS, vector<bool>(COLS, false));

        int l = 0, r = 1'000'000, res = r;
        while (l <= r) {
            int mid = (l + r) / 2;
            for (auto& row : visited) {
                fill(row.begin(), row.end(), false);
            }
            if (dfs(0, 0, mid)) {
                res = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        return res;
    }

private:
    bool dfs(int r, int c, int limit) {
        if (r == ROWS - 1 && c == COLS - 1) {
            return true;
        }

        visited[r][c] = true;
        for (const auto& dir : directions) {
            int newR = r + dir[0];
            int newC = c + dir[1];
            if (newR < 0 || newC < 0 || newR >= ROWS || newC >= COLS || visited[newR][newC]) {
                continue;
            }
            if (abs(heights[newR][newC] - heights[r][c]) > limit) {
                continue;
            }
            if (dfs(newR, newC, limit)) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * \log (m * n))$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given matrix.

## 3. Kruskal's Algorithm

We can view the grid as a graph where each cell is a node and edges connect adjacent cells with weights equal to the absolute height difference. The problem becomes finding the path from top-left to bottom-right that minimizes the maximum edge weight. Kruskal's algorithm processes edges in sorted order, and we stop as soon as the source and destination become connected. The last edge added determines the minimum effort.

```cpp
class DSU {
private:
    vector<int> Parent, Size;

public:
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
        int pu = find(u);
        int pv = find(v);
        if (pu == pv) {
            return false;
        }
        if (Size[pu] < Size[pv]) {
            swap(pu, pv);
        }
        Size[pu] += Size[pv];
        Parent[pv] = pu;
        return true;
    }
};

class Solution {
public:
    int minimumEffortPath(vector<vector<int>>& heights) {
        int ROWS = heights.size();
        int COLS = heights[0].size();
        vector<tuple<int, int, int>> edges;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (r + 1 < ROWS) {
                    edges.push_back({abs(heights[r][c] - heights[r + 1][c]), r * COLS + c, (r + 1) * COLS + c});
                }
                if (c + 1 < COLS) {
                    edges.push_back({abs(heights[r][c] - heights[r][c + 1]), r * COLS + c, r * COLS + c + 1});
                }
            }
        }

        sort(edges.begin(), edges.end());
        DSU dsu(ROWS * COLS);
        for (auto& edge : edges) {
            int weight, u, v;
            tie(weight, u, v) = edge;
            dsu.unionSets(u, v);
            if (dsu.find(0) == dsu.find(ROWS * COLS - 1)) {
                return weight;
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * \log (m * n))$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given matrix.

## 4. Shortest Path Faster Algorithm

SPFA can also solve this problem by treating effort as the distance metric. We use a queue to process cells and update their minimum effort when a better path is found. Unlike Dijkstra's, SPFA does not require a priority queue, trading off guaranteed optimal ordering for simplicity and potential efficiency on some inputs.

```cpp
class Solution {
public:
    int minimumEffortPath(vector<vector<int>>& heights) {
        int ROWS = heights.size(), COLS = heights[0].size();
        vector<int> dist(ROWS * COLS, INT_MAX);
        dist[0] = 0;

        vector<bool> inQueue(ROWS * COLS, false);
        queue<int> q;
        q.push(0);
        inQueue[0] = true;

        vector<vector<int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

        while (!q.empty()) {
            int u = q.front();
            q.pop();
            inQueue[u] = false;

            int r = u / COLS, c = u % COLS;

            for (const auto& dir : directions) {
                int newR = r + dir[0], newC = c + dir[1];
                if (newR >= 0 && newC >= 0 && newR < ROWS && newC < COLS) {
                    int v = newR * COLS + newC;
                    int weight = abs(heights[r][c] - heights[newR][newC]);
                    int newDist = max(dist[u], weight);
                    if (newDist < dist[v]) {
                        dist[v] = newDist;
                        if (!inQueue[v]) {
                            q.push(v);
                            inQueue[v] = true;
                        }
                    }
                }
            }
        }

        return dist[ROWS * COLS - 1];
    }
};
```

**Complexity**

- Time complexity:
    - $O(m * n)$ time in average case.
    - $O(m ^ 2 * n ^ 2)$ time in worst case.
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the given matrix.
