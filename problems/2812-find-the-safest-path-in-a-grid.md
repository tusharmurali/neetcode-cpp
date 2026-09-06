# 2812. Find the Safest Path in a Grid

- **Difficulty:** Medium  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-safest-path-in-a-grid/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-safest-path-in-a-grid>  
- **Video:** <https://www.youtube.com/watch?v=-5mQcNiVWTs>  

[← Back to index](../INDEX.md)

## 1. Multi Source BFS + Dijkstra's Algorithm

The safeness factor of a path is the minimum distance to any thief along that path. We want to maximize this minimum. First, we need to know the distance from every cell to the nearest thief, which we can compute using multi-source BFS from all thief positions. Then, finding the safest path becomes a modified shortest path problem where we maximize the minimum edge weight along the path, which Dijkstra's algorithm with a max-heap handles well.

```cpp
class Solution {
    static constexpr int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

public:
    int maximumSafenessFactor(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>> minDist = precompute(grid, N);
        priority_queue<vector<int>> maxHeap;
        vector<vector<bool>> visit(N, vector<bool>(N, false));

        maxHeap.push({minDist[0][0], 0, 0});
        visit[0][0] = true;

        while (!maxHeap.empty()) {
            vector<int> cur = maxHeap.top(); maxHeap.pop();
            int dist = cur[0], r = cur[1], c = cur[2];

            if (r == N - 1 && c == N - 1) {
                return dist;
            }

            for (const auto& dir : directions) {
                int r2 = r + dir[0], c2 = c + dir[1];
                if (inBounds(r2, c2, N) && !visit[r2][c2]) {
                    visit[r2][c2] = true;
                    int dist2 = min(dist, minDist[r2][c2]);
                    maxHeap.push({dist2, r2, c2});
                }
            }
        }
        return 0;
    }

private:
    vector<vector<int>> precompute(vector<vector<int>>& grid, int N) {
        vector<vector<int>> minDist(N, vector<int>(N, -1));
        queue<vector<int>> q;

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    q.push({r, c, 0});
                    minDist[r][c] = 0;
                }
            }
        }

        while (!q.empty()) {
            vector<int> cur = q.front();
            q.pop();
            int r = cur[0], c = cur[1], dist = cur[2];

            for (const auto& dir : directions) {
                int r2 = r + dir[0], c2 = c + dir[1];
                if (inBounds(r2, c2, N) && minDist[r2][c2] == -1) {
                    minDist[r2][c2] = dist + 1;
                    q.push({r2, c2, dist + 1});
                }
            }
        }
        return minDist;
    }

    bool inBounds(int r, int c, int N) {
        return r >= 0 && c >= 0 && r < N && c < N;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 2. Multi Source BFS + Dijkstra's Algorithm (Overwriting the Input)

This approach is identical to the previous one but optimizes space by reusing the input grid to store the precomputed minimum distances. Additionally, it uses a `safeFactor` array to track the best safeness factor found so far for each cell, allowing us to skip cells if we have already found a better path to them.

```cpp
class Solution {
public:
    int maximumSafenessFactor(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<int> directions = {0, 1, 0, -1, 0};
        vector<vector<int>>& minDist = grid;

        queue<int> q;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    q.push(r * N + c);
                    minDist[r][c] = 0;
                } else {
                    minDist[r][c] = -1;
                }
            }
        }

        while (!q.empty()) {
            int node = q.front(); q.pop();
            int r = node / N, c = node % N;
            for (int i = 0; i < 4; i++) {
                int r2 = r + directions[i], c2 = c + directions[i + 1];
                if (r2 >= 0 && c2 >= 0 && r2 < N && c2 < N && minDist[r2][c2] == -1) {
                    minDist[r2][c2] = minDist[r][c] + 1;
                    q.push(r2 * N + c2);
                }
            }
        }

        priority_queue<pair<int, int>> maxHeap;
        vector<int> safeFactor(N * N, 0);
        safeFactor[0] = minDist[0][0];
        maxHeap.push({safeFactor[0], 0});

        while (!maxHeap.empty()) {
            auto [dist, node] = maxHeap.top(); maxHeap.pop();
            int r = node / N, c = node % N;
            if (r == N - 1 && c == N - 1) {
                return dist;
            }
            if (safeFactor[node] > dist) {
                continue;
            }

            for (int i = 0; i < 4; i++) {
                int r2 = r + directions[i], c2 = c + directions[i + 1], node2 = r2 * N + c2;
                if (r2 >= 0 && c2 >= 0 && r2 < N && c2 < N) {
                    int dist2 = min(dist, minDist[r2][c2]);
                    if (dist2 > safeFactor[node2]) {
                        safeFactor[node2] = dist2;
                        maxHeap.push({dist2, node2});
                    }
                }
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 3. Multi Source BFS + Binary Search

Instead of using Dijkstra to find the optimal safeness, we can binary search on the answer. For a given safeness threshold, we check if there exists a path from start to end using only cells with `minDist >= threshold`. This check is a simple BFS or DFS. The maximum valid threshold is our answer.

```cpp
class Solution {
    static constexpr int directions[5] = {0, 1, 0, -1, 0};

public:
    int maximumSafenessFactor(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>>& minDist = grid;

        queue<int> q;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    q.push(r * N + c);
                    minDist[r][c] = 0;
                } else {
                    minDist[r][c] = -1;
                }
            }
        }

        while (!q.empty()) {
            int node = q.front(); q.pop();
            int r = node / N, c = node % N;
            for (int i = 0; i < 4; i++) {
                int r2 = r + directions[i], c2 = c + directions[i + 1];
                if (r2 >= 0 && c2 >= 0 && r2 < N && c2 < N && minDist[r2][c2] == -1) {
                    minDist[r2][c2] = minDist[r][c] + 1;
                    q.push(r2 * N + c2);
                }
            }
        }

        int l = 0, r = min(minDist[0][0], minDist[N - 1][N - 1]);
        while (l <= r) {
            int mid = (l + r) / 2;
            if (canReach(minDist, N, mid)) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        return l - 1;
    }

private:
    bool canReach(vector<vector<int>>& minDist, int N, int threshold) {
        queue<int> q;
        vector<bool> visited(N * N, false);
        q.push(0);
        visited[0] = true;

        while (!q.empty()) {
            int node = q.front(); q.pop();
            int r = node / N, c = node % N;
            if (r == N - 1 && c == N - 1) {
                return true;
            }

            for (int i = 0; i < 4; i++) {
                int r2 = r + directions[i], c2 = c + directions[i + 1], node2 = r2 * N + c2;
                if (r2 >= 0 && c2 >= 0 && r2 < N && c2 < N && !visited[node2] &&
                    minDist[r2][c2] >= threshold) {
                    visited[node2] = true;
                    q.push(node2);
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 4. Breadth First Search (0-1 BFS)

0-1 BFS is an optimization when edge weights are only 0 or 1. Here we adapt it: moving to a neighbor with the same or better safeness has cost 0, while moving to a neighbor with worse safeness has cost 1 (we are forced to accept a lower minimum). By adding zero-cost moves to the front and cost-1 moves to the back of a deque, we process cells in order of decreasing safeness factor.

```cpp
class Solution {
public:
    int maximumSafenessFactor(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>>& minDist = grid;
        constexpr int directions[5] = {0, 1, 0, -1, 0};

        deque<int> q;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    q.push_back(r * N + c);
                    minDist[r][c] = 0;
                } else {
                    minDist[r][c] = -1;
                }
            }
        }

        while (!q.empty()) {
            int node = q.front(); q.pop_front();
            int r = node / N, c = node % N;
            for (int i = 0; i < 4; i++) {
                int r2 = r + directions[i], c2 = c + directions[i + 1];
                if (r2 >= 0 && c2 >= 0 && r2 < N && c2 < N && minDist[r2][c2] == -1) {
                    minDist[r2][c2] = minDist[r][c] + 1;
                    q.push_back(r2 * N + c2);
                }
            }
        }

        vector<int> safeFactor(N * N, -1);
        int res = safeFactor[0] = min(minDist[N - 1][N - 1], minDist[0][0]);
        q.push_back(0);

        while (!q.empty()) {
            int node = q.front(); q.pop_front();
            int r = node / N, c = node % N;
            res = min(res, safeFactor[node]);
            if (r == N - 1 && c == N - 1) {
                break;
            }

            for (int i = 0; i < 4; i++) {
                int r2 = r + directions[i], c2 = c + directions[i + 1], node2 = r2 * N + c2;
                if (r2 >= 0 && c2 >= 0 && r2 < N && c2 < N && safeFactor[node2] == -1) {
                    safeFactor[node2] = min(safeFactor[node], minDist[r2][c2]);
                    if (safeFactor[node2] < res) {
                        q.push_back(node2);
                    } else {
                        q.push_front(node2);
                    }
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$
