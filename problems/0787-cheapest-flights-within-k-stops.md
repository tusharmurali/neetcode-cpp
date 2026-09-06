# 787. Cheapest Flights Within K Stops

- **Difficulty:** Medium  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/cheapest-flights-within-k-stops/>  
- **NeetCode:** <https://neetcode.io/problems/cheapest-flight-path>  
- **Video:** <https://www.youtube.com/watch?v=5eIK3zUdYmE>  

[← Back to index](../INDEX.md)

## 1. Dijkstra's Algorithm

We want the **cheapest cost** to go from `src` to `dst`, but we can take **at most `k` stops** (so at most `k+1` flights/edges).
Normal Dijkstra finds the cheapest path, but it ignores stop limits.  
So we treat a "state" as: (current city, how many stops used).
That way, reaching the same city with different stop counts is considered different, and we can enforce the limit.

We always expand the currently cheapest state first using a min-heap.
The first time we pop `dst`, that cost is the cheapest possible within the allowed stops.

```cpp
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        int INF = 1e9;
        vector<vector<pair<int, int>>> adj(n);
        vector<vector<int>> dist(n, vector<int>(k + 5, INF));

        for (auto& flight : flights) {
            adj[flight[0]].emplace_back(flight[1], flight[2]);
        }

        dist[src][0] = 0;
        priority_queue<tuple<int, int, int>,
                       vector<tuple<int, int, int>>, greater<>> minHeap;
        minHeap.emplace(0, src, -1);

        while (!minHeap.empty()) {
            auto [cst, node, stops] = minHeap.top();
            minHeap.pop();
            if (node == dst) return cst;
            if (stops == k || dist[node][stops + 1] < cst) continue;
            for (auto& [nei, w] : adj[node]) {
                int nextCst = cst + w;
                int nextStops = stops + 1;
                if (dist[nei][nextStops + 1] > nextCst) {
                    dist[nei][nextStops + 1] = nextCst;
                    minHeap.emplace(nextCst, nei, nextStops);
                }
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot K + m \cdot K \cdot \log(m \cdot K))$, commonly written as $O(m \cdot k \cdot \log(m \cdot k))$
- Space complexity: $O(m + n \cdot K + m \cdot K)$

> Where $n$ is the number of cities, $m$ is the number of flights, and $K = k + 1$ is the maximum number of flights/edges allowed. The layered graph has $O(n \cdot K)$ states and $O(m \cdot K)$ transitions. With the lazy priority queue used here, each successful relaxation can push one heap entry, so the heap operation cost is $\log(m \cdot K)$, and the heap can hold $O(m \cdot K)$ entries in the worst case. The adjacency list takes $O(m)$ space and `dist` takes $O(n \cdot K)$ space.

## 2. Bellman Ford Algorithm

We are allowed **at most `k` stops**, which means **at most `k + 1` flights (edges)**.
Bellman–Ford is perfect here because it relaxes edges **level by level**, where each iteration allows one more edge in the path.

Key idea:

- After `i` iterations, we know the cheapest cost to reach every city using at most `i` flights.
- By running the relaxation `k` + 1 times, we ensure we only consider paths that respect the stop limit.
- We use a temporary array each iteration so that paths from the same iteration don't chain together and accidentally exceed the allowed number of flights.

```cpp
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<int> prices(n, INT_MAX);
        prices[src] = 0;

        for (int i = 0; i <= k; i++) {
            vector<int> tmpPrices = prices;

            for (const auto& flight : flights) {
                int s = flight[0];
                int d = flight[1];
                int p = flight[2];

                if (prices[s] == INT_MAX)
                    continue;

                if (prices[s] + p < tmpPrices[d])
                    tmpPrices[d] = prices[s] + p;
            }

            prices = tmpPrices;
        }

        return prices[dst] == INT_MAX ? -1 : prices[dst];
    }
};
```

**Complexity**

- Time complexity: $O(n + (m * k))$
- Space complexity: $O(n)$

> Where $n$ is the number of cities, $m$ is the number of flights and $k$ is the number of stops.

## 3. Shortest Path Faster Algorithm

This problem is still about finding the **cheapest path with at most `k` stops**.  
SPFA (Shortest Path Faster Algorithm) is essentially a **queue-optimized Bellman–Ford**.

Key observations:

- Each time we relax an edge, we may improve the cost to reach a city.
- However, unlike classic shortest path problems, we must not exceed `k` stops.
- So every state in the queue must track:
    - the current city
    - the total cost so far
    - the number of stops used
- We only continue expanding a path if `stops` <= `k`.

This approach works well because:

- Only promising states (those that improve cost) are pushed into the queue.
- The stop constraint naturally prevents infinite relaxation loops.

```cpp
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<int> prices(n, INT_MAX);
        prices[src] = 0;
        vector<vector<pair<int, int>>> adj(n);
        for (const auto& flight : flights) {
            adj[flight[0]].emplace_back(flight[1], flight[2]);
        }

        queue<tuple<int, int, int>> q;
        q.push({0, src, 0});

        while (!q.empty()) {
            auto [cst, node, stops] = q.front();
            q.pop();
            if (stops > k) continue;

            for (const auto& neighbor : adj[node]) {
                int nei = neighbor.first, w = neighbor.second;
                int nextCost = cst + w;
                if (nextCost < prices[nei]) {
                    prices[nei] = nextCost;
                    q.push({nextCost, nei, stops + 1});
                }
            }
        }
        return prices[dst] == INT_MAX ? -1 : prices[dst];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n + m)$

