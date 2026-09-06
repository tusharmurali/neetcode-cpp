# 1514. Path with Maximum Probability

- **Difficulty:** Medium  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/path-with-maximum-probability/>  
- **NeetCode:** <https://neetcode.io/problems/path-with-maximum-probability>  
- **Video:** <https://www.youtube.com/watch?v=kPsDTGcrzGM>  

[← Back to index](../INDEX.md)

## 1. Dijkstra's Algorithm - I

This problem asks for the path with maximum probability, which is similar to finding the shortest path but with multiplication instead of addition. Since probabilities are between 0 and 1, multiplying them gives smaller values, so we want to maximize the product. Dijkstra's algorithm works here because we can negate probabilities (or use a max-heap) to always process the most promising path first. Once we reach the destination, we have found the optimal path.

```cpp
class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start_node, int end_node) {
        vector<vector<pair<int, double>>> adj(n);
        for (int i = 0; i < edges.size(); i++) {
            int src = edges[i][0], dst = edges[i][1];
            adj[src].emplace_back(dst, succProb[i]);
            adj[dst].emplace_back(src, succProb[i]);
        }

        vector<double> maxProb(n, 0.0);
        maxProb[start_node] = 1.0;
        priority_queue<pair<double, int>> pq;
        pq.emplace(1.0, start_node);

        while (!pq.empty()) {
            auto [curr_prob, node] = pq.top(); pq.pop();

            if (node == end_node) return curr_prob;
            if (curr_prob < maxProb[node]) continue;

            for (auto& [nei, edge_prob] : adj[node]) {
                double new_prob = curr_prob * edge_prob;
                if (new_prob > maxProb[nei]) {
                    maxProb[nei] = new_prob;
                    pq.emplace(new_prob, nei);
                }
            }
        }

        return 0.0;
    }
};
```

**Complexity**

- Time complexity: $O((V + E) \log V)$
- Space complexity: $O(V + E)$

> Where $V$ is the number nodes and $E$ is the number of edges.

## 2. Dijkstra's Algorithm - II

This is a refined version of Dijkstra's algorithm that tracks the maximum probability to reach each node. Instead of just using a visited set, we maintain an array storing the best probability found so far for each node. This allows us to skip processing a node if we have already found a better path to it, reducing unnecessary work.

```cpp
class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start_node, int end_node) {
        vector<vector<pair<int, double>>> adj(n);
        for (int i = 0; i < edges.size(); i++) {
            int src = edges[i][0], dst = edges[i][1];
            adj[src].emplace_back(dst, succProb[i]);
            adj[dst].emplace_back(src, succProb[i]);
        }

        vector<double> maxProb(n, 0.0);
        maxProb[start_node] = 1.0;
        priority_queue<pair<double, int>> pq;
        pq.emplace(1.0, start_node);

        while (!pq.empty()) {
            auto [curr_prob, node] = pq.top(); pq.pop();

            if (node == end_node) return curr_prob;
            if (curr_prob < maxProb[node]) continue;

            for (auto& [nei, edge_prob] : adj[node]) {
                double new_prob = curr_prob * edge_prob;
                if (new_prob > maxProb[nei]) {
                    maxProb[nei] = new_prob;
                    pq.emplace(new_prob, nei);
                }
            }
        }

        return 0.0;
    }
};
```

**Complexity**

- Time complexity: $O((V + E) \log V)$
- Space complexity: $O(V + E)$

> Where $V$ is the number nodes and $E$ is the number of edges.

## 3. Bellman Ford Algorithm

The Bellman-Ford algorithm can find the best path by relaxing all edges repeatedly. For this problem, we relax edges to maximize probability instead of minimizing distance. Since the graph is undirected, we check both directions for each edge. The algorithm runs for at most `n` iterations, but we can stop early if no updates occur in a round, meaning we have found the optimal solution.

```cpp
class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start_node, int end_node) {
        vector<double> maxProb(n, 0.0);
        maxProb[start_node] = 1.0;

        for (int i = 0; i < n; i++) {
            bool updated = false;
            for (int j = 0; j < edges.size(); j++) {
                int src = edges[j][0], dst = edges[j][1];

                if (maxProb[src] * succProb[j] > maxProb[dst]) {
                    maxProb[dst] = maxProb[src] * succProb[j];
                    updated = true;
                }

                if (maxProb[dst] * succProb[j] > maxProb[src]) {
                    maxProb[src] = maxProb[dst] * succProb[j];
                    updated = true;
                }
            }
            if (!updated) break;
        }

        return maxProb[end_node];
    }
};
```

**Complexity**

- Time complexity: $O(V * E)$
- Space complexity: $O(V)$

> Where $V$ is the number nodes and $E$ is the number of edges.

## 4. Shortest Path Faster Algorithm

SPFA is an optimization of Bellman-Ford that uses a queue to process only nodes whose distances (or probabilities) have changed. Instead of iterating through all edges in every round, we only process edges from nodes that might lead to improvements. This can be significantly faster in practice, especially for sparse graphs.

```cpp
class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start_node, int end_node) {
        vector<vector<pair<int, double>>> adj(n);

        for (int i = 0; i < edges.size(); i++) {
            int src = edges[i][0], dst = edges[i][1];
            adj[src].emplace_back(dst, succProb[i]);
            adj[dst].emplace_back(src, succProb[i]);
        }

        vector<double> maxProb(n, 0.0);
        maxProb[start_node] = 1.0;
        queue<int> q;
        q.push(start_node);

        while (!q.empty()) {
            int node = q.front();
            q.pop();

            for (auto& [nei, edgeProb] : adj[node]) {
                double newProb = maxProb[node] * edgeProb;
                if (newProb > maxProb[nei]) {
                    maxProb[nei] = newProb;
                    q.push(nei);
                }
            }
        }

        return maxProb[end_node];
    }
};
```

**Complexity**

- Time complexity: $O(V * E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number nodes and $E$ is the number of edges.

## Standalone solution file (`cpp/1514-path-with-maximum-probability.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start_node, int end_node) {
        // adj list mapping {node -> [(probability, neighborNode), ...]}
        unordered_map<int, vector<pair<double, int>>> adj;
        for (int i=0; i<edges.size(); ++i) {
            vector<int> edge = edges[i];
            adj[edge[0]].push_back({succProb[i], edge[1]});
            adj[edge[1]].push_back({succProb[i], edge[0]});
        }

        // maxHeap storing pairs of (probability, node)
        priority_queue<pair<double, int>> pq; 
        pq.push({1.0, start_node});

        unordered_set<int> visited;

        // applying Dijkstra's algorithm
        while (!pq.empty()) {
            double currProb = pq.top().first;
            int currNode = pq.top().second;
            pq.pop();

            if (currNode == end_node)
                return currProb;

            visited.insert(currNode);

            for (auto& [nextProb, nextNode] : adj[currNode]) {
                if (visited.find(nextNode) == visited.end()) {
                    pq.push({currProb*nextProb, nextNode});
                }
            }
        }   

        return 0.0;
    }
};
```
