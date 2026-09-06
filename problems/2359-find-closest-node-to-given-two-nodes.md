# 2359. Find Closest Node to Given Two Nodes

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-closest-node-to-given-two-nodes/>  
- **NeetCode:** <https://neetcode.io/problems/find-closest-node-to-given-two-nodes>  
- **Video:** <https://www.youtube.com/watch?v=AZA8orksO4w>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

We want a node reachable from both `node1` and `node2` that minimizes the maximum of the two distances. First, we compute distances from `node1` to all reachable nodes, then do the same from `node2`. For each node reachable from both, the "cost" is the larger of the two distances. We pick the node with the smallest such cost, breaking ties by choosing the smaller index.

```cpp
class Solution {
public:
    int closestMeetingNode(vector<int>& edges, int node1, int node2) {
        int n = edges.size();
        vector<vector<int>> adj(n);
        for (int i = 0; i < n; i++) {
            if (edges[i] != -1) adj[i].push_back(edges[i]);
        }

        vector<int> node1Dist = bfs(node1, n, adj);
        vector<int> node2Dist = bfs(node2, n, adj);

        int res = -1, resDist = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (node1Dist[i] != -1 && node2Dist[i] != -1) {
                int dist = max(node1Dist[i], node2Dist[i]);
                if (dist < resDist) {
                    resDist = dist;
                    res = i;
                }
            }
        }
        return res;
    }

private:
    vector<int> bfs(int src, int n, vector<vector<int>>& adj) {
        vector<int> distMap(n, -1);
        queue<pair<int, int>> q;
        q.push({src, 0});
        distMap[src] = 0;

        while (!q.empty()) {
            auto [node, dist] = q.front();
            q.pop();

            for (int nei : adj[node]) {
                if (distMap[nei] == -1) {
                    q.push({nei, dist + 1});
                    distMap[nei] = dist + 1;
                }
            }
        }
        return distMap;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search (Optimal)

Since each node has at most one outgoing edge, we do not need a full adjacency list. We can traverse directly using the edges array. The BFS logic remains the same, but we simplify by following `edges[node]` directly instead of iterating through neighbors.

```cpp
class Solution {
public:
    int closestMeetingNode(vector<int>& edges, int node1, int node2) {
        int n = edges.size();
        vector<int> node1Dist = bfs(node1, edges, n);
        vector<int> node2Dist = bfs(node2, edges, n);

        int res = -1, resDist = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (node1Dist[i] != -1 && node2Dist[i] != -1) {
                int dist = max(node1Dist[i], node2Dist[i]);
                if (dist < resDist) {
                    resDist = dist;
                    res = i;
                }
            }
        }
        return res;
    }

private:
    vector<int> bfs(int src, vector<int>& edges, int n) {
        vector<int> dist(n, -1);
        queue<int> q;
        q.push(src);
        dist[src] = 0;

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            int nei = edges[node];
            if (nei == -1 || dist[nei] != -1) {
                continue;
            }

            q.push(nei);
            dist[nei] = dist[node] + 1;
        }
        return dist;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Depth First Search

DFS achieves the same goal as BFS here. Starting from each source node, we recursively follow edges and record distances. The graph structure (each node has at most one outgoing edge) means DFS naturally follows the single path from each source without branching.

```cpp
class Solution {
public:
    int closestMeetingNode(vector<int>& edges, int node1, int node2) {
        int n = edges.size();
        vector<int> node1Dist(n, -1), node2Dist(n, -1);
        node1Dist[node1] = node2Dist[node2] = 0;

        dfs(node1, edges, node1Dist);
        dfs(node2, edges, node2Dist);

        int res = -1, resDist = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (min(node1Dist[i], node2Dist[i]) != -1) {
                int dist = max(node1Dist[i], node2Dist[i]);
                if (dist < resDist) {
                    resDist = dist;
                    res = i;
                }
            }
        }
        return res;
    }

private:
    void dfs(int node, vector<int>& edges, vector<int>& dist) {
        int nei = edges[node];
        if (nei != -1 && dist[nei] == -1) {
            dist[nei] = dist[node] + 1;
            dfs(nei, edges, dist);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Iterative Depth First Search

Since each node has exactly one outgoing edge, we can replace recursion with a simple while loop. Starting from each source, we follow edges iteratively until we reach `-1` or a visited node. This avoids recursion overhead while computing the same distances.

```cpp
class Solution {
public:
    int closestMeetingNode(vector<int>& edges, int node1, int node2) {
        int n = edges.size();
        vector<int> node1Dist = dfs(node1, edges, n);
        vector<int> node2Dist = dfs(node2, edges, n);

        int res = -1, resDist = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (min(node1Dist[i], node2Dist[i]) != -1) {
                int dist = max(node1Dist[i], node2Dist[i]);
                if (dist < resDist) {
                    resDist = dist;
                    res = i;
                }
            }
        }
        return res;
    }

private:
    vector<int> dfs(int node, vector<int>& edges, int n) {
        vector<int> dist(n, -1);
        dist[node] = 0;
        while (edges[node] != -1 && dist[edges[node]] == -1) {
            int nei = edges[node];
            dist[nei] = dist[node] + 1;
            node = nei;
        }
        return dist;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
