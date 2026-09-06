# 802. Find Eventual Safe States

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-eventual-safe-states/>  
- **NeetCode:** <https://neetcode.io/problems/find-eventual-safe-states>  
- **Video:** <https://www.youtube.com/watch?v=Re_v0j0CRsg>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A node is safe if every path starting from it eventually leads to a terminal node (a node with no outgoing edges). Conversely, a node is unsafe if it can reach a cycle. We can use DFS with memoization to determine safety: initially mark a node as unsafe when we start exploring it (to detect cycles), then mark it safe only if all its neighbors are safe. If we revisit a node marked unsafe during exploration, we have found a cycle.

```cpp
class Solution {
    vector<int> safe;

public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> res;
        safe.assign(n, -1);
        for (int node = 0; node < n; node++) {
            if (dfs(graph, node)) {
                res.push_back(node);
            }
        }
        return res;
    }

private:
    bool dfs(vector<vector<int>>& graph, int node) {
        if (safe[node] != -1) {
            return safe[node];
        }
        safe[node] = 0;
        for (int nei : graph[node]) {
            if (!dfs(graph, nei)) {
                return false;
            }
        }
        safe[node] = 1;
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the given graph.

## 2. Topological Sort (Kahn's Algorithm)

Think of safe nodes as those that can reach terminal nodes. If we reverse the edge directions, safe nodes are those reachable from terminal nodes. Using Kahn's algorithm on this reversed perspective: terminal nodes have zero out-degree in the original graph. We start from these terminal nodes and work backward, removing edges. Any node whose out-degree reaches zero is safe because all its paths lead to already-confirmed safe nodes.

```cpp
class Solution {
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> outdegree(n, 0);
        vector<vector<int>> parents(n);
        queue<int> q;

        for (int node = 0; node < n; node++) {
            outdegree[node] = graph[node].size();
            if (outdegree[node] == 0) {
                q.push(node);
            }
            for (int nei : graph[node]) {
                parents[nei].push_back(node);
            }
        }

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            for (int parent : parents[node]) {
                outdegree[parent]--;
                if (outdegree[parent] == 0) {
                    q.push(parent);
                }
            }
        }

        vector<int> res;
        for (int node = 0; node < n; node++) {
            if (outdegree[node] <= 0) {
                res.push_back(node);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the given graph.
