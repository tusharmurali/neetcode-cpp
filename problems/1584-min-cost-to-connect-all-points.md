# 1584. Min Cost to Connect All Points

- **Difficulty:** Medium  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/min-cost-to-connect-all-points/>  
- **NeetCode:** <https://neetcode.io/problems/min-cost-to-connect-points>  
- **Video:** <https://www.youtube.com/watch?v=f7JOBJIC-NA>  
- **Video approach:** 2. Prim's Algorithm  

[← Back to index](../INDEX.md)

## 1. Kruskal's Algorithm

We want to connect **all points** such that the **total cost is minimum**, where the cost to connect two points is their **Manhattan distance**.
This is exactly the definition of a **Minimum Spanning Tree (MST)**.

**Kruskal's Algorithm** fits naturally:

- Treat each point as a node.
- Treat the distance between every pair of points as an edge weight.
- Always choose the **cheapest edge** that connects two **different components**.
- Avoid cycles while connecting all nodes.

To efficiently check whether two points are already connected, we use **Disjoint Set Union (Union-Find)**.

```cpp
class DSU {
public:
    vector<int> Parent, Size;

    DSU(int n) : Parent(n + 1), Size(n + 1, 1) {
        for (int i = 0; i <= n; ++i) Parent[i] = i;
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionSets(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (Size[pu] < Size[pv]) swap(pu, pv);
        Size[pu] += Size[pv];
        Parent[pv] = pu;
        return true;
    }
};

class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        DSU dsu(n);
        vector<array<int, 3>> edges;

        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                int dist = abs(points[i][0] - points[j][0]) +
                           abs(points[i][1] - points[j][1]);
                edges.push_back({dist, i, j});
            }
        }

        sort(edges.begin(), edges.end());
        int res = 0;

        for (auto& [dist, u, v] : edges) {
            if (dsu.unionSets(u, v)) {
                res += dist;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 2. Prim's Algorithm ▶ video

We still want a **Minimum Spanning Tree (MST)**: connect all points with minimum total Manhattan distance.

**Prim's Algorithm** grows the MST **one node at a time**:

- Start from any point (say point `0`).
- At every step, pick the **cheapest edge** that connects:
    - a point already in the MST
    - to a point not yet in the MST
- Keep doing this until all points are included.

A **min-heap (priority queue)** is used to always get the next cheapest edge quickly.

```cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int N = points.size();
        unordered_map<int, vector<pair<int, int>>> adj;
        for (int i = 0; i < N; i++) {
            int x1 = points[i][0];
            int y1 = points[i][1];
            for (int j = i + 1; j < N; j++) {
                int x2 = points[j][0];
                int y2 = points[j][1];
                int dist = abs(x1 - x2) + abs(y1 - y2);
                adj[i].push_back({dist, j});
                adj[j].push_back({dist, i});
            }
        }

        int res = 0;
        unordered_set<int> visit;
        priority_queue<pair<int, int>, vector<pair<int, int>>,
                                greater<pair<int, int>>> minH;
        minH.push({0, 0});
        while (visit.size() < N) {
            auto curr = minH.top();
            minH.pop();
            int cost = curr.first;
            int i = curr.second;
            if (visit.count(i)) {
                continue;
            }
            res += cost;
            visit.insert(i);
            for (const auto& nei : adj[i]) {
                int neiCost = nei.first;
                int neiIndex = nei.second;
                if (!visit.count(neiIndex)) {
                    minH.push({neiCost, neiIndex});
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 3. Prim's Algorithm (Optimal)

We want to connect all points so that the **total cost is minimum**, where the cost to connect two points is their **Manhattan distance**.  
This is exactly a **Minimum Spanning Tree (MST)** problem:

- Think of each point as a node in a graph.
- Every pair of points has an edge with weight = Manhattan distance.
- We need the cheapest way to connect all nodes without forming unnecessary cycles → that’s an MST.

This solution uses **Prim’s Algorithm** (greedy MST building):

- Start from any node (here, node `0`).
- Repeatedly add the **closest unvisited node** to the growing connected set.
- Keep track of the best (minimum) known distance from the current MST to every unvisited node.

Instead of building all edges (which would be too many), we compute distances **on the fly** and update the best known connection cost for each node.

---

```cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size(), node = 0;
        vector<int> dist(n, 100000000);
        vector<bool> visit(n, false);
        int edges = 0, res = 0;

        while (edges < n - 1) {
            visit[node] = true;
            int nextNode = -1;
            for (int i = 0; i < n; i++) {
                if (visit[i]) continue;
                int curDist = abs(points[i][0] - points[node][0]) +
                               abs(points[i][1] - points[node][1]);
                dist[i] = min(dist[i], curDist);
                if (nextNode == -1 || dist[i] < dist[nextNode]) {
                    nextNode = i;
                }
            }
            res += dist[nextNode];
            node = nextNode;
            edges++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1584-min-cost-to-connect-all-points.cpp` in the NeetCode repo)

```cpp
/*
    Given array of points, return min cost to connect all points
    All points have 1 path b/w them, cost is Manhattan distance

    MST problem, Prim's, greedily pick node not in MST & has smallest edge cost
    Add to MST, & for all its neighbors, try to update min dist values, repeat

    Time: O(n^2)
    Space: O(n)
*/

class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        
        int edgesUsed = 0;
        // track visited nodes
        vector<bool> inMST(n);
        vector<int> minDist(n, INT_MAX);
        minDist[0] = 0;
        
        int result = 0;
        
        while (edgesUsed < n) {
            int currMinEdge = INT_MAX;
            int currNode = -1;
            
            // greedily pick lowest cost node not in MST
            for (int i = 0; i < n; i++) {
                if (!inMST[i] && currMinEdge > minDist[i]) {
                    currMinEdge = minDist[i];
                    currNode = i;
                }
            }
            
            result += currMinEdge;
            edgesUsed++;
            inMST[currNode] = true;
            
            // update adj nodes of curr node
            for (int i = 0; i < n; i++) {
                int cost = abs(points[currNode][0] - points[i][0])
                    + abs(points[currNode][1] - points[i][1]);
                
                if (!inMST[i] && minDist[i] > cost) {
                    minDist[i] = cost;
                }
            }
        }
        
        return result;
    }
};
```
