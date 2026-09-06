# 1466. Reorder Routes to Make All Paths Lead to The City Zero

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/>  
- **NeetCode:** <https://neetcode.io/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero>  
- **Video:** <https://www.youtube.com/watch?v=m17yOR5_PpI>  

[← Back to index](../INDEX.md)

## 1. Depth First Search - I

We need all cities to reach city 0, so we traverse outward from city 0 and check edge directions. Build an undirected `neighbors` graph for traversal, but store original edges in `edges` set to check direction. When moving from `city` A to `neighbor` B, if the original edge goes from A to B (away from 0), it needs to be reversed. `dfs` ensures we visit every city exactly once.

```cpp
class Solution {
public:
    int minReorder(int n, vector<vector<int>>& connections) {
        unordered_set<string> edges;
        unordered_map<int, vector<int>> neighbors;
        vector<bool> visit(n, false);
        int changes = 0;

        for (auto& c : connections) {
            edges.insert(to_string(c[0]) + "," + to_string(c[1]));
            neighbors[c[0]].push_back(c[1]);
            neighbors[c[1]].push_back(c[0]);
        }

        function<void(int)> dfs = [&](int city) {
            visit[city] = true;
            for (int neighbor : neighbors[city]) {
                if (visit[neighbor]) continue;
                if (edges.find(to_string(neighbor) + "," + to_string(city)) == edges.end()) {
                    changes++;
                }
                dfs(neighbor);
            }
        };

        dfs(0);
        return changes;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Depth First Search - II

Instead of using a separate set to track edge directions, we can encode direction information directly in the adjacency list. When adding edges, we store the original direction as a positive value and the reverse as negative. During `dfs`, positive `nei` values indicate edges pointing away from city 0, which need reversal.

```cpp
class Solution {
public:
    int minReorder(int n, vector<vector<int>>& connections) {
        vector<vector<int>> adj(n);
        for (auto& conn : connections) {
            int u = conn[0], v = conn[1];
            adj[u].push_back(v);
            adj[v].push_back(-u);
        }

        return dfs(0, -1, adj);
    }

private:
    int dfs(int node, int parent, vector<vector<int>>& adj) {
        int changes = 0;
        for (int nei : adj[node]) {
            if (abs(nei) == parent) continue;
            changes += dfs(abs(nei), node, adj) + (nei > 0);
        }
        return changes;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Breadth First Search

`bfs` works equally well since we just need to visit all nodes once from city 0. We store each edge with a flag `isForward` indicating if it is a forward edge (pointing away from city 0). Processing level by level in `queue`, whenever we traverse a forward edge, we count it as needing reversal.

```cpp
class Solution {
public:
    int minReorder(int n, vector<vector<int>>& connections) {
        vector<vector<pair<int, int>>> adj(n);
        for (auto& conn : connections) {
            adj[conn[0]].push_back({conn[1], 1});
            adj[conn[1]].push_back({conn[0], 0});
        }

        vector<bool> visit(n, false);
        queue<int> q;
        q.push(0);
        visit[0] = true;
        int changes = 0;

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            for (auto& [neighbor, isForward] : adj[node]) {
                if (!visit[neighbor]) {
                    visit[neighbor] = true;
                    changes += isForward;
                    q.push(neighbor);
                }
            }
        }
        return changes;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1466-reorder-routes-to-make-all-paths-lead-to-the-city-zero.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int minReorder(int n, vector<vector<int>>& connections) {
        unordered_map<int, vector<pair<int, bool>>> graph;
        unordered_set<int> visited;

        for (int i = 0; i < n; i++)
            graph[i] = vector<pair<int, bool>>{};

        for (vector<int> connection : connections) {
            graph[connection[0]].push_back(make_pair(connection[1], true));
            graph[connection[1]].push_back(make_pair(connection[0], false));
        }

        int cnt = 0;
        stack<int> stk;
        stk.push(0);
        visited.insert(0);

        while (!stk.empty()) {
            int u = stk.top();
            stk.pop();
            for (pair<int, bool> v : graph[u]) {
                if (visited.count(v.first))
                    continue;
                stk.push(v.first);
                visited.insert(v.first);
                if (v.second)
                    cnt += 1;
            }
        }

        return cnt;
    }
};
```
