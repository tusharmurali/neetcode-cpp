# 2421. Number of Good Paths

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-good-paths/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-good-paths>  
- **Video:** <https://www.youtube.com/watch?v=rv2GBYQm7xM>  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

A good path starts and ends with nodes having the same value, and all nodes along the path have values less than or equal to that value. For each node, we can run a `dfs` to explore all reachable nodes where path values stay at or below the starting node's value. We count nodes with the same value as valid endpoints.

```cpp
class Solution {
public:
    int numberOfGoodPaths(vector<int>& vals, vector<vector<int>>& edges) {
        int n = vals.size();
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        int res = 0;
        for (int node = 0; node < n; node++) {
            res += dfs(node, node, -1, vals, adj);
        }
        return res;
    }

private:
    int dfs(int node, int startNode, int parent, vector<int>& vals, vector<vector<int>>& adj) {
        if (vals[node] > vals[startNode]) {
            return 0;
        }

        int res = 0;
        if (vals[node] == vals[startNode] && node >= startNode) {
            res += 1;
        }

        for (int child : adj[node]) {
            if (child == parent) {
                continue;
            }
            res += dfs(child, startNode, node, vals, adj);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Brute Force (BFS)

This is the same logic as the `dfs` approach but uses `bfs` instead. Starting from each node, we explore all reachable nodes using a queue, only visiting neighbors with values at or below the starting node's value. We count valid endpoints with matching values.

```cpp
class Solution {
public:
    int numberOfGoodPaths(vector<int>& vals, vector<vector<int>>& edges) {
        int n = vals.size();
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        int res = 0;
        for (int startNode = 0; startNode < n; startNode++) {
            queue<int> q;
            unordered_set<int> visited;
            q.push(startNode);
            visited.insert(startNode);
            int count = 0;

            while (!q.empty()) {
                int node = q.front();
                q.pop();
                if (vals[node] == vals[startNode] && node >= startNode) {
                    count++;
                }

                for (int child : adj[node]) {
                    if (visited.find(child) == visited.end() && vals[child] <= vals[startNode]) {
                        visited.insert(child);
                        q.push(child);
                    }
                }
            }

            res += count;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Disjoint Set Union

Processing nodes in increasing order of their values allows us to incrementally build connected components. When we process nodes with value `v`, we union them with their neighbors that have values at most `v`. At each step, nodes with value `v` in the same component can form good paths with each other. The number of such paths equals the count of same-valued nodes per component.

```cpp
class DSU {
public:
    vector<int> parent, size;

    DSU(int n) {
        parent.resize(n + 1);
        size.resize(n + 1, 1);
        for (int i = 0; i <= n; i++) parent[i] = i;
    }

    int find(int node) {
        if (parent[node] != node) parent[node] = find(parent[node]);
        return parent[node];
    }

    bool unite(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (size[pu] >= size[pv]) {
            size[pu] += size[pv];
            parent[pv] = pu;
        } else {
            size[pv] += size[pu];
            parent[pu] = pv;
        }
        return true;
    }
};

class Solution {
public:
    int numberOfGoodPaths(vector<int>& vals, vector<vector<int>>& edges) {
        int n = vals.size();
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        map<int, vector<int>> valToIndex;
        for (int i = 0; i < n; i++) valToIndex[vals[i]].push_back(i);

        DSU dsu(n);
        int res = 0;

        for (auto& [val, nodes] : valToIndex) {
            for (int& i : nodes) {
                for (int& nei : adj[i]) {
                    if (vals[nei] <= vals[i]) dsu.unite(nei, i);
                }
            }

            unordered_map<int, int> count;
            for (int& i : nodes) {
                int root = dsu.find(i);
                count[root]++;
                res += count[root];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Disjoint Set Union (Union By Value)

Instead of grouping nodes by value, we can sort the edges by the maximum value of their endpoints. Processing edges in this order ensures that when we connect two components, we only form new good paths when both component representatives have the same value. Each component tracks how many nodes share the maximum value, allowing us to compute new paths during union operations.

```cpp
class DSU {
    vector<int> parent, count, vals;

public:
    DSU(int n, vector<int>& vals) : vals(vals), parent(n), count(n, 1) {
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int node) {
        if (parent[node] != node) {
            parent[node] = find(parent[node]);
        }
        return parent[node];
    }

    int unionNodes(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) {
            return 0;
        }
        if (vals[pu] < vals[pv]) {
            parent[pu] = pv;
        } else if (vals[pu] > vals[pv]) {
            parent[pv] = pu;
        } else {
            parent[pv] = pu;
            int result = count[pu] * count[pv];
            count[pu] += count[pv];
            return result;
        }
        return 0;
    }
};

class Solution {
public:
    int numberOfGoodPaths(vector<int>& vals, vector<vector<int>>& edges) {
        int n = vals.size();
        DSU dsu(n, vals);

        // Sort edges based on max value of the two nodes
        sort(edges.begin(), edges.end(), [&](auto& a, auto& b) {
            return max(vals[a[0]], vals[a[1]]) < max(vals[b[0]], vals[b[1]]);
        });

        int res = n; // Each node alone is a good path
        for (auto& edge : edges) {
            res += dsu.unionNodes(edge[0], edge[1]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n\log n)$
- Space complexity: $O(n)$
