# 2492. Minimum Score of a Path Between Two Cities

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-score-of-a-path-between-two-cities>  
- **Video:** <https://www.youtube.com/watch?v=K7-mXA0irhY>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

The problem asks for the minimum edge weight on any path from city `1` to city `n`, where we can revisit edges and nodes. The key realization is that since we can traverse any edge multiple times, we're essentially looking for the minimum edge weight in the entire connected component containing city `1`. If an edge is reachable from city `1`, we can always include it in our path by going there and back.

```cpp
class Solution {
public:
    vector<vector<pair<int, int>>> adj;
    vector<bool> visit;
    int res;

    int minScore(int n, vector<vector<int>>& roads) {
        adj.resize(n + 1);
        visit.resize(n + 1, false);
        res = INT_MAX;

        for (auto& road : roads) {
            adj[road[0]].push_back({road[1], road[2]});
            adj[road[1]].push_back({road[0], road[2]});
        }

        dfs(1);
        return res;
    }

    void dfs(int node) {
        if (visit[node]) return;
        visit[node] = true;

        for (auto& edge : adj[node]) {
            res = min(res, edge.second);
            dfs(edge.first);
        }
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Breadth First Search

BFS achieves the same goal as DFS by exploring all reachable nodes level by level. Since we need to find the minimum edge weight in the connected component containing node `1`, BFS works equally well. We process each node, check all its edges, and track the smallest weight seen.

```cpp
class Solution {
public:
    int minScore(int n, vector<vector<int>>& roads) {
        vector<vector<pair<int, int>>> adj(n + 1);
        for (auto& road : roads) {
            adj[road[0]].emplace_back(road[1], road[2]);
            adj[road[1]].emplace_back(road[0], road[2]);
        }

        int res = INT_MAX;
        vector<bool> visit(n + 1, false);
        queue<int> q;
        q.push(1);
        visit[1] = true;

        while (!q.empty()) {
            int node = q.front();q.pop();
            for (auto& [nei, dist] : adj[node]) {
                res = min(res, dist);
                if (!visit[nei]) {
                    visit[nei] = true;
                    q.push(nei);
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 3. Iterative DFS

This is the same approach as recursive DFS, but using an explicit stack instead of the call stack. This avoids potential stack overflow issues for very deep graphs and gives us more control over the traversal.

```cpp
class Solution {
public:
    int minScore(int n, vector<vector<int>>& roads) {
        vector<vector<pair<int, int>>> adj(n + 1);
        for (auto& road : roads) {
            adj[road[0]].emplace_back(road[1], road[2]);
            adj[road[1]].emplace_back(road[0], road[2]);
        }

        int res = INT_MAX;
        vector<bool> visit(n + 1, false);
        stack<int> stk;
        stk.push(1);
        visit[1] = true;

        while (!stk.empty()) {
            int node = stk.top();stk.pop();
            for (auto& [nei, dist] : adj[node]) {
                res = min(res, dist);
                if (!visit[nei]) {
                    visit[nei] = true;
                    stk.push(nei);
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 4. Disjoint Set Union

Union-Find provides another way to identify which edges belong to the same connected component as node `1`. First, we union all nodes connected by edges. Then, we iterate through all edges and check if they belong to the same component as node `1`. The minimum weight among those edges is our answer.

```cpp
class DSU {
public:
    vector<int> parent, size;

    DSU(int n) {
        parent.resize(n + 1);
        size.resize(n + 1, 1);
        for (int i = 0; i <= n; i++) {
            parent[i] = i;
        }
    }

    int find(int node) {
        if (parent[node] != node) {
            parent[node] = find(parent[node]);
        }
        return parent[node];
    }

    bool unionSets(int u, int v) {
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
    int minScore(int n, vector<vector<int>>& roads) {
        DSU dsu(n);
        for (auto& road : roads) {
            dsu.unionSets(road[0], road[1]);
        }

        int res = INT_MAX;
        int root = dsu.find(1);
        for (auto& road : roads) {
            if (dsu.find(road[0]) == root) {
                res = min(res, road[2]);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + (E * α(V)))$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph. $α()$ is used for amortized complexity.
