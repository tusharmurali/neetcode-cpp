# 1376. Time Needed to Inform All Employees

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/time-needed-to-inform-all-employees/>  
- **NeetCode:** <https://neetcode.io/problems/time-needed-to-inform-all-employees>  
- **Video:** <https://www.youtube.com/watch?v=zdBYi0p4L5Q>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

The company structure forms a tree with the head of the company as the root. Each manager must inform their direct subordinates, who then inform their subordinates, and so on. The total time to inform everyone equals the longest path from the root to any leaf, where each edge weight is the manager's inform time.

We can traverse this tree using `dfs`, tracking the accumulated time as we go deeper. At each node, we add that manager's inform time before visiting their subordinates. The answer is the maximum time across all leaf nodes.

```cpp
class Solution {
public:
    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        vector<vector<int>> adj(n);
        for (int i = 0; i < n; i++) {
            if (i != headID) {
                adj[manager[i]].push_back(i);
            }
        }
        return dfs(headID, adj, informTime);
    }

private:
    int dfs(int node, vector<vector<int>>& adj, vector<int>& informTime) {
        int res = 0;
        for (int child : adj[node]) {
            res = max(res, informTime[node] + dfs(child, adj, informTime));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search

Instead of using recursion, we can traverse the tree level by level using `bfs`. We process nodes in waves, tracking the time at which each employee receives the news. The maximum time across all employees gives us the answer.

Each node in the queue stores both the employee ID and the time at which they were informed. When we process a node, we inform all their direct reports, adding the manager's inform time to compute when each subordinate receives the news.

```cpp
class Solution {
public:
    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        unordered_map<int, vector<int>> adj;
        for (int i = 0; i < n; ++i) {
            adj[manager[i]].push_back(i);
        }

        queue<pair<int, int>> q; // {id, time}
        q.push({headID, 0});
        int res = 0;

        while (!q.empty()) {
            auto [id, time] = q.front();
            q.pop();
            res = max(res, time);
            for (int emp : adj[id]) {
                q.push({emp, time + informTime[id]});
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Topological Sort (Kahn's Algorithm)

We can reverse our thinking: instead of propagating time down from the root, we can compute times bottom-up starting from leaf employees. Leaf employees have an `indegree` of `0` (no one reports to them). They propagate their total time upward to their managers.

A manager's total time is the maximum among all their subordinates' times plus their own inform time. We process employees in topological order, from leaves toward the root. When all of a manager's subordinates have been processed, we can compute and propagate the manager's time.

```cpp
class Solution {
public:
    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        vector<int> indegree(n, 0);
        vector<int> time(n, 0);

        for (int i = 0; i < n; ++i) {
            if (manager[i] != -1) {
                indegree[manager[i]]++;
            }
        }

        queue<int> queue;
        for (int i = 0; i < n; ++i) {
            if (indegree[i] == 0) {
                queue.push(i);
            }
        }

        while (!queue.empty()) {
            int node = queue.front();
            queue.pop();
            time[node] += informTime[node];
            if (manager[node] != -1) {
                time[manager[node]] = max(time[manager[node]], time[node]);
                indegree[manager[node]]--;
                if (indegree[manager[node]] == 0) {
                    queue.push(manager[node]);
                }
            }
        }

        return time[headID];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Depth First Search (Optimal)

Instead of building an explicit adjacency list, we can traverse from each employee up to the root, caching results along the way. For any employee, their total inform time is their own inform time plus their manager's total inform time.

We use the manager array directly for traversal and cache computed results in the inform time array itself. Once an employee's path to root is computed, we mark their manager as `-1` to indicate completion. This approach uses path compression similar to Union-Find.

```cpp
class Solution {
public:
    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        function<int(int)> dfs = [&](int node) {
            if (manager[node] != -1) {
                informTime[node] += dfs(manager[node]);
                manager[node] = -1;
            }
            return informTime[node];
        };

        int res = 0;
        for (int node = 0; node < n; ++node) {
            res = max(res, dfs(node));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.
