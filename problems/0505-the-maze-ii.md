# 505. The Maze II

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/the-maze-ii/>  
- **NeetCode:** <https://neetcode.io/problems/the-maze-ii>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Unlike Maze I where we just need to determine reachability, here we need to find the shortest distance. The ball rolls until it hits a wall, and each cell it passes counts as one unit of distance.

We can use DFS with distance tracking: maintain a distance matrix where each cell stores the shortest known distance to reach it. When we find a shorter path to a stopping position, update the distance and continue exploring from there.

```cpp
class Solution {
public:
    int shortestDistance(vector<vector<int>>& maze, vector<int>& start, vector<int>& destination) {
        vector<vector<int>> distance(maze.size(), vector<int>(maze[0].size(), INT_MAX));
        distance[start[0]][start[1]] = 0;
        dfs(maze, start[0], start[1], distance);
        return distance[destination[0]][destination[1]] == INT_MAX
                   ? -1
                   : distance[destination[0]][destination[1]];
    }

private:
    int dirs[4][2] = {{0, 1}, {0, -1}, {-1, 0}, {1, 0}};

    void dfs(vector<vector<int>>& maze, int sr, int sc, vector<vector<int>>& distance) {
        int m = maze.size(), n = maze[0].size();
        for (auto& dir : dirs) {
            int x = sr + dir[0];
            int y = sc + dir[1];
            int count = 0;
            while (x >= 0 && y >= 0 && x < m && y < n && maze[x][y] == 0) {
                x += dir[0];
                y += dir[1];
                count++;
            }
            if (distance[sr][sc] + count < distance[x - dir[0]][y - dir[1]]) {
                distance[x - dir[0]][y - dir[1]] = distance[sr][sc] + count;
                dfs(maze, x - dir[0], y - dir[1], distance);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n \cdot max(m,n))$
- Space complexity: $O(m \cdot n)$

> Where $m$ and $n$ are the number of rows and columns in `maze`.

## 2. Breadth First Search

BFS can also solve this problem, but unlike typical BFS for shortest path, we cannot stop when we first reach the destination. This is because the ball rolls varying distances, so the first path to reach a position might not be the shortest.

Instead, we use BFS with distance relaxation: whenever we find a shorter path to a stopping position, we update the distance and add it back to the queue for further exploration.

```cpp
class Solution {
public:
    int shortestDistance(vector<vector<int>>& maze, vector<int>& start, vector<int>& destination) {
        int m = maze.size(), n = maze[0].size();
        vector<vector<int>> distance(m, vector<int>(n, INT_MAX));
        distance[start[0]][start[1]] = 0;
        int dirs[4][2] = {{0, 1}, {0, -1}, {-1, 0}, {1, 0}};

        queue<pair<int, int>> q;
        q.push({start[0], start[1]});
        while (!q.empty()) {
            auto [sr, sc] = q.front();
            q.pop();
            for (auto& dir : dirs) {
                int x = sr + dir[0];
                int y = sc + dir[1];
                int count = 0;
                while (x >= 0 && y >= 0 && x < m && y < n && maze[x][y] == 0) {
                    x += dir[0];
                    y += dir[1];
                    count++;
                }

                if (distance[sr][sc] + count < distance[x - dir[0]][y - dir[1]]) {
                    distance[x - dir[0]][y - dir[1]] = distance[sr][sc] + count;
                    q.push({x - dir[0], y - dir[1]});
                }
            }
        }
        return distance[destination[0]][destination[1]] == INT_MAX
                   ? -1
                   : distance[destination[0]][destination[1]];
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n \cdot (m + n))$
- Space complexity: $O(m \cdot n)$

> Where $m$ and $n$ are the number of rows and columns in `maze`.

## 3. Dijkstra's Algorithm

Since edge weights (rolling distances) vary, Dijkstra's algorithm is a natural fit. The key insight is that once we process a position with Dijkstra (after extracting it with the minimum distance), we have found the shortest path to that position.

This version uses a simple implementation where we scan the entire distance matrix to find the unvisited position with minimum distance. While correct, this approach is slower than using a priority queue.

```cpp
class Solution {
public:
    int shortestDistance(vector<vector<int>>& maze, vector<int>& start, vector<int>& destination) {
        int m = maze.size(), n = maze[0].size();
        vector<vector<int>> distance(m, vector<int>(n, INT_MAX));
        vector<vector<bool>> visited(m, vector<bool>(n, false));
        distance[start[0]][start[1]] = 0;
        dijkstra(maze, distance, visited);
        return distance[destination[0]][destination[1]] == INT_MAX
                   ? -1
                   : distance[destination[0]][destination[1]];
    }

private:
    pair<int, int> minDistance(vector<vector<int>>& distance, vector<vector<bool>>& visited) {
        pair<int, int> minCell = {-1, -1};
        int minVal = INT_MAX;

        for (int i = 0; i < distance.size(); i++) {
            for (int j = 0; j < distance[0].size(); j++) {
                if (!visited[i][j] && distance[i][j] < minVal) {
                    minCell = {i, j};
                    minVal = distance[i][j];
                }
            }
        }

        return minCell;
    }

    void dijkstra(vector<vector<int>>& maze, vector<vector<int>>& distance,
                  vector<vector<bool>>& visited) {
        int m = maze.size(), n = maze[0].size();
        int dirs[4][2] = {{0, 1}, {0, -1}, {-1, 0}, {1, 0}};
        while (true) {
            auto [sr, sc] = minDistance(distance, visited);
            if (sr < 0) {
                break;
            }
            visited[sr][sc] = true;
            for (auto& dir : dirs) {
                int x = sr + dir[0];
                int y = sc + dir[1];
                int count = 0;
                while (x >= 0 && y >= 0 && x < m && y < n && maze[x][y] == 0) {
                    x += dir[0];
                    y += dir[1];
                    count++;
                }

                if (distance[sr][sc] + count < distance[x - dir[0]][y - dir[1]]) {
                    distance[x - dir[0]][y - dir[1]] = distance[sr][sc] + count;
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O((mn)^2)$
- Space complexity: $O(mn)$

> Where $m$ and $n$ are the number of rows and columns in `maze`.

## 4. Dijkstra's Algorithm and Priority Queue

Using a priority queue (min-heap) optimizes Dijkstra's algorithm by efficiently extracting the position with the minimum distance. Instead of scanning the entire matrix, we simply pop from the heap.

When we pop a position from the heap, if its distance is already worse than what we have recorded, we skip it (this handles duplicate entries). Otherwise, we explore all four directions and add newly discovered shorter paths to the heap.

```cpp
class Solution {
public:
    int shortestDistance(vector<vector<int>>& maze, vector<int>& start, vector<int>& destination) {
        int m = maze.size();
        int n = maze[0].size();
        vector<vector<int>> distance(m, vector<int>(n, INT_MAX));
        distance[start[0]][start[1]] = 0;
        dijkstra(maze, start, distance);
        return distance[destination[0]][destination[1]] == INT_MAX ? -1 : distance[destination[0]][destination[1]];
    }

private:
    void dijkstra(vector<vector<int>>& maze, vector<int>& start, vector<vector<int>>& distance) {
        int m = maze.size();
        int n = maze[0].size();
        vector<vector<int>> dirs = {{0, 1}, {0, -1}, {-1, 0}, {1, 0}};

        // Min-heap: {distance, x, y}
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq;
        pq.push({0, start[0], start[1]});

        while (!pq.empty()) {
            vector<int> s = pq.top();
            pq.pop();
            int dist = s[0], sx = s[1], sy = s[2];

            if (distance[sx][sy] < dist)
                continue;

            for (auto& dir : dirs) {
                int x = sx + dir[0];
                int y = sy + dir[1];
                int count = 0;

                while (x >= 0 && y >= 0 && x < m && y < n && maze[x][y] == 0) {
                    x += dir[0];
                    y += dir[1];
                    count++;
                }

                if (distance[sx][sy] + count < distance[x - dir[0]][y - dir[1]]) {
                    distance[x - dir[0]][y - dir[1]] = distance[sx][sy] + count;
                    pq.push({distance[x - dir[0]][y - dir[1]], x - dir[0], y - dir[1]});
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(mn \cdot \log(mn))$
- Space complexity: $O(m \cdot n)$

> Where $m$ and $n$ are the number of rows and columns in `maze`.
