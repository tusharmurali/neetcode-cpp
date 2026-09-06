# 1557. Minimum Number of Vertices to Reach all Nodes

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-vertices-to-reach-all-nodes>  
- **Video:** <https://www.youtube.com/watch?v=TLzcum7vrTc>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We want to find the smallest set of vertices from which all other vertices are reachable. A vertex must be in this set if no other vertex can reach it, meaning it has no incoming edges.

Using `dfs`, we traverse from each unvisited `node` and mark all reachable nodes. Any `node` that gets reached from another `node` can be removed from our candidate set. The nodes that remain are those with no incoming edges.

```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }

        unordered_set<int> res;
        vector<bool> visited(n, false);
        for (int i = 0; i < n; i++) res.insert(i);

        function<void(int)> dfs = [&](int node) {
            visited[node] = true;
            for (int& nei : adj[node]) {
                if (!visited[nei]) dfs(nei);
                res.erase(nei);
            }
        };

        for (int i = 0; i < n; i++) {
            if (!visited[i]) dfs(i);
        }
        return vector<int>(res.begin(), res.end());
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Iterative DFS

This is the same approach as recursive `dfs` but uses an explicit `stack` to avoid recursion. We process nodes iteratively, marking each visited `node` and removing any `node` that has an incoming edge from our candidate set.

```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }

        vector<bool> res(n, true), visited(n, false);
        stack<int> stack;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                stack.push(i);
                while (!stack.empty()) {
                    int node = stack.top();
                    stack.pop();
                    if (visited[node]) continue;
                    visited[node] = true;
                    for (int nei : adj[node]) {
                        if (!visited[nei]) stack.push(nei);
                        res[nei] = false;
                    }
                }
            }
        }

        vector<int> result;
        for (int i = 0; i < n; i++) {
            if (res[i]) result.push_back(i);
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 3. Indegree Count

A vertex needs to be in our starting set only if it cannot be reached from any other vertex. This happens exactly when the vertex has no incoming edges. We can track which vertices have incoming edges by building a list of sources for each destination.

```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        vector<vector<int>> incoming(n);
        for (auto& edge : edges) {
            incoming[edge[1]].push_back(edge[0]);
        }

        vector<int> res;
        for (int i = 0; i < n; i++) {
            if (incoming[i].empty()) {
                res.push_back(i);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 4. Indegree Count (Optimal)

We do not need to store the actual source vertices for each destination. We only care whether a vertex has at least one incoming edge. A simple boolean array is sufficient: mark each destination as having an incoming edge, then return all vertices that were never marked.

```cpp
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        vector<bool> indegree(n, false);
        for (const auto& edge : edges) {
            indegree[edge[1]] = true;
        }

        vector<int> res;
        for (int i = 0; i < n; i++) {
            if (!indegree[i]) {
                res.push_back(i);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.
