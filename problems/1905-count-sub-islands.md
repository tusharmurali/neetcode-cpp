# 1905. Count Sub Islands

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-sub-islands/>  
- **NeetCode:** <https://neetcode.io/problems/count-sub-islands>  
- **Video:** <https://www.youtube.com/watch?v=mLpW3qfbNJ8>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

An island in `grid2` is a sub-island if every land cell of that island is also land in `grid1`. We can use DFS to explore each island in `grid2` and simultaneously check if all its cells correspond to land in `grid1`. If any cell in the island exists in `grid2` but not in `grid1`, the entire island is disqualified. We must explore the complete island before deciding, so we continue the DFS even after finding a mismatch.

```cpp
class Solution {
    vector<vector<bool>> visit;

public:
    int countSubIslands(vector<vector<int>>& grid1, vector<vector<int>>& grid2) {
        int ROWS = grid1.size(), COLS = grid1[0].size();
        visit.assign(ROWS, vector<bool>(COLS, false));

        int count = 0;
        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                if (grid2[r][c] && !visit[r][c]) {
                    count += dfs(r, c, grid1, grid2);
                }
            }
        }
        return count;
    }

private:
    bool dfs(int r, int c, vector<vector<int>>& grid1, vector<vector<int>>& grid2) {
        if (r < 0 || c < 0 || r >= grid1.size() || c >= grid1[0].size() ||
            grid2[r][c] == 0 || visit[r][c]) {
            return true;
        }

        visit[r][c] = true;
        bool res = grid1[r][c] == 1;
        res &= dfs(r - 1, c, grid1, grid2);
        res &= dfs(r + 1, c, grid1, grid2);
        res &= dfs(r, c - 1, grid1, grid2);
        res &= dfs(r, c + 1, grid1, grid2);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Breadth First Search

Similar to DFS, we can use BFS to explore islands in `grid2`. Starting from any unvisited land cell, we use a queue to visit all connected land cells level by level. During the traversal, we check if each cell also exists as land in `grid1`. If any cell fails this check, the island is not a sub-island, but we continue exploring to mark all cells as visited.

```cpp
class Solution {
    vector<vector<bool>> visit;
    vector<int> directions = {1, 0, -1, 0, 1};

public:
    int countSubIslands(vector<vector<int>>& grid1, vector<vector<int>>& grid2) {
        int ROWS = grid1.size(), COLS = grid1[0].size();
        visit.assign(ROWS, vector<bool>(COLS, false));
        int count = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid2[r][c] == 1 && !visit[r][c]) {
                    if (bfs(r, c, grid1, grid2)) {
                        count++;
                    }
                }
            }
        }
        return count;
    }

private:
    bool bfs(int r, int c, vector<vector<int>>& grid1, vector<vector<int>>& grid2) {
        queue<pair<int, int>> q;
        q.push({r, c});
        visit[r][c] = true;
        bool res = true;

        while (!q.empty()) {
            auto [cr, cc] = q.front(); q.pop();

            if (grid1[cr][cc] == 0) res = false;

            for (int i = 0; i < 4; i++) {
                int nr = cr + directions[i], nc = cc + directions[i + 1];
                if (nr >= 0 && nr < grid1.size() && nc >= 0 && nc < grid1[0].size() &&
                    grid2[nr][nc] == 1 && !visit[nr][nc]) {
                    visit[nr][nc] = true;
                    q.push({nr, nc});
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Disjoint Set Union

We can use Union-Find to group connected land cells in `grid2` into islands. The key insight is that we also create a special "invalid" node (indexed at `N`, where `N` is the total number of cells). Any land cell in `grid2` that corresponds to water in `grid1` gets unioned with this invalid node. After processing, the number of sub-islands equals the total land cells minus the number of union operations performed (since each union either merges two components or marks one as invalid).

```cpp
class DSU {
    vector<int> Parent, Size;

public:
    DSU(int n) {
        Parent.resize(n + 1);
        Size.assign(n + 1, 1);
        for (int i = 0; i <= n; i++) Parent[i] = i;
    }

    int find(int node) {
        if (Parent[node] != node) Parent[node] = find(Parent[node]);
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
};

class Solution {
public:
    int countSubIslands(vector<vector<int>>& grid1, vector<vector<int>>& grid2) {
        int ROWS = grid1.size(), COLS = grid1[0].size(), N = ROWS * COLS;
        DSU dsu(N);

        int land = 0, unions = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (!grid2[r][c]) continue;
                land++;
                if (r + 1 < ROWS && grid2[r + 1][c])
                    unions += dsu.unionSets(r * COLS + c, (r + 1) * COLS + c);
                if (c + 1 < COLS && grid2[r][c + 1])
                    unions += dsu.unionSets(r * COLS + c, r * COLS + c + 1);
                if (!grid1[r][c])
                    unions += dsu.unionSets(r * COLS + c, N);
            }
        }
        return land - unions;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## Standalone solution file (`cpp/1905-count-sub-islands.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int countSubIslands(vector<vector<int>>& grid1, vector<vector<int>>& grid2) {
        const int ROWS = grid1.size(), COLS = grid1[0].size();
        set<int> visit;
        
        function<bool(int, int)> dfs = [&] (int r, int c) -> bool {
            if (
                r < 0
                || c < 0
                || r == ROWS
                || c == COLS
                || grid2[r][c] == 0
                || visit.count(r*COLS + c)
            )
                return true;
            
            visit.insert(r*COLS + c);
            bool res = true;
            if(grid1[r][c] == 0)
                res = false;
            
            res = dfs(r - 1, c) && res;
            res = dfs(r + 1, c) && res;
            res = dfs(r, c - 1) && res;
            res = dfs(r, c + 1) && res;
            return res;
        };
        
        int count = 0;
        for(int r = 0; r < ROWS; r++)
            for(int c = 0; c < COLS; c++)
                if(grid2[r][c] && !visit.count(r*COLS + c) && dfs(r, c))
                    count += 1;
        return count;
    }
};
```
