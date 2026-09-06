# 2101. Detonate the Maximum Bombs

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/detonate-the-maximum-bombs/>  
- **NeetCode:** <https://neetcode.io/problems/detonate-the-maximum-bombs>  
- **Video:** <https://www.youtube.com/watch?v=8NPbAvVXKR4>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

When a bomb detonates, it triggers other bombs within its blast radius. This creates a chain reaction that can be modeled as a directed graph. Bomb A has an edge to bomb B if B is within A's blast radius. Note that this relationship is not symmetric since bombs have different radii. To find the maximum detonation, we try detonating each bomb and use DFS to count how many bombs explode in the chain reaction.

```cpp
class Solution {
public:
    int maximumDetonation(vector<vector<int>>& bombs) {
        int n = bombs.size();
        vector<vector<int>> adj(n);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                long long x1 = bombs[i][0], y1 = bombs[i][1], r1 = bombs[i][2];
                long long x2 = bombs[j][0], y2 = bombs[j][1], r2 = bombs[j][2];
                long long d = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);

                if (d <= r1 * r1) {
                    adj[i].push_back(j);
                }
                if (d <= r2 * r2) {
                    adj[j].push_back(i);
                }
            }
        }

        int res = 0;
        for (int i = 0; i < n; i++) {
            unordered_set<int> visit;
            res = max(res, dfs(i, visit, adj));
        }
        return res;
    }

private:
    int dfs(int i, unordered_set<int>& visit, vector<vector<int>>& adj) {
        if (!visit.insert(i).second) return 0;
        for (int nei : adj[i]) {
            dfs(nei, visit, adj);
        }
        return visit.size();
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 2. Breadth First Search

The chain reaction of bomb detonations can also be explored level by level using BFS. Starting from an initial bomb, we explore all bombs it directly triggers, then all bombs those trigger, and so on. This approach naturally models the wave-like spread of explosions.

```cpp
class Solution {
public:
    int maximumDetonation(vector<vector<int>>& bombs) {
        int n = bombs.size();
        vector<vector<int>> adj(n);

        for (int i = 0; i < n; i++) {
            int x1 = bombs[i][0], y1 = bombs[i][1], r1 = bombs[i][2];
            for (int j = i + 1; j < n; j++) {
                int x2 = bombs[j][0], y2 = bombs[j][1], r2 = bombs[j][2];
                long long d = (x1 - x2) * 1LL * (x1 - x2) + (y1 - y2) * 1LL * (y1 - y2);

                if (d <= (long long) r1 * r1) adj[i].push_back(j);
                if (d <= (long long) r2 * r2) adj[j].push_back(i);
            }
        }

        int res = 0;
        for (int i = 0; i < n; i++) {
            queue<int> q;
            vector<bool> visit(n, false);
            q.push(i);
            visit[i] = true;
            int count = 1;

            while (!q.empty()) {
                int node = q.front();q.pop();
                for (int& nei : adj[node]) {
                    if (!visit[nei]) {
                        visit[nei] = true;
                        count++;
                        q.push(nei);
                    }
                }
            }
            res = max(res, count);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 3. Iterative DFS

This is the same approach as recursive DFS but uses an explicit stack instead of the call stack. This avoids potential stack overflow issues for very large inputs and can be more efficient in some languages due to reduced function call overhead.

```cpp
class Solution {
public:
    int maximumDetonation(vector<vector<int>>& bombs) {
        int n = bombs.size();
        vector<vector<int>> adj(n);

        for (int i = 0; i < n; i++) {
            int x1 = bombs[i][0], y1 = bombs[i][1], r1 = bombs[i][2];
            for (int j = i + 1; j < n; j++) {
                int x2 = bombs[j][0], y2 = bombs[j][1], r2 = bombs[j][2];
                long long d = (long long)(x1 - x2) * (x1 - x2) + (long long)(y1 - y2) * (y1 - y2);

                if (d <= (long long) r1 * r1) adj[i].push_back(j);
                if (d <= (long long) r2 * r2) adj[j].push_back(i);
            }
        }

        int res = 0;
        for (int i = 0; i < n; i++) {
            stack<int> stk;
            vector<bool> visit(n, false);
            stk.push(i);
            visit[i] = true;
            int count = 1;

            while (!stk.empty()) {
                int node = stk.top();stk.pop();
                for (int& nei : adj[node]) {
                    if (!visit[nei]) {
                        visit[nei] = true;
                        count++;
                        stk.push(nei);
                    }
                }
            }
            res = max(res, count);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$