> Where $n$ is the number of cities, $m$ is the number of flights and $k$ is the number of stops.

## Standalone solution file (`cpp/0787-cheapest-flights-within-k-stops.cpp` in the NeetCode repo)

```cpp
/**
  This function uses the Bellman-Ford algorithm to find the cheapest price from source (src) to destination (dst)
  with at most k stops allowed. It iteratively relaxes the edges for k+1 iterations, updating the minimum
  cost to reach each vertex. The final result is the minimum cost to reach the destination, or -1 if the
  destination is not reachable within the given constraints.
  
  Space Complexity: O(n) - space used for the prices array.
  Time Complexity: O(k * |flights|) - k iterations, processing all flights in each iteration.
 */
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<int> prices(n, INT_MAX);
        prices[src] = 0;

        // Perform k+1 iterations of Bellman-Ford algorithm.
        for (int i = 0; i < k + 1; i++) {
            vector<int> tmpPrices(begin(prices), end(prices));

            for (auto it : flights) {
                int s = it[0];
                int d = it[1];
                int p = it[2];

                if (prices[s] == INT_MAX) continue;

                if (prices[s] + p < tmpPrices[d]) {
                    tmpPrices[d] = prices[s] + p;
                }
            }
            prices = tmpPrices;
        }
        return prices[dst] == INT_MAX ? -1 : prices[dst];
    }
};


/*
    Given cities connected by flights [from,to,price], also given src, dst, & k:
    Return cheapest price from src to dst with at most k stops

    Dijkstra's but modified, normal won't work b/c will discard heap nodes w/o finishing
    Modify: need to re-consider a node if dist from source is shorter than what we recorded
    But, if we encounter node already processed but # of stops from source is lesser,
    Need to add it back to the heap to be considered again

    Time: O(V^2 log V) -> V = number of cities
    Space: O(V^2)
*/

class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        // build adjacency matrix
        vector<vector<int>> adj(n, vector<int>(n));
        for (int i = 0; i < flights.size(); i++) {
            vector<int> flight = flights[i];
            adj[flight[0]][flight[1]] = flight[2];
        }
        
        // shortest distances
        vector<int> distances(n, INT_MAX);
        distances[src] = 0;
        // shortest steps
        vector<int> currStops(n, INT_MAX);
        currStops[src] = 0;
        
        // priority queue -> (cost, node, stops)
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq;
        pq.push({0, src, 0});
        
        while (!pq.empty()) {
            int cost = pq.top()[0];
            int node = pq.top()[1];
            int stops = pq.top()[2];
            pq.pop();
            
            // if destination is reached, return cost to get here
            if (node == dst) {
                return cost;
            }
            
            // if no more steps left, continue
            if (stops == k + 1) {
                continue;
            }
            
            // check & relax all neighboring edges
            for (int neighbor = 0; neighbor < n; neighbor++) {
                if (adj[node][neighbor] > 0) {
                    int currCost = cost;
                    int neighborDist = distances[neighbor];
                    int neighborWeight = adj[node][neighbor];
                    
                    // check if better cost
                    int currDist = currCost + neighborWeight;
                    if (currDist < neighborDist || stops + 1 < currStops[neighbor]) {
                        pq.push({currDist, neighbor, stops + 1});
                        distances[neighbor] = currDist;
                        currStops[neighbor] = stops;
                    } else if (stops < currStops[neighbor]) {
                        // check if better steps
                        pq.push({currDist, neighbor, stops + 1});
                    }
                    currStops[neighbor] = stops;
                }
            }
        }
        
        if (distances[dst] == INT_MAX) {
            return -1;
        }
        return distances[dst];
    }
};
```
