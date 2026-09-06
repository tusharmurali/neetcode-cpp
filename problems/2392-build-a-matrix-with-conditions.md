# 2392. Build a Matrix With Conditions

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/build-a-matrix-with-conditions/>  
- **NeetCode:** <https://neetcode.io/problems/build-a-matrix-with-conditions>  
- **Video:** <https://www.youtube.com/watch?v=khTKB1PzCuw>  

[← Back to index](../INDEX.md)

## 1. Topological Sort (DFS)

The problem asks us to place numbers `1` to `k` in a `k x k` matrix such that certain numbers appear above others (row conditions) and certain numbers appear to the left of others (column conditions). This is essentially two independent ordering problems: one for rows and one for columns.

Each set of conditions forms a directed graph where an edge from A to B means A must come before B. Finding a valid ordering that satisfies all constraints is exactly what topological sort does. If there's a cycle in either graph, no valid ordering exists and we return an empty matrix.

```cpp
class Solution {
public:
    vector<vector<int>> buildMatrix(int k, vector<vector<int>>& rowConditions, vector<vector<int>>& colConditions) {
        vector<int> rowOrder = topoSort(k, rowConditions);
        if (rowOrder.empty()) return {};
        vector<int> colOrder = topoSort(k, colConditions);
        if (colOrder.empty()) return {};

        unordered_map<int, int> valToRow, valToCol;
        for (int i = 0; i < rowOrder.size(); i++) {
            valToRow[rowOrder[i]] = i;
        }
        for (int i = 0; i < colOrder.size(); i++) {
            valToCol[colOrder[i]] = i;
        }

        vector<vector<int>> res(k, vector<int>(k, 0));
        for (int num = 1; num <= k; num++) {
            int r = valToRow[num];
            int c = valToCol[num];
            res[r][c] = num;
        }
        return res;
    }

private:
    unordered_set<int> visit;
    unordered_set<int> path;
    vector<int> order;

    vector<int> topoSort(int k, vector<vector<int>>& edges) {
        unordered_map<int, vector<int>> adj;
        for (int i = 1; i <= k; i++) {
            adj[i] = {};
        }
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }

        visit.clear();
        path.clear();
        order.clear();
        for (int i = 1; i <= k; i++) {
            if (visit.find(i) == visit.end()) {
                if (!dfs(i, adj)) {
                    return {};
                }
            }
        }

        reverse(order.begin(), order.end());
        return order;
    }

    bool dfs(int src, unordered_map<int, vector<int>>& adj) {
        if (path.find(src) != path.end()) return false;
        if (visit.find(src) != visit.end()) return true;

        visit.insert(src);
        path.insert(src);
        for (int nei : adj[src]) {
            if (!dfs(nei, adj)) {
                return false;
            }
        }
        path.erase(src);
        order.push_back(src);
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(k ^ 2 + n + m)$
- Space complexity:
    - $O(k + n + m)$ extra space.
    - $O(k ^ 2)$ space for the output matrix.

> Where $n$ is the size of the array $rowConditions$, $m$ is the size of the array $colConditions$, and $k$ is the size of the output matrix.

## 2. Topological Sort (Kahn's Algorithm)

This approach solves the same problem using Kahn's algorithm (BFS-based topological sort) instead of DFS. The key insight remains the same: we need valid orderings for both rows and columns. Kahn's algorithm processes nodes with zero incoming edges first, which naturally produces a valid topological order when no cycle exists.

If we process fewer than `k` nodes, it means there's a cycle in the graph and no valid ordering is possible.

```cpp
class Solution {
public:
    vector<vector<int>> buildMatrix(int k, vector<vector<int>>& rowConditions, vector<vector<int>>& colConditions) {
        vector<int> rowOrder = topoSort(k, rowConditions);
        if (rowOrder.size() != k) return {};

        vector<int> colOrder = topoSort(k, colConditions);
        if (colOrder.size() != k) return {};

        vector<vector<int>> res(k, vector<int>(k, 0));
        vector<int> colIndex(k + 1);
        for (int i = 0; i < k; i++) {
            colIndex[colOrder[i]] = i;
        }
        for (int i = 0; i < k; i++) {
            res[i][colIndex[rowOrder[i]]] = rowOrder[i];
        }
        return res;
    }

private:
    vector<int> topoSort(int k, vector<vector<int>>& edges) {
        vector<int> indegree(k + 1, 0);
        vector<vector<int>> adj(k + 1);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            indegree[edge[1]]++;
        }

        queue<int> q;
        vector<int> order;
        for (int i = 1; i <= k; i++) {
            if (indegree[i] == 0) {
                q.push(i);
            }
        }

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            order.push_back(node);

            for (int nei : adj[node]) {
                indegree[nei]--;
                if (indegree[nei] == 0) {
                    q.push(nei);
                }
            }
        }

        if (order.size() != k) return {};
        return order;
    }
};
```

**Complexity**

- Time complexity: $O(k ^ 2 + n + m)$
- Space complexity:
    - $O(k + n + m)$ extra space.
    - $O(k ^ 2)$ space for the output matrix.

> Where $n$ is the size of the array $rowConditions$, $m$ is the size of the array $colConditions$, and $k$ is the size of the output matrix.
