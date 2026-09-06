# 417. Pacific Atlantic Water Flow

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/pacific-atlantic-water-flow/>  
- **NeetCode:** <https://neetcode.io/problems/pacific-atlantic-water-flow>  
- **Video:** <https://www.youtube.com/watch?v=s-VkcjHqkGI>  
- **Video approach:** 2. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Brute Force (Backtracking)

For each cell, we try to see **where water can flow** if it starts there.

Rule: water can flow from a cell to a neighbor only if the neighbor’s height is **<= current height** (downhill or flat).

So for every (r, c):

- Run DFS exploring all paths that keep going to **same or lower** heights.
- If during DFS we ever step **out of the grid**:
    - Out of **top/left** boundary ⇒ it can reach the **Pacific**.
    - Out of **bottom/right** boundary ⇒ it can reach the **Atlantic**.
- If both oceans are reachable, include (r, c) in the answer.

To avoid infinite loops, we temporarily mark the current cell as **visited** (here by setting it to `inf`) while exploring, then restore it after backtracking.

```cpp
class Solution {
public:
    int ROWS, COLS;
    bool pacific, atlantic;
    vector<vector<int>> directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        ROWS = heights.size();
        COLS = heights[0].size();
        vector<vector<int>> res;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                pacific = false;
                atlantic = false;
                dfs(heights, r, c, INT_MAX);
                if (pacific && atlantic) {
                    res.push_back({r, c});
                }
            }
        }

        return res;
    }

    void dfs(vector<vector<int>>& heights, int r, int c, int prevVal) {
        if (r < 0 || c < 0) {
            pacific = true;
            return;
        }
        if (r >= ROWS || c >= COLS) {
            atlantic = true;
            return;
        }
        if (heights[r][c] > prevVal) {
            return;
        }

        int tmp = heights[r][c];
        heights[r][c] = INT_MAX;
        for (auto& dir : directions) {
            dfs(heights, r + dir[0], c + dir[1], tmp);
            if (pacific && atlantic) {
                break;
            }
        }
        heights[r][c] = tmp;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * 4 ^ {m * n})$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Depth First Search ▶ video

Instead of starting DFS from every cell (slow), we reverse the thinking:

A cell can reach an ocean **if water can flow from that cell to the ocean** (downhill/flat).
Reverse it: start from the **ocean borders** and move **uphill/flat** (to neighbors with height >= current).
If you can climb from the ocean to a cell, then that cell can flow down to that ocean.

So we do 2 DFS runs:

- From all **Pacific border** cells (top row + left column) → mark all reachable cells in `pac`
- From all **Atlantic border** cells (bottom row + right column) → mark all reachable cells in `atl`

Answer = cells that are in **both** sets.

```cpp
class Solution {
    vector<pair<int, int>> directions = {{1, 0}, {-1, 0},
                                         {0, 1}, {0, -1}};
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int ROWS = heights.size(), COLS = heights[0].size();
        vector<vector<bool>> pac(ROWS, vector<bool>(COLS, false));
        vector<vector<bool>> atl(ROWS, vector<bool>(COLS, false));

        for (int c = 0; c < COLS; ++c) {
            dfs(0, c, pac, heights);
            dfs(ROWS - 1, c, atl, heights);
        }
        for (int r = 0; r < ROWS; ++r) {
            dfs(r, 0, pac, heights);
            dfs(r, COLS - 1, atl, heights);
        }

        vector<vector<int>> res;
        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                if (pac[r][c] && atl[r][c]) {
                    res.push_back({r, c});
                }
            }
        }
        return res;
    }

