# 733. Flood Fill

- **Difficulty:** Easy  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/flood-fill/>  
- **NeetCode:** <https://neetcode.io/problems/flood-fill>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Flood fill is like using the paint bucket tool in image editors. Starting from a pixel, we want to change its color and spread to all connected pixels of the same original color. This naturally maps to a graph traversal problem where each pixel is a node connected to its four neighbors.

DFS works well here because we recursively explore as far as possible in one direction before backtracking. By changing the color as we visit each pixel, we mark it as visited, preventing infinite loops. If the new color equals the original, we skip the operation entirely to avoid unnecessary work.

```cpp
class Solution {
public:
    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {
        int orig = image[sr][sc];
        if (orig == color) return image;
        m = image.size();
        n = image[0].size();
        dfs(image, sr, sc, orig, color);
        return image;
    }
private:
    int m, n;
    void dfs(vector<vector<int>>& image, int r, int c, int orig, int color) {
        if (r < 0 || r >= m || c < 0 || c >= n || image[r][c] != orig) return;
        image[r][c] = color;
        dfs(image, r + 1, c, orig, color);
        dfs(image, r - 1, c, orig, color);
        dfs(image, r, c + 1, orig, color);
        dfs(image, r, c - 1, orig, color);
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the image.

## 2. Breadth First Search

BFS explores pixels level by level, processing all pixels at distance 1 from the start before those at distance 2, and so on. While DFS dives deep immediately, BFS spreads outward uniformly. Both achieve the same result for flood fill, but BFS uses a queue instead of the call stack.

The key is to color pixels when adding them to the queue, not when processing them. This prevents adding the same pixel multiple times and keeps the queue size manageable.

```cpp
class Solution {
public:
    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {
        int orig = image[sr][sc];
        if (orig == color) return image;
        int m = image.size(), n = image[0].size();
        queue<pair<int,int>> q;
        q.emplace(sr, sc);
        image[sr][sc] = color;
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};

        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (auto &d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && image[nr][nc] == orig) {
                    image[nr][nc] = color;
                    q.emplace(nr, nc);
                }
            }
        }
        return image;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the image.
