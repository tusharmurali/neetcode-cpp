# 547. Number of Provinces

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-provinces/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-provinces>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A province is a group of directly or indirectly connected cities. This is essentially finding the number of connected components in an undirected graph. We can use DFS to explore all cities reachable from a starting city, marking them as visited. Each time we start a new DFS from an unvisited city, we have found a new province.

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        vector<bool> visited(n, false);
        int res = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfs(i, isConnected, visited, n);
                res++;
            }
        }
        return res;
    }

    void dfs(int node, vector<vector<int>>& isConnected, vector<bool>& visited, int n) {
        visited[node] = true;
        for (int nei = 0; nei < n; nei++) {
            if (isConnected[node][nei] == 1 && !visited[nei]) {
                dfs(nei, isConnected, visited, n);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Depth First Search (Modifying Input)

Instead of using a separate visited array, we can use the diagonal of the adjacency matrix itself to track visited status. Since `isConnected[i][i]` is always `1` (a city is connected to itself), we can set it to `0` when we visit that city. This saves space but modifies the input.

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        int res = 0;

        for (int i = 0; i < n; i++) {
            if (isConnected[i][i] == 1) {
                dfs(i, isConnected, n);
                res++;
            }
        }
        return res;
    }

    void dfs(int node, vector<vector<int>>& isConnected, int n) {
        isConnected[node][node] = 0;
        for (int nei = 0; nei < n; nei++) {
            if (node != nei && isConnected[node][nei] == 1 && isConnected[nei][nei] == 1) {
                dfs(nei, isConnected, n);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Breadth First Search

`BFS` provides an alternative to `DFS` for exploring connected components. Instead of going deep first, we explore all neighbors at the current level before moving to the next. The logic remains the same: start from an unvisited city, explore all reachable cities using a queue, and count each new starting point as a separate province.

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        vector<bool> visited(n, false);
        queue<int> q;
        int res = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                res++;
                visited[i] = true;
                q.push(i);
                while (!q.empty()) {
                    int node = q.front(); q.pop();
                    for (int nei = 0; nei < n; nei++) {
                        if (isConnected[node][nei] && !visited[nei]) {
                            visited[nei] = true;
                            q.push(nei);
                        }
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Disjoint Set Union

The Union-Find (Disjoint Set Union) data structure is designed for efficiently managing connected components. We start with each city as its own component. As we process connections, we union the components of connected cities. The final number of distinct components equals the number of provinces. Path compression and union by size optimizations make this approach nearly `O(1)` per operation.

```cpp
class DSU {
public:
    vector<int> Parent, Size;
    int components;

    DSU(int n) {
        Parent.resize(n);
        Size.assign(n, 1);
        components = n;
        for (int i = 0; i < n; ++i) Parent[i] = i;
    }

    int find(int node) {
        if (Parent[node] != node)
            Parent[node] = find(Parent[node]);
        return Parent[node];
    }

    bool unionSet(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;

        components--;
        if (Size[pu] >= Size[pv]) {
            Size[pu] += Size[pv];
            Parent[pv] = pu;
        } else {
            Size[pv] += Size[pu];
            Parent[pu] = pv;
        }
        return true;
    }

    int numOfComps() {
        return components;
    }
};

class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        DSU dsu(n);
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (isConnected[i][j])
                    dsu.unionSet(i, j);
        return dsu.numOfComps();
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$
