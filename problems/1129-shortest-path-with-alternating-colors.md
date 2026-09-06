# 1129. Shortest Path with Alternating Colors

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shortest-path-with-alternating-colors/>  
- **NeetCode:** <https://neetcode.io/problems/shortest-path-with-alternating-colors>  
- **Video:** <https://www.youtube.com/watch?v=69rcy6lb-HQ>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search - I

We need to find shortest paths from node `0` to all other nodes, but with a twist: the path must alternate between red and blue edges. The key insight is that reaching a node via a red edge is different from reaching it via a blue edge, because it affects which color we can use next. So we track states as `(node, last_edge_color)` pairs. `BFS` naturally finds shortest paths in unweighted graphs, and since we want the first time we reach each node, we record the distance on first visit.

```cpp
class Solution {
public:
    vector<int> shortestAlternatingPaths(int n, vector<vector<int>>& redEdges, vector<vector<int>>& blueEdges) {
        vector<vector<int>> red(n), blue(n);
        for (auto& edge : redEdges) red[edge[0]].push_back(edge[1]);
        for (auto& edge : blueEdges) blue[edge[0]].push_back(edge[1]);

        vector<int> answer(n, -1);
        queue<vector<int>> q;
        q.push({0, 0, -1});
        unordered_set<string> visit;
        visit.insert("0,-1");

        while (!q.empty()) {
            vector<int> nodeData = q.front();
            q.pop();
            int node = nodeData[0], length = nodeData[1], edgeColor = nodeData[2];

            if (answer[node] == -1) answer[node] = length;

            if (edgeColor != 0) {
                for (int nei : red[node]) {
                    string key = to_string(nei) + ",0";
                    if (visit.insert(key).second) {
                        q.push({nei, length + 1, 0});
                    }
                }
            }
            if (edgeColor != 1) {
                for (int nei : blue[node]) {
                    string key = to_string(nei) + ",1";
                    if (visit.insert(key).second) {
                        q.push({nei, length + 1, 1});
                    }
                }
            }
        }
        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Breadth First Search - II

This approach uses a cleaner state representation. Instead of tracking the edge color explicitly, we use `0` for red and `1` for blue, and toggle between them using XOR (`color ^ 1`). We maintain a 2D distance array where `dist[node][color]` stores the shortest distance to reach `node` when the last edge used was `color`. Starting from node `0` with both colors as valid starting points, we relax edges only when we find a shorter path.

```cpp
class Solution {
public:
    vector<int> shortestAlternatingPaths(int n, vector<vector<int>>& redEdges, vector<vector<int>>& blueEdges) {
        vector<vector<int>> red = buildGraph(n, redEdges);
        vector<vector<int>> blue = buildGraph(n, blueEdges);
        vector<vector<int>> adj[] = {red, blue};

        const int INF = 1e6;
        vector<vector<int>> dist(n, vector<int>(2, INF));
        dist[0][0] = dist[0][1] = 0;

        queue<pair<int, int>> q;
        q.push({0, 0});
        q.push({0, 1});

        while (!q.empty()) {
            auto [node, color] = q.front();q.pop();
            for (int nei : adj[color][node]) {
                if (dist[nei][color ^ 1] > dist[node][color] + 1) {
                    dist[nei][color ^ 1] = dist[node][color] + 1;
                    q.push({nei, color ^ 1});
                }
            }
        }

        vector<int> answer(n, -1);
        for (int i = 0; i < n; i++) {
            answer[i] = min(dist[i][0], dist[i][1]);
            if (answer[i] == INF) answer[i] = -1;
        }
        return answer;
    }

private:
    vector<vector<int>> buildGraph(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }
        return adj;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 3. Depth First Search

While `BFS` is typically preferred for shortest path problems, `DFS` can also work here because we are tracking distances and only updating when we find a shorter path. The recursion naturally handles the alternating color constraint. We start `DFS` from node `0` twice: once beginning with red edges and once with blue. Whenever we find a shorter path to a node with a particular ending color, we update the distance and continue exploring.

```cpp
class Solution {
public:
    vector<int> shortestAlternatingPaths(int n, vector<vector<int>>& redEdges, vector<vector<int>>& blueEdges) {
        vector<vector<int>> adj[2] = {buildGraph(n, redEdges), buildGraph(n, blueEdges)};

        int INF = numeric_limits<int>::max();
        vector<vector<int>> dist(n, vector<int>(2, INF));
        dist[0][0] = dist[0][1] = 0;

        dfs(0, 0, adj, dist);
        dfs(0, 1, adj, dist);

        vector<int> answer(n, -1);
        for (int i = 0; i < n; i++) {
            answer[i] = min(dist[i][0], dist[i][1]);
            if (answer[i] == INF) answer[i] = -1;
        }
        return answer;
    }

private:
    void dfs(int node, int color, vector<vector<int>> adj[], vector<vector<int>>& dist) {
        for (int nei : adj[color][node]) {
            if (dist[nei][color ^ 1] > dist[node][color] + 1) {
                dist[nei][color ^ 1] = dist[node][color] + 1;
                dfs(nei, color ^ 1, adj, dist);
            }
        }
    }

    vector<vector<int>> buildGraph(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        for (auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
        }
        return adj;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.
