# 743. Network Delay Time

- **Difficulty:** Medium  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/network-delay-time/>  
- **NeetCode:** <https://neetcode.io/problems/network-delay-time>  
- **Video:** <https://www.youtube.com/watch?v=EaphyqKU4PQ>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We want to know **how long it takes for a signal to reach all nodes** starting from node `k`.

Using **DFS**, we try all possible paths from `k` and keep track of the **minimum time** needed to reach each node.

- If we reach a node with a **better (smaller) time**, we update it.
- If the current path is already worse than a known path, we stop exploring it (pruning).

After exploring all reachable paths:

- The answer is the **maximum time** among all nodes (last node to receive the signal).
- If any node is unreachable, return `-1`.

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        unordered_map<int, vector<pair<int, int>>> adj;
        for (auto& time : times) {
            adj[time[0]].emplace_back(time[1], time[2]);
        }

        vector<int> dist(n + 1, INT_MAX);
        dfs(k, 0, adj, dist);

        int res = *max_element(dist.begin() + 1, dist.end());
        return res == INT_MAX ? -1 : res;
    }

private:
    void dfs(int node, int time,
             unordered_map<int, vector<pair<int, int>>>& adj,
             vector<int>& dist) {
        if (time >= dist[node]) return;
        dist[node] = time;
        for (auto& [nei, w] : adj[node]) {
            dfs(nei, time + w, adj, dist);
        }
    }
};
```

**Complexity**

- Time complexity: $O(V * E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Floyd Warshall Algorithm

We want the **shortest time between every pair of nodes** so that we can easily know how long it takes for the signal to reach all nodes starting from `k`.

**Floyd–Warshall** is an _all-pairs shortest path_ algorithm:

- It repeatedly tries to improve the shortest path between every `(i, j)` by allowing an intermediate node `mid`.
- After processing all intermediates, `dist[i][j]` stores the shortest time from `i` to `j`.

Once all shortest paths are known:

- Look at the row corresponding to the starting node `k`.
- The **maximum value in that row** is the time when the last node receives the signal.
- If any node is unreachable (distance = ∞), return `-1`.

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        int inf = INT_MAX / 2;
        vector<vector<int>> dist(n, vector<int>(n, inf));

        for (int i = 0; i < n; i++)
            dist[i][i] = 0;

        for (auto& time : times) {
            int u = time[0] - 1, v = time[1] - 1, w = time[2];
            dist[u][v] = w;
        }

        for (int mid = 0; mid < n; mid++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    dist[i][j] = min(dist[i][j],
                                     dist[i][mid] + dist[mid][j]);

        int res = *max_element(dist[k-1].begin(), dist[k-1].end());
        return res == inf ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(V ^ 3)$
- Space complexity: $O(V ^ 2)$

> Where $V$ is the number of vertices.

## 3. Bellman Ford Algorithm

We want the **shortest time for a signal to reach every node** starting from node `k`.

**Bellman–Ford** works by:

- Relaxing (updating) all edges repeatedly.
- Each relaxation tries to improve the shortest distance to a node using one more edge.
- After `n - 1` rounds, all shortest paths are guaranteed to be found (because the longest simple path has at most `n - 1` edges).

Once distances are finalized:

- The **maximum distance** tells us when the last node receives the signal.
- If any node is still unreachable (`∞`), return `-1`.

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<int> dist(n, INT_MAX);
        dist[k - 1] = 0;

        for (int i = 0; i < n - 1; ++i) {
            for (const auto& time : times) {
                int u = time[0] - 1, v = time[1] - 1, w = time[2];
                if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }

        int maxDist = *max_element(dist.begin(), dist.end());
        return maxDist == INT_MAX ? -1 : maxDist;
    }
};
```

**Complexity**

