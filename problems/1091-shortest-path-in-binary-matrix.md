# 1091. Shortest Path in Binary Matrix

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shortest-path-in-binary-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/shortest-path-in-binary-matrix>  
- **Video:** <https://www.youtube.com/watch?v=YnxUdAO7TAo>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

We need to find the shortest path from the top-left corner to the bottom-right corner in a binary matrix, where we can only travel through cells containing `0`. Since we want the shortest path and each step has equal weight, `BFS` is the natural choice. `BFS` explores cells level by level, guaranteeing that the first time we reach the destination, we have found the shortest path. We can move in all 8 directions (horizontal, vertical, and diagonal), so we check all 8 neighbors at each step.

```cpp
class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int N = grid.size();
        if (grid[0][0] == 1 || grid[N - 1][N - 1] == 1) return -1;

        vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0},
                                             {1, 1}, {-1, -1}, {1, -1}, {-1, 1}};
        vector<vector<bool>> visit(N, vector<bool>(N, false));

        queue<tuple<int, int, int>> q;
        q.push({0, 0, 1});
        visit[0][0] = true;

        while (!q.empty()) {
            auto [r, c, length] = q.front();
            q.pop();

            if (r == N - 1 && c == N - 1) return length;

            for (auto [dr, dc] : directions) {
                int nr = r + dr, nc = c + dc;
                if (nr >= 0 && nc >= 0 && nr < N && nc < N &&
                    grid[nr][nc] == 0 && !visit[nr][nc]) {
                    q.push({nr, nc, length + 1});
                    visit[nr][nc] = true;
                }
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Breadth First Search (Overwriting the Input)

This approach is similar to the standard `BFS` but optimizes space by using the input grid itself to store distances. Instead of maintaining a separate visited set, we overwrite each cell with its `distance` from the start. A cell value of `0` indicates unvisited, while any positive value represents the shortest distance to reach that cell. This eliminates the need for extra space while preserving the `BFS` guarantee of finding the shortest path.

```cpp
class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int N = grid.size();
        int direct[10] = {0, 1, 0, -1, 0, 1, 1, -1, -1, 1};

        if (grid[0][0] || grid[N - 1][N - 1])
            return -1;

        queue<pair<int, int>> q;
        q.push({0, 0});
        grid[0][0] = 1;

        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            int dist = grid[r][c];

            if (r == N - 1 && c == N - 1)
                return dist;

            for (int d = 0; d < 9; d++) {
                int nr = r + direct[d], nc = c + direct[d + 1];

                if (nr >= 0 && nc >= 0 && nr < N && nc < N && grid[nr][nc] == 0) {
                    grid[nr][nc] = dist + 1;
                    q.push({nr, nc});
                }
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Bidirectional Breadth First Search

Standard `BFS` explores outward from the source in all directions. Bidirectional `BFS` runs two searches simultaneously: one from the start and one from the end. When the two search frontiers meet, we have found the shortest path. This reduces the search space significantly because instead of exploring a circle of radius `d`, we explore two circles of radius `d/2`. The total area explored is roughly half of what single-direction `BFS` would cover.

```cpp
class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int N = grid.size();
        if (grid[0][0] || grid[N - 1][N - 1]) return -1;
        if (N == 1) return 1;

        int direct[10] = {0, 1, 0, -1, 0, 1, 1, -1, -1, 1};
        queue<pair<int, int>> q1, q2;
        q1.push({0, 0});
        q2.push({N - 1, N - 1});
        grid[0][0] = -1;
        grid[N - 1][N - 1] = -2;

        int res = 2, start = -1, end = -2;
        while (!q1.empty() && !q2.empty()) {
            for (int i = q1.size(); i > 0; i--) {
                auto [r, c] = q1.front();
                q1.pop();

                for (int d = 0; d < 9; d++) {
                    int nr = r + direct[d], nc = c + direct[d + 1];
                    if (nr >= 0 && nc >= 0 && nr < N && nc < N) {
                        if (grid[nr][nc] == end) return res;
                        if (grid[nr][nc] == 0) {
                            grid[nr][nc] = start;
                            q1.push({nr, nc});
                        }
                    }
                }
            }
            swap(q1, q2);
            swap(start, end);
            res++;
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## Standalone solution file (`cpp/1091-shortest-path-in-binary-matrix.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int n = grid.size();
        if(grid[0][0]==1 || grid[n-1][n-1]==1) return -1;

        // {{r,c},length}
        queue<pair<pair<int,int>,int>> q;
        set<pair<int,int>> visited;

        q.push({{0,0},0});
        visited.insert(make_pair(0,0));

        int drow[] = {0,1,0,-1,1,-1,1,-1};
        int dcol[] = {1,0,-1,0,1,-1,-1,1};

        while(!q.empty()){
            int row = q.front().first.first;
            int col = q.front().first.second;
            int len = q.front().second;

            if(row == n-1 && col == n-1){
                return len+1;
            }

            for(int i=0; i<8; i++){
                int nrow = row + drow[i];
                int ncol = col + dcol[i];

                if(nrow>=0 && nrow<n && ncol>=0 && ncol<n && visited.find({nrow,ncol})==visited.end() && grid[nrow][ncol]==0){
                    q.push({{nrow,ncol},len+1});
                    visited.insert(make_pair(nrow,ncol));
                }
            }
            q.pop(); 
        }
        return -1;
    }
};
```
