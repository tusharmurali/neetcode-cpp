# 1162. As Far from Land as Possible

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/as-far-from-land-as-possible/>  
- **NeetCode:** <https://neetcode.io/problems/as-far-from-land-as-possible>  
- **Video:** <https://www.youtube.com/watch?v=fjxb1hQfrZk>  

[← Back to index](../INDEX.md)

## 1. Brute Force (BFS)

For each water cell, we want to find the distance to the nearest land cell. The simplest approach is to run a separate BFS from each water cell, expanding outward until we hit land. We track the maximum of all these minimum distances. This gives the correct answer but is slow because we repeat similar work for each water cell.

```cpp
class Solution {
public:
    int maxDistance(vector<vector<int>>& grid) {
        int N = grid.size();
        int res = -1;

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 0) {
                    res = max(res, bfs(grid, r, c, N));
                    if (res == -1) return res;
                }
            }
        }
        return res;
    }

private:
    const int direct[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    int bfs(vector<vector<int>>& grid, int row, int col, int N) {
        queue<pair<int, int>> q;
        vector<vector<bool>> visit(N, vector<bool>(N, false));
        q.push({row, col});
        visit[row][col] = true;
        int dist = 0;

        while (!q.empty()) {
            dist++;
            for (int i = q.size(); i > 0; i--) {
                auto [r, c] = q.front();q.pop();

                for (auto& d : direct) {
                    int newR = r + d[0], newC = c + d[1];
                    if (newR < 0 || newC < 0 || newR >= N || newC >= N || visit[newR][newC])
                        continue;
                    if (grid[newR][newC] == 1)
                        return dist;

                    visit[newR][newC] = true;
                    q.push({newR, newC});
                }
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 4)$
- Space complexity: $O(n ^ 2)$

## 2. Multi Source BFS (Overwriting Input)

Instead of searching from each water cell, we can flip the problem: start from all land cells simultaneously and expand outward. This multi-source BFS finds the shortest distance from any land cell to each water cell in a single traversal. The last water cell we reach has the maximum distance. We use the grid itself to store distances, avoiding extra space.

```cpp
class Solution {
    const int direct[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

public:
    int maxDistance(vector<vector<int>>& grid) {
        int N = grid.size();
        queue<pair<int, int>> q;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    q.push({r, c});
                }
            }
        }

        int res = -1;
        while (!q.empty()) {
            auto [r, c] = q.front();q.pop();
            res = grid[r][c];
            for (int d = 0; d < 4; d++) {
                int newR = r + direct[d][0], newC = c + direct[d][1];
                if (newR >= 0 && newC >= 0 && newR < N && newC < N && grid[newR][newC] == 0) {
                    q.push({newR, newC});
                    grid[newR][newC] = grid[r][c] + 1;
                }
            }
        }
        return res > 1 ? res - 1 : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Multi Source BFS

This is similar to the previous approach but uses a separate visited array instead of modifying the input grid. We still start BFS from all land cells at once and expand outward. The number of BFS levels we complete before the queue empties tells us the maximum distance from any water cell to its nearest land.

```cpp
class Solution {
public:
    int maxDistance(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<int> direct = {0, 1, 0, -1, 0};
        vector<vector<bool>> visit(N, vector<bool>(N, false));
        queue<pair<int, int>> q;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) {
                    visit[r][c] = true;
                    q.push({r, c});
                }
            }
        }

        int res = 0;
        while (!q.empty()) {
            res++;
            for (int i = q.size(); i > 0; i--) {
                auto [r, c] = q.front();q.pop();
                for (int d = 0; d < 4; d++) {
                    int newR = r + direct[d], newC = c + direct[d + 1];
                    if (newR >= 0 && newC >= 0 && newR < N && newC < N && !visit[newR][newC]) {
                        q.push({newR, newC});
                        visit[newR][newC] = true;
                    }
                }
            }
        }
        return res > 1 ? res - 1 : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Overwriting the Input)

Distance to the nearest land can propagate from multiple directions. If we make two passes, one from top-left to bottom-right and another from bottom-right to top-left, we cover all four directions. In the first pass, each cell gets the minimum distance considering paths from above and left. In the second pass, we also consider paths from below and right. The maximum value after both passes is our answer.

```cpp
class Solution {
public:
    int maxDistance(vector<vector<int>>& grid) {
        int N = grid.size(), INF = 1000000;

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 1) continue;
                grid[r][c] = INF;
                if (r > 0) grid[r][c] = min(grid[r][c], grid[r - 1][c] + 1);
                if (c > 0) grid[r][c] = min(grid[r][c], grid[r][c - 1] + 1);
            }
        }

        int res = 0;
        for (int r = N - 1; r >= 0; r--) {
            for (int c = N - 1; c >= 0; c--) {
                if (grid[r][c] == 1) continue;
                if (r < N - 1) grid[r][c] = min(grid[r][c], grid[r + 1][c] + 1);
                if (c < N - 1) grid[r][c] = min(grid[r][c], grid[r][c + 1] + 1);
                res = max(res, grid[r][c]);
            }
        }

        return res < INF ? res - 1 : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 5. Dynamic Programming

This approach is identical to the previous one but uses a separate DP array instead of modifying the input. We pad the array with an extra row and column on each side (filled with infinity) to avoid boundary checks. Land cells get distance 0, and water cells accumulate distances from their neighbors across two passes.

```cpp
class Solution {
public:
    int maxDistance(vector<vector<int>>& grid) {
        int N = grid.size();
        int INF = 1000000, res = -1;
        vector<vector<int>> dp(N + 2, vector<int>(N + 2, INF));

        for (int r = 1; r <= N; r++) {
            for (int c = 1; c <= N; c++) {
                if (grid[r - 1][c - 1] == 1) {
                    dp[r][c] = 0;
                } else {
                    dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + 1;
                }
            }
        }

        for (int r = N; r > 0; r--) {
            for (int c = N; c > 0; c--) {
                if (grid[r - 1][c - 1] == 0) {
                    dp[r][c] = min(dp[r][c], min(dp[r + 1][c], dp[r][c + 1]) + 1);
                    res = max(res, dp[r][c]);
                }
            }
        }
        return res < INF ? res : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$