private:
    void dfs(int r, int c, vector<vector<bool>>& ocean, vector<vector<int>>& heights) {
        ocean[r][c] = true;
        for (auto [dr, dc] : directions) {
            int nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < heights.size() &&
                nc >= 0 && nc < heights[0].size() &&
                !ocean[nr][nc] && heights[nr][nc] >= heights[r][c]) {
                dfs(nr, nc, ocean, heights);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Breadth First Search

Do the same “reverse flow” idea, but with BFS.

A cell can flow to an ocean if you can start from the ocean border and move _backwards_ into the grid using the rule:

- from (r, c) you can go to neighbor (nr, nc) if `heights[nr][nc] >= heights[r][c]`
  (because in the real direction water would flow from higher/equal down to (r, c)).

So:

- Multi-source BFS from all Pacific border cells marks `pac[r][c] = True`
- Multi-source BFS from all Atlantic border cells marks `atl[r][c] = True`
  Cells that are `True` in both are the answer.

```cpp
class Solution {
    vector<pair<int, int>> directions = {{1, 0}, {-1, 0},
                                         {0, 1}, {0, -1}};
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int ROWS = heights.size(), COLS = heights[0].size();
        vector<vector<bool>> pac(ROWS, vector<bool>(COLS, false));
        vector<vector<bool>> atl(ROWS, vector<bool>(COLS, false));

        queue<pair<int, int>> pacQueue, atlQueue;

        for (int c = 0; c < COLS; ++c) {
            pacQueue.push({0, c});
            atlQueue.push({ROWS - 1, c});
        }
        for (int r = 0; r < ROWS; ++r) {
            pacQueue.push({r, 0});
            atlQueue.push({r, COLS - 1});
        }

        bfs(pacQueue, pac, heights);
        bfs(atlQueue, atl, heights);

        vector<vector<int>> res;
        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                if (pac[r][c] && atl[r][c]) {
                    res.push_back({r, c});
                }
            }
        }
        return res;
    }

private:
    void bfs(queue<pair<int, int>>& q, vector<vector<bool>>& ocean,
                                        vector<vector<int>>& heights) {
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            ocean[r][c] = true;
            for (auto [dr, dc] : directions) {
                int nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < heights.size() && nc >= 0 &&
                    nc < heights[0].size() && !ocean[nr][nc] &&
                    heights[nr][nc] >= heights[r][c]) {
                    q.push({nr, nc});
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## Standalone solution file (`cpp/0417-pacific-atlantic-water-flow.cpp` in the NeetCode repo)

```cpp
/*
    Top & left pacific, bottom & right atlantic, determine spots that flow to both

    Instead go outside in, from oceans to spots where rain could flow from
    Faster bc avoids repeated work: cells along a path can also reach that ocean

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int m = heights.size();
        int n = heights[0].size();
        
        vector<vector<bool>> pacific(m, vector<bool>(n));
        vector<vector<bool>> atlantic(m, vector<bool>(n));
        
        for (int i = 0; i < m; i++) {
            dfs(heights, pacific, i, 0, m, n);
            dfs(heights, atlantic, i, n - 1, m, n);
        }
        
        for (int j = 0; j < n; j++) {
            dfs(heights, pacific, 0, j, m, n);
            dfs(heights, atlantic, m - 1, j, m, n);
        }
        
        vector<vector<int>> result;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (pacific[i][j] && atlantic[i][j]) {
                    result.push_back({i, j});
                }
            }
        }
        
        return result;
    }
private:
    void dfs(vector<vector<int>>& heights, vector<vector<bool>>& visited,
        int i, int j, int m, int n) {
        
        visited[i][j] = true;
        
        if (i > 0 && !visited[i - 1][j] && heights[i - 1][j] >= heights[i][j]) {
            dfs(heights, visited, i - 1, j, m, n);
        }
        if (i < m - 1 && !visited[i + 1][j] && heights[i + 1][j] >= heights[i][j]) {
            dfs(heights, visited, i + 1, j, m, n);
        }
        if (j > 0 && !visited[i][j - 1] && heights[i][j - 1] >= heights[i][j]) {
            dfs(heights, visited, i, j - 1, m, n);
        }
        if (j < n - 1 && !visited[i][j + 1] && heights[i][j + 1] >= heights[i][j]) {
            dfs(heights, visited, i, j + 1, m, n);
        }
    }
};


/*
    BFS solution
*/

class Solution {
private:
    int rows, cols;

    void bfs(queue<pair<int, int>>& q, vector<vector<bool>>& visited, vector<vector<int>>& heights) {

        vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
        while (!q.empty()) {
            auto [row, col] = q.front();
            q.pop();
            for (const auto &direction : directions) {
                int newRow = row + direction.first;
                int newCol = col + direction.second;
                if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols && !visited[newRow][newCol] 
                               && heights[newRow][newCol] >= heights[row][col]) {
                    q.push({newRow, newCol});
                    visited[newRow][newCol] = true;
                }
            }
        }
    }
    
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        rows = heights.size();
        cols = heights[0].size();
        vector<vector<int>> results;
        queue<pair<int, int>> pacificQueue;
        queue<pair<int, int>> atlanticQueue;
        vector<vector<bool>> pacific(rows, vector<bool>(cols, false));
        vector<vector<bool>> atlantic(rows, vector<bool>(cols, false));

        for (int row = 0; row < rows; ++row) {
            pacific[row][0] = true;
            atlantic[row][cols - 1] = true;
            pacificQueue.push({row, 0});
            atlanticQueue.push({row, cols-1});
        }

        for (int col = 0; col < cols; ++col) {
            pacific[0][col] = true;
            atlantic[rows - 1][col] = true;
            pacificQueue.push({0, col});
            atlanticQueue.push({rows - 1, col});
        }

        bfs(pacificQueue, pacific, heights);
        bfs(atlanticQueue, atlantic, heights);

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (pacific[row][col] && atlantic[row][col]) {
                    results.push_back({row, col});
                }
            }
        }

        return results;
    
    }
};
```
