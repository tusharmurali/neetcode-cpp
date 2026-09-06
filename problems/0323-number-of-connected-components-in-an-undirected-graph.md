# 323. Number of Connected Components In An Undirected Graph

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/>  
- **NeetCode:** <https://neetcode.io/problems/count-connected-components>  
- **Video:** <https://www.youtube.com/watch?v=8f1XPm4WOUc>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A **connected component** is a group of nodes where every node is reachable from any other node in that group.

Using **DFS**:

- If we start DFS from an unvisited node, we will visit **all nodes in its connected component**
- Every time we start DFS from a new unvisited node, we’ve found **one new component**

```cpp
class Solution {
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        vector<bool> visit(n, false);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        int res = 0;
        for (int node = 0; node < n; ++node) {
            if (!visit[node]) {
                dfs(adj, visit, node);
                res++;
            }
        }
        return res;
    }

private:
    void dfs(const vector<vector<int>>& adj, vector<bool>& visit, int node) {
        visit[node] = true;
        for (int nei : adj[node]) {
            if (!visit[nei]) {
                dfs(adj, visit, nei);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph.

## 2. Breadth First Search

A **connected component** is a set of nodes where each node can reach the others.

Using **BFS**:

- Starting BFS from an unvisited node will visit **all nodes in that component**
- Each time we start BFS from a new unvisited node, we discover **one new connected component**

```cpp
class Solution {
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        vector<bool> visit(n, false);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        int res = 0;
        for (int node = 0; node < n; ++node) {
            if (!visit[node]) {
                bfs(adj, visit, node);
                res++;
            }
        }
        return res;
    }

private:
    void bfs(vector<vector<int>>& adj, vector<bool>& visit, int node) {
        queue<int> q;
        q.push(node);
        visit[node] = true;
        while (!q.empty()) {
            int cur = q.front();
            q.pop();
            for (int nei : adj[cur]) {
                if (!visit[nei]) {
                    visit[nei] = true;
                    q.push(nei);
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph.

## 3. Disjoint Set Union (Rank | Size)

Disjoint Set Union (DSU) groups nodes into **connected components** efficiently.

- Start by assuming **each node is its own component**
- When we process an edge `(u, v)`:
    - If `u` and `v` are already in the same set, nothing changes
    - If they are in different sets, we **merge** them and the number of components decreases by 1
- Using **union by rank/size + path compression** keeps operations fast

At the end, the number of remaining sets is the number of connected components.

```cpp
class DSU {
public:
    vector<int> parent;
    vector<int> rank;

    DSU(int n) {
        parent.resize(n);
        rank.resize(n, 1);
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }

    int find(int node) {
        int cur = node;
        while (cur != parent[cur]) {
            parent[cur] = parent[parent[cur]];
            cur = parent[cur];
        }
        return cur;
    }

    bool unionSets(int u, int v) {
        int pu = find(u);
        int pv = find(v);
        if (pu == pv) {
            return false;
        }
        if (rank[pv] > rank[pu]) {
            swap(pu, pv);
        }
        parent[pv] = pu;
        rank[pu] += rank[pv];
        return true;
    }
};

class Solution {
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        DSU dsu(n);
        int res = n;
        for (auto& edge : edges) {
            if (dsu.unionSets(edge[0], edge[1])) {
                res--;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + (E * α(V)))$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph. $α()$ is used for amortized complexity.

## Standalone solution file (`cpp/0323-number-of-connected-components-in-an-undirected-graph.cpp` in the NeetCode repo)

```cpp
/*
    Graph of n nodes, given edges array, return # of connected components
    Ex. n = 5, edges = [[0,1],[1,2],[3,4]] -> 2

    Union find, for each edge combine, if already in same set keep traversing
    If not in same set, decrement count by 1, count will store # of components

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        vector<int> parents;
        vector<int> ranks;
        for (int i = 0; i < n; i++) {
            parents.push_back(i);
            ranks.push_back(1);
        }
        
        int result = n;
        for (int i = 0; i < edges.size(); i++) {
            int n1 = edges[i][0];
            int n2 = edges[i][1];
            result -= doUnion(parents, ranks, n1, n2);
        }
        return result;
    }
private:
    int doFind(vector<int>& parents, int n) {
        int p = parents[n];
        while (p != parents[p]) {
            parents[p] = parents[parents[p]];
            p = parents[p];
        }
        return p;
    }
    
    int doUnion(vector<int>& parents, vector<int>& ranks, int n1, int n2) {
        int p1 = doFind(parents, n1);
        int p2 = doFind(parents, n2);
        if (p1 == p2) {
            return 0;
        }
        
        if (ranks[p1] > ranks[p2]) {
            parents[p2] = p1;
            ranks[p1] += ranks[p2];
        } else {
            parents[p1] = p2;
            ranks[p2] += ranks[p1];
        }
        
        return 1;
    }
};
```
