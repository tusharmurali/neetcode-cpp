# 2477. Minimum Fuel Cost to Report to the Capital

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-fuel-cost-to-report-to-the-capital/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-fuel-cost-to-report-to-the-capital>  
- **Video:** <https://www.youtube.com/watch?v=I3lnDUIzIG4>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Think of the tree as a network of cities where everyone needs to travel to the capital (node `0`). Since the tree structure means there's only one path from any city to the capital, we can work backwards from the leaves.

The key insight is that as we move toward the capital, passengers accumulate. At each node, we collect all the people from its subtree, and the number of cars needed to transport them equals the ceiling of passengers divided by seats. By using `dfs` to traverse from leaves to the root, we can count passengers bottom-up and calculate fuel costs as people flow toward the capital.

```cpp
class Solution {
private:
    vector<vector<int>> adj;
    long long res = 0;

public:
    long long minimumFuelCost(vector<vector<int>>& roads, int seats) {
        int n = roads.size() + 1;
        adj.resize(n);

        for (auto& road : roads) {
            adj[road[0]].push_back(road[1]);
            adj[road[1]].push_back(road[0]);
        }

        dfs(0, -1, seats);
        return res;
    }

private:
    int dfs(int node, int parent, int seats) {
        int passengers = 0;
        for (int child : adj[node]) {
            if (child != parent) {
                int p = dfs(child, node, seats);
                passengers += p;
                res += ceil((double) p / seats);
            }
        }
        return passengers + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Topological Sort (Kahn's Algorithm)

Instead of recursion, we can process the tree level by level starting from the leaf nodes. Leaves have only one connection, so we identify them by their degree. As each leaf "sends" its passengers toward the capital, we remove it from consideration and check if its neighbor becomes a new leaf.

This approach simulates the natural flow of people gathering and moving inward. Each time a node is processed, we calculate how many cars are needed to transport its passengers one step closer to the root.

```cpp
class Solution {
public:
    long long minimumFuelCost(vector<vector<int>>& roads, int seats) {
        int n = roads.size() + 1;
        vector<vector<int>> adj(n);
        vector<int> indegree(n, 0), passengers(n, 1);
        long long res = 0;

        for (auto& road : roads) {
            int src = road[0], dst = road[1];
            adj[src].push_back(dst);
            adj[dst].push_back(src);
            indegree[src]++;
            indegree[dst]++;
        }

        queue<int> q;
        for (int i = 1; i < n; i++) {
            if (indegree[i] == 1) q.push(i);
        }

        while (!q.empty()) {
            int node = q.front();q.pop();
            res += ceil((double) passengers[node] / seats);
            for (int parent : adj[node]) {
                if (--indegree[parent] == 1 && parent != 0) q.push(parent);
                passengers[parent] += passengers[node];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
