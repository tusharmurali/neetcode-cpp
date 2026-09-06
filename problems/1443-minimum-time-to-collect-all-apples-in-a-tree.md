# 1443. Minimum Time to Collect All Apples in a Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-time-to-collect-all-apples-in-a-tree>  
- **Video:** <https://www.youtube.com/watch?v=Xdt5Z583auM>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We start at node `0` and need to visit all nodes that have apples. The key observation is that if a subtree contains any apple (either at the child node itself or deeper in the subtree), we must traverse the edge to that child and back, costing `2` seconds. We use DFS to compute the time needed for each subtree. If a child has an apple or its subtree requires time (meaning there's an apple deeper), we add `2` plus the child's subtree time to our current total.

```cpp
class Solution {
public:
    int minTime(int n, vector<vector<int>>& edges, vector<bool>& hasApple) {
        vector<vector<int>> adj(n);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        return dfs(0, -1, adj, hasApple);
    }

private:
    int dfs(int cur, int parent, vector<vector<int>>& adj, vector<bool>& hasApple) {
        int time = 0;
        for (int child : adj[cur]) {
            if (child == parent) continue;
            int childTime = dfs(child, cur, adj, hasApple);
            if (childTime > 0 || hasApple[child]) {
                time += 2 + childTime;
            }
        }
        return time;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Topological Sort (Kahn's Algorithm)

Instead of top-down DFS, we can process the tree from leaves to root. Starting from leaf nodes (nodes with only one connection, excluding the root), we propagate the time upward. If a leaf has an apple or already accumulated time from its subtree, we add `2` seconds to its parent. This bottom-up approach naturally handles the aggregation of times from multiple subtrees.

```cpp
class Solution {
public:
    int minTime(int n, vector<vector<int>>& edges, vector<bool>& hasApple) {
        vector<vector<int>> adj(n);
        vector<int> indegree(n, 0);

        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
            indegree[edge[0]]++;
            indegree[edge[1]]++;
        }

        queue<int> q;
        for (int i = 1; i < n; ++i) {
            if (indegree[i] == 1) {
                q.push(i);
                indegree[i] = 0;
            }
        }

        vector<int> time(n, 0);
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            for (int neighbor : adj[node]) {
                if (indegree[neighbor] <= 0) {
                    continue;
                }

                indegree[neighbor]--;
                if (hasApple[node] || time[node] > 0) {
                    time[neighbor] += time[node] + 2;
                }
                if (indegree[neighbor] == 1 && neighbor != 0) {
                    q.push(neighbor);
                }
            }
        }

        return time[0];
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.
