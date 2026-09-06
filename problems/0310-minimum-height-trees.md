# 310. Minimum Height Trees

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/minimum-height-trees/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-height-trees>  
- **Video:** <https://www.youtube.com/watch?v=wQGQnyv_9hI>  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

The most straightforward approach is to try each node as a potential root and measure the resulting tree height. The height of a tree rooted at any node is the maximum distance to any other node, which we can find using `dfs`.

By computing the height for every possible root, we can identify which nodes produce the minimum height. While simple to understand, this repeats a lot of work since we recompute distances from scratch for each candidate root.

```cpp
class Solution {
private:
    vector<vector<int>> adj;

    int dfs(int node, int parent) {
        int hgt = 0;
        for (int nei : adj[node]) {
            if (nei == parent)
                continue;
            hgt = max(hgt, 1 + dfs(nei, node));
        }
        return hgt;
    }

public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        adj.resize(n);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        int minHgt = n;
        vector<int> result;
        for (int i = 0; i < n; i++) {
            int curHgt = dfs(i, -1);
            if (curHgt == minHgt) {
                result.push_back(i);
            } else if (curHgt < minHgt) {
                result = {i};
                minHgt = curHgt;
            }
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(V * (V + E))$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Dynamic Programming On Trees (Rerooting)

Rather than recomputing everything for each root, we can reuse information. The tree height from any node depends on the longest path in two directions: down into its subtree and up through its parent to the rest of the tree.

We run two `dfs` passes. The first computes the two longest downward paths for each node (we need two in case the longest path goes through the child we came from). The second pass propagates information from parent to children, combining the parent's best path with sibling subtree heights.

```cpp
class Solution {
private:
    vector<vector<int>> adj;
    vector<vector<int>> dp;

    void dfs(int node, int parent) {
        for (int nei : adj[node]) {
            if (nei == parent) continue;
            dfs(nei, node);
            int curHgt = 1 + dp[nei][0];
            if (curHgt > dp[node][0]) {
                dp[node][1] = dp[node][0];
                dp[node][0] = curHgt;
            } else if (curHgt > dp[node][1]) {
                dp[node][1] = curHgt;
            }
        }
    }

    void dfs1(int node, int parent, int topHgt) {
        if (topHgt > dp[node][0]) {
            dp[node][1] = dp[node][0];
            dp[node][0] = topHgt;
        } else if (topHgt > dp[node][1]) {
            dp[node][1] = topHgt;
        }

        for (int nei : adj[node]) {
            if (nei == parent) continue;
            int toChild = 1 + ((dp[node][0] == 1 + dp[nei][0]) ? dp[node][1] : dp[node][0]);
            dfs1(nei, node, toChild);
        }
    }

public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        adj.resize(n);
        dp.assign(n, vector<int>(2, 0)); // top two heights for each node
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        dfs(0, -1);
        dfs1(0, -1, 0);

        int minHgt = n;
        vector<int> res;
        for (int i = 0; i < n; i++) {
            minHgt = min(minHgt, dp[i][0]);
        }
        for (int i = 0; i < n; i++) {
            if (minHgt == dp[i][0]) {
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

## 3. Find Centroids of the Tree (DFS)

The minimum height trees are rooted at the centroid(s) of the tree. These centroids lie at the middle of the longest path (diameter) in the tree. If the diameter has odd length, there are two centroids; if even, there's exactly one.

We find the diameter using two `bfs`/`dfs` passes: first find the farthest node from any starting point, then find the farthest node from that. The path between these two endpoints is the diameter, and its middle node(s) are the answer.

```cpp
class Solution {
public:
    vector<vector<int>> adj;
    vector<int> centroids;
    int nodeB;

    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        if (n == 1)
            return {0};

        adj.resize(n);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        int nodeA = dfs(0, -1).first;
        nodeB = dfs(nodeA, -1).first;
        findCentroids(nodeA, -1);

        int L = centroids.size();
        if (dfs(nodeA, -1).second % 2 == 0)
            return {centroids[L / 2]};
        else
            return {centroids[L / 2 - 1], centroids[L / 2]};
    }

private:
    pair<int, int> dfs(int node, int parent) {
        int farthestNode = node, maxDistance = 0;
        for (int neighbor : adj[node]) {
            if (neighbor != parent) {
                auto res = dfs(neighbor, node);
                if (res.second + 1 > maxDistance) {
                    maxDistance = res.second + 1;
                    farthestNode = res.first;
                }
            }
        }
        return {farthestNode, maxDistance};
    }

    bool findCentroids(int node, int parent) {
        if (node == nodeB) {
            centroids.push_back(node);
            return true;
        }
        for (int neighbor : adj[node]) {
            if (neighbor != parent) {
                if (findCentroids(neighbor, node)) {
                    centroids.push_back(node);
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 4. Topological Sorting (BFS)

Imagine peeling the tree like an onion, removing leaves layer by layer. The nodes that remain at the very end (when only `1` or `2` nodes are left) must be the centroids, since they're the innermost points of the tree.

Each round of removal brings us one step closer to the center. Since a tree can have at most `2` centroids (on a diameter of odd length), we stop when `2` or fewer nodes remain.

```cpp
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        if (n == 1) return {0};

        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        vector<int> edge_cnt(n);
        queue<int> leaves;

        for (int i = 0; i < n; ++i) {
            edge_cnt[i] = adj[i].size();
            if (adj[i].size() == 1)
                leaves.push(i);
        }

        while (!leaves.empty()) {
            if (n <= 2) {
                vector<int> result;
                while (!leaves.empty()) {
                    result.push_back(leaves.front());
                    leaves.pop();
                }
                return result;
            }
            int size = leaves.size();
            for (int i = 0; i < size; ++i) {
                int node = leaves.front();
                leaves.pop();
                --n;
                for (int& nei : adj[node]) {
                    --edge_cnt[nei];
                    if (edge_cnt[nei] == 1)
                        leaves.push(nei);
                }
            }
        }

        return {};
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.