- Time complexity: $O(V * E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 4. Shortest Path Faster Algorithm

**SPFA (Shortest Path Faster Algorithm)** is an optimized version of Bellman–Ford.

Instead of relaxing **all edges every time**, we:

- Only re-process nodes whose distance was **actually improved**
- Use a **queue** to propagate distance updates efficiently

Whenever a node’s shortest time decreases, its neighbors might also get a shorter path — so we push that node into the queue.

This avoids unnecessary work and is usually much faster in practice.

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        unordered_map<int, vector<pair<int, int>>> adj;
        for (const auto& time : times) {
            adj[time[0]].emplace_back(time[1], time[2]);
        }

        unordered_map<int, int> dist;
        for (int i = 1; i <= n; ++i) dist[i] = INT_MAX;
        dist[k] = 0;

        queue<pair<int, int>> q;
        q.emplace(k, 0);

        while (!q.empty()) {
            auto [node, time] = q.front();
            q.pop();
            if (dist[node] < time) continue;
            for (const auto& [nei, w] : adj[node]) {
                if (time + w < dist[nei]) {
                    dist[nei] = time + w;
                    q.emplace(nei, time + w);
                }
            }
        }

        int res = 0;
        for (const auto& [node, time] : dist) {
            res = max(res, time);
        }
        return res == INT_MAX ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$ in average case, $O(V * E)$ in worst case.
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 5. Dijkstra's Algorithm

**Dijkstra's Algorithm** finds the shortest time from the source node `k` to all other nodes when all edge weights are **non-negative**.

The key idea:

- Always expand the node that currently has the **smallest known time**
- Once a node is picked from the min-heap, its shortest time is **final**
- Use a **min-heap (priority queue)** to always process the closest node next

By doing this, we gradually spread the signal in increasing order of time.

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        unordered_map<int, vector<pair<int, int>>> edges;
        for (const auto& time : times) {
            edges[time[0]].emplace_back(time[1], time[2]);
        }

        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> minHeap;
        minHeap.push({0, k});

        set<int> visited;
        int t = 0;
        while (!minHeap.empty()) {
            auto curr = minHeap.top();
            minHeap.pop();
            int w1 = curr.first, n1 = curr.second;
            if (visited.count(n1)) {
                continue;
            }
            visited.insert(n1);
            t = w1;

            if (edges.count(n1)) {
                for (const auto& next : edges[n1]) {
                    int n2 = next.first, w2 = next.second;
                    if (!visited.count(n2)) {
                        minHeap.push({w1 + w2, n2});
                    }
                }
            }
        }

        return visited.size() == n ? t : -1;
    }
};
```

**Complexity**

- Time complexity: $O(E \log V)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## Standalone solution file (`cpp/0743-network-delay-time.cpp` in the NeetCode repo)

```cpp
/*
    Signal sent from node k to network of n nodes, return time for all nodes to receive it
    Ex. times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2 -> 2
                  u,v,w -> u = source node, v = target node, w = signal travel time

    Shortest path from node k to every other node, Dijkstra's to find fastest path

    Time: O(V + E log V)
    Space: O(V + E)
*/

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<pair<int, int>> adj[n + 1];
        for (int i = 0; i < times.size(); i++) {
            int source = times[i][0];
            int dest = times[i][1];
            int time = times[i][2];
            adj[source].push_back({time, dest});
        }
        
        vector<int> signalReceiveTime(n + 1, INT_MAX);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, k});
        
        // time for start node is 0
        signalReceiveTime[k] = 0;
        
        while (!pq.empty()) {
            int currNodeTime = pq.top().first;
            int currNode = pq.top().second;
            pq.pop();
            
            if (currNodeTime > signalReceiveTime[currNode]) {
                continue;
            }
            
            // send signal to adjacent nodes
            for (int i = 0; i < adj[currNode].size(); i++) {
                pair<int, int> edge = adj[currNode][i];
                int time = edge.first;
                int neighborNode = edge.second;
                
                // fastest signal time for neighborNode so far
                if (signalReceiveTime[neighborNode] > currNodeTime + time) {
                    signalReceiveTime[neighborNode] = currNodeTime + time;
                    pq.push({signalReceiveTime[neighborNode], neighborNode});
                }
            }
        }
        
        int result = INT_MIN;
        for (int i = 1; i <= n; i++) {
            result = max(result, signalReceiveTime[i]);
        }
        
        if (result == INT_MAX) {
            return -1;
        }
        return result;
    }
};
```
