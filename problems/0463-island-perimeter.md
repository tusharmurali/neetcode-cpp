# 463. Island Perimeter

- **Difficulty:** Easy  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/island-perimeter/>  
- **NeetCode:** <https://neetcode.io/problems/island-perimeter>  
- **Video:** <https://www.youtube.com/watch?v=fISIuAFRM2s>  
- **Video approach:** 1. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search ▶ video

The perimeter of an island comes from the edges of land cells that touch either water or the grid boundary. Using DFS, we can traverse all connected land cells starting from any land cell. Each time we step outside the grid or hit water, we've found one edge of the perimeter. By recursively exploring in all four directions and counting these boundary crossings, we accumulate the total perimeter.

```cpp
class Solution {
private:
    vector<vector<int>> grid;
    vector<vector<bool>> visited;
    int rows, cols;

    int dfs(int i, int j) {
        if (i < 0 || j < 0 || i >= rows ||
            j >= cols || grid[i][j] == 0) {
            return 1;
        }
        if (visited[i][j]) {
            return 0;
        }

        visited[i][j] = true;
        return dfs(i, j + 1) + dfs(i + 1, j) +
               dfs(i, j - 1) + dfs(i - 1, j);
    }

public:
    int islandPerimeter(vector<vector<int>>& grid) {
        this->grid = grid;
        rows = grid.size();
        cols = grid[0].size();
        visited = vector<vector<bool>>(rows, vector<bool>(cols, false));

        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                if (grid[i][j] == 1) {
                    return dfs(i, j);
                }
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the grid.

## 2. Breadth First Search

BFS offers a level-by-level traversal of the island. Starting from any land cell, we explore its neighbors using a queue. The key observation remains the same: each neighbor that is water or out of bounds contributes one unit to the perimeter. By processing each land cell once and checking its four directions, we count all perimeter edges.

```cpp
class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size();
        vector<vector<bool>> visited(rows, vector<bool>(cols, false));
        int directions[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                if (grid[i][j] == 1) {
                    queue<pair<int, int>> q;
                    q.push({i, j});
                    visited[i][j] = true;
                    int perimeter = 0;

                    while (!q.empty()) {
                        auto [x, y] = q.front();
                        q.pop();

                        for (auto& dir : directions) {
                            int nx = x + dir[0], ny = y + dir[1];
                            if (nx < 0 || ny < 0 || nx >= rows ||
                                ny >= cols || grid[nx][ny] == 0) {
                                perimeter++;
                            } else if (!visited[nx][ny]) {
                                visited[nx][ny] = true;
                                q.push({nx, ny});
                            }
                        }
                    }
                    return perimeter;
                }
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the grid.

## 3. Iteration - I

Instead of graph traversal, we can directly iterate through every cell. For each land cell, we check all four directions. If a neighbor is water or out of bounds, that direction contributes to the perimeter. This approach processes each cell independently, making it straightforward and efficient.

```cpp
class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size(), res = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    res += (i + 1 >= m || grid[i + 1][j] == 0) ? 1 : 0;
                    res += (j + 1 >= n || grid[i][j + 1] == 0) ? 1 : 0;
                    res += (i - 1 < 0 || grid[i - 1][j] == 0) ? 1 : 0;
                    res += (j - 1 < 0 || grid[i][j - 1] == 0) ? 1 : 0;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns in the grid.

## 4. Iteration - II

Every land cell contributes `4` to the perimeter initially. However, when two land cells are adjacent, they share an edge, and both cells lose one perimeter unit on that shared side. So for each adjacent pair, we subtract `2` from the total. By only checking the top and left neighbors while iterating, we count each adjacency exactly once.

```cpp
class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        int res = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c]) {
                    res += 4;
                    if (r && grid[r - 1][c]) {
                        res -= 2;
                    }
                    if (c && grid[r][c - 1]) {
                        res -= 2;
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns in the grid.

## Standalone solution file (`cpp/0463-island-perimeter.cpp` in the NeetCode repo)

```cpp
// Time complexity is O(M*N)
// Space complexity is O(1)

class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
      int m = grid.size();
      int n = grid[0].size();
      
      int prem = 0;
      
      for(int i = 0 ; i < m ; i++)
      {
        for(int j = 0 ; j < n ; j++)
        {
          if(grid[i][j] == 1) {
            prem += 4;
          
            if(j > 0 && grid[i][j-1] == 1) prem -=2;
            if(i >0 && grid[i-1][j] == 1) prem -=2;

          }
        }
      }
      
      return prem;
    }
};
```
