# 1857. Largest Color Value in a Directed Graph

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-color-value-in-a-directed-graph/>  
- **NeetCode:** <https://neetcode.io/problems/largest-color-value-in-a-directed-graph>  
- **Video:** <https://www.youtube.com/watch?v=xLoDjKczUSk>  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

The problem asks for the maximum count of any single color along any valid path in the graph. A direct approach is to try every possible starting node and every possible color, then use DFS to explore all paths and count how many nodes of that color we encounter. If we detect a cycle during DFS, the answer is -1 since valid paths cannot contain cycles.

```cpp
class Solution {
public:
    int n;
    vector<vector<int>> adj;
    vector<bool> visit;

    int largestPathValue(string colors, vector<vector<int>>& edges) {
        n = colors.size();
        adj.assign(n, vector<int>());
        visit.assign(n, false);

        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }

        int res = -1;
        for (int i = 0; i < n; i++) {
            for (int c = 0; c < 26; c++) {
                int cnt = dfs(i, c, colors);
                if (cnt == 1e9) return -1;
                res = max(res, cnt);
            }
        }
        return res;
    }

private:
    int dfs(int node, int c, string& colors) {
        if (visit[node]) return 1e9;

        visit[node] = true;
        int clrCnt = 0;
        for (int nei : adj[node]) {
            int cur = dfs(nei, c, colors);
            if (cur == 1e9) return cur;
            clrCnt = max(clrCnt, cur);
        }
        visit[node] = false;
        return clrCnt + ((colors[node] - 'a') == c ? 1 : 0);
    }
};
```

**Complexity**

- Time complexity: $O(V * (V + E))$
- Space complexity: $O(V + E)$

> Where $V$ is the number of verticies and $E$ is the number of edges.

## 2. Depth First Search

Instead of checking one color at a time, we can track all 26 color counts simultaneously for each node. Using memoization, once we compute the maximum color counts reachable from a node, we store and reuse that result. We use two sets: one for globally visited nodes (already fully processed) and one for the current DFS path (to detect cycles).

```cpp
class Solution {
public:
    int n, INF = 1e9;
    vector<vector<int>> adj;
    vector<bool> visit, path;
    vector<vector<int>> count;

    int largestPathValue(string colors, vector<vector<int>>& edges) {
        this->n = colors.size();
        adj.resize(n);
        visit.assign(n, false);
        path.assign(n, false);
        count.assign(n, vector<int>(26));

        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }

        int res = 0;
        for (int i = 0; i < n; i++) {
            if (dfs(i, colors) == INF) return -1;
            for (int c = 0; c < 26; c++) {
                res = max(res, count[i][c]);
            }
        }
        return res;
    }

private:
    int dfs(int node, string& colors) {
        if (path[node]) return INF;
        if (visit[node]) return 0;

        visit[node] = true;
        path[node] = true;
        int colorIndex = colors[node] - 'a';
        count[node][colorIndex] = 1;

        for (int& nei : adj[node]) {
            if (dfs(nei, colors) == INF) return INF;
            for (int c = 0; c < 26; c++) {
                count[node][c] = max(
                    count[node][c],
                    (c == colorIndex ? 1 : 0) + count[nei][c]
                );
            }
        }

        path[node] = false;
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of verticies and $E$ is the number of edges.

## 3. Topological Sort (Kahn's Algorithm)

Since we need valid paths in a directed graph, topological sorting naturally fits. We process nodes in topological order using Kahn's algorithm (BFS with indegree tracking). For each node, we propagate color counts to its neighbors before they are processed. If we cannot process all nodes, a cycle exists. This approach avoids recursion and handles cycle detection elegantly.

```cpp
class Solution {
public:
    int largestPathValue(string colors, vector<vector<int>>& edges) {
        int n = colors.size();
        vector<vector<int>> adj(n);
        vector<int> indegree(n);
        vector<vector<int>> count(n, vector<int>(26));

        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            indegree[edge[1]]++;
        }

        queue<int> q;
        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0) {
                q.push(i);
            }
        }

        int visit = 0, res = 0;
        while (!q.empty()) {
            int node = q.front();q.pop();
            visit++;
            int colorIndex = colors[node] - 'a';
            count[node][colorIndex]++;
            res = max(res, count[node][colorIndex]);

            for (int& nei : adj[node]) {
                for (int c = 0; c < 26; c++) {
                    count[nei][c] = max(count[nei][c], count[node][c]);
                }
                if (--indegree[nei] == 0) {
                    q.push(nei);
                }
            }
        }

        return visit == n ? res : -1;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of verticies and $E$ is the number of edges.
