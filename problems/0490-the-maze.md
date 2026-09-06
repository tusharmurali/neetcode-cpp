# 490. The Maze

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/the-maze/>  
- **NeetCode:** <https://neetcode.io/problems/the-maze>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Unlike typical grid problems where movement is one cell at a time, the ball in this maze rolls continuously in one direction until it hits a wall. This means the ball can only stop at specific positions: cells adjacent to walls.

We can model this as a graph where each stopping position is a node, and edges connect positions reachable by rolling in any of the four directions. DFS explores all reachable stopping positions to determine if the destination is among them.

```cpp
class Solution {
public:
    bool dfs(int m, int n, vector<vector<int>>& maze, vector<int> curr, vector<int>& destination,
             vector<vector<bool>>& visit) {
        if (visit[curr[0]][curr[1]]) {
            return false;
        }
        if (curr[0] == destination[0] && curr[1] == destination[1]) {
            return true;
        }

        visit[curr[0]][curr[1]] = true;
        vector<int> dirX{0, 1, 0, -1};
        vector<int> dirY{-1, 0, 1, 0};

        for (int i = 0; i < 4; i++) {
            int r = curr[0], c = curr[1];
            // Move the ball in the chosen direction until it can.
            while (r >= 0 && r < m && c >= 0 && c < n && maze[r][c] == 0) {
                r += dirX[i];
                c += dirY[i];
            }
            // Revert the last move to get the cell to which the ball rolls.
            if (dfs(m, n, maze, {r - dirX[i], c - dirY[i]}, destination, visit)) {
                return true;
            }
        }
        return false;
    }

    bool hasPath(vector<vector<int>>& maze, vector<int>& start, vector<int>& destination) {
        int m = maze.size();
        int n = maze[0].size();
        vector<vector<bool>> visit(m, vector<bool>(n));
        return dfs(m, n, maze, start, destination, visit);
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n \cdot (m + n))$
- Space complexity: $O(m \cdot n)$

> Where $m$ and $n$ are the number of rows and columns in `maze`.

## 2. Breadth First Search

BFS offers an alternative traversal strategy that explores all stopping positions at each "distance level" before moving deeper. While DFS might go deep into one path before backtracking, BFS systematically explores positions in order of how many rolls it takes to reach them.

The core rolling mechanic remains the same: the ball rolls until hitting a wall, and we only consider positions where the ball actually stops.

```cpp
class Solution {
public:
    bool hasPath(vector<vector<int>>& maze, vector<int>& start, vector<int>& destination) {
        int m = maze.size();
        int n = maze[0].size();
        vector<vector<bool>> visit(m, vector<bool>(n, false));
        vector<int> dirX{0, 1, 0, -1};
        vector<int> dirY{-1, 0, 1, 0};

        queue<vector<int>> q;
        q.push(start);
        visit[start[0]][start[1]] = true;

        while (!q.empty()) {
            vector<int> curr = q.front();
            q.pop();
            if (curr[0] == destination[0] && curr[1] == destination[1]) {
                return true;
            }

            for (int i = 0; i < 4; i++) {
                int r = curr[0];
                int c = curr[1];
                // Move the ball in the chosen direction until it can.
                while (r >= 0 && r < m && c >= 0 && c < n && maze[r][c] == 0) {
                    r += dirX[i];
                    c += dirY[i];
                }
                // Revert the last move to get the cell to which the ball rolls.
                r -= dirX[i];
                c -= dirY[i];
                if (!visit[r][c]) {
                    q.push({r, c});
                    visit[r][c] = true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n \cdot (m + n))$
- Space complexity: $O(m \cdot n)$

> Where $m$ and $n$ are the number of rows and columns in `maze`.
