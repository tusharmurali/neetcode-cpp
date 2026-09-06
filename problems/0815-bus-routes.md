# 815. Bus Routes

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/bus-routes/>  
- **NeetCode:** <https://neetcode.io/problems/bus-routes>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search (Stops as Nodes)

This is a shortest path problem where we want to find the minimum number of buses needed to travel from a source stop to a target stop. We can model this as a graph problem where stops are nodes, and we use BFS to find the shortest path in terms of bus transfers.

The key insight is that when we board a bus, we can reach all stops on that route. So from any stop, we can transition to all other stops on any bus that serves that stop. We count bus transfers (not individual stops) to measure distance.

```cpp
class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int source, int target) {
        if (source == target) return 0;
        int n = routes.size();
        unordered_map<int, vector<int>> stops;
        for (int bus = 0; bus < n; bus++) {
            for (int stop : routes[bus]) {
                stops[stop].push_back(bus);
            }
        }

        unordered_set<int> seenBus;
        unordered_set<int> seenStop;
        seenStop.insert(source);
        queue<int> q;
        q.push(source);
        int res = 0;

        while (!q.empty()) {
            int size = q.size();
            for (int k = 0; k < size; k++) {
                int stop = q.front(); q.pop();
                if (stop == target) return res;
                for (int bus : stops[stop]) {
                    if (seenBus.count(bus)) continue;
                    seenBus.insert(bus);
                    for (int nxtStop : routes[bus]) {
                        if (seenStop.count(nxtStop)) continue;
                        seenStop.insert(nxtStop);
                        q.push(nxtStop);
                    }
                }
            }
            res++;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of routes and $m$ is the maximum number of stops per bus route.

## 2. Breadth First Search (Routes as Nodes)

Instead of treating stops as nodes, we can treat bus routes as nodes. Two routes are connected if they share at least one common stop (you can transfer between them). This transforms the problem into finding the shortest path between any route containing the source stop and any route containing the target stop.

This approach can be more efficient when there are many stops but fewer routes, as we traverse through routes rather than individual stops.

```cpp
class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int source, int target) {
        if (source == target) return 0;

        int n = routes.size();
        vector<vector<int>> adjList(n);
        unordered_map<int, vector<int>> stopToRoutes;
        for (int bus = 0; bus < n; bus++) {
            for (int stop : routes[bus]) {
                stopToRoutes[stop].push_back(bus);
            }
        }

        if (!stopToRoutes.count(source) || !stopToRoutes.count(target)) return -1;

        vector<vector<bool>> hasEdge(n, vector<bool>(n, false));
        for (auto& [stop, buses] : stopToRoutes) {
            for (int i = 0; i < (int)buses.size(); i++) {
                for (int j = i + 1; j < (int)buses.size(); j++) {
                    int b1 = buses[i], b2 = buses[j];
                    if (!hasEdge[b1][b2]) {
                        hasEdge[b1][b2] = hasEdge[b2][b1] = true;
                        adjList[b1].push_back(b2);
                        adjList[b2].push_back(b1);
                    }
                }
            }
        }

        queue<int> q;
        for (int bus : stopToRoutes[source]) q.push(bus);

        int res = 1;
        while (!q.empty()) {
            int size = q.size();
            for (int k = 0; k < size; k++) {
                int node = q.front(); q.pop();
                if (find(stopToRoutes[target].begin(), stopToRoutes[target].end(), node) != stopToRoutes[target].end()) {
                    return res;
                }
                while (!adjList[node].empty()) {
                    int nxtBus = adjList[node].back();
                    adjList[node].pop_back();
                    if (!adjList[nxtBus].empty()) {
                        q.push(nxtBus);
                    }
                }
            }
            res++;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 + n * m)$
- Space complexity: $O(n ^ 2 + n * m)$

> Where $n$ is the number of routes and $m$ is the maximum number of stops per bus route.
