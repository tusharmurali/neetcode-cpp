# 684. Redundant Connection

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/redundant-connection/>  
- **NeetCode:** <https://neetcode.io/problems/redundant-connection>  
- **Video:** <https://www.youtube.com/watch?v=1lNK80tOTfc>  
- **Video approach:** 4. Disjoint Set Union  

[← Back to index](../INDEX.md)

## 1. Cycle Detection (DFS)

A **tree** cannot contain a cycle.
While adding edges one by one, the **first edge that creates a cycle** is the redundant connection.

For each new edge `(u, v)`:

- Temporarily add it to the graph
- Run `dfs` to check if a cycle exists
- If `dfs` revisits a node (not coming from its parent), a cycle is formed
  → that edge is the answer

```cpp
class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        vector<vector<int>> adj(n + 1);

        for (const auto& edge : edges) {
            int u = edge[0], v = edge[1];
            adj[u].push_back(v);
            adj[v].push_back(u);
            vector<bool> visit(n + 1, false);

            if (dfs(u, -1, adj, visit)) {
                return {u, v};
            }
        }
        return {};
    }

private:
    bool dfs(int node, int parent,
             vector<vector<int>>& adj, vector<bool>& visit) {
        if (visit[node]) return true;
        visit[node] = true;
        for (int nei : adj[node]) {
            if (nei == parent) continue;
            if (dfs(nei, node, adj, visit)) return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(E * (V + E))$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph.

## 2. Depth First Search (Optimal)

Instead of checking for a cycle **after every edge**, we build the whole graph once and find the **cycle nodes** in a single `dfs`.

Key idea:

- In an undirected graph made from `n` edges on `n` nodes, there is exactly **one cycle**.
- During `dfs`, if we reach a node that is already `visited`, we just found the **start of the cycle**.
- While recursion "unwinds" back, we mark every node on that return path as part of the cycle, until we come back to the cycle start.

After we have the set `cycle` (all nodes that lie on the cycle):

- The redundant edge must connect **two cycle nodes**.
- The problem asks for the edge that appears **last** in the input among the cycle edges,
  so we scan edges from the end and return the first edge `(u, v)` where `u` and `v` are both in `cycle`.

```cpp
class Solution {
    vector<bool> visit;
    vector<vector<int>> adj;
    unordered_set<int> cycle;
    int cycleStart;
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        adj.resize(n + 1);
        for (auto& edge : edges) {
            int u = edge[0], v = edge[1];
            adj[u].push_back(v);
            adj[v].push_back(u);
        }

        visit.resize(n + 1, false);
        cycleStart = -1;
        dfs(1, -1);

        for (int i = edges.size() - 1; i >= 0; i--) {
            int u = edges[i][0], v = edges[i][1];
            if (cycle.count(u) && cycle.count(v)) {
                return {u, v};
            }
        }
        return {};
    }

private:
    bool dfs(int node, int par) {
        if (visit[node]) {
            cycleStart = node;
            return true;
        }
        visit[node] = true;
        for (int nei : adj[node]) {
            if (nei == par) continue;
            if (dfs(nei, node)) {
                if (cycleStart != -1) cycle.insert(node);
                if (node == cycleStart) {
                    cycleStart = -1;
                }
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph.

## 3. Topological Sort (Kahn's Algorithm)

This uses the **"peel off leaves"** idea (often called topological trimming).
Even though the graph is undirected, we can still remove nodes with degree `1` repeatedly:

- Nodes with degree `1` **cannot** be inside a cycle (a cycle needs every node to have degree ≥ 2).
- So we push all degree-1 nodes into a queue and remove them.
- When we remove a node, its neighbor's degree decreases; that neighbor might become a new leaf (degree 1), so we remove it next.
- After this process finishes, the only nodes left with degree > 0 are exactly the **cycle nodes**.

Finally, the redundant edge must be an edge whose both ends are still in the cycle.
Because we need the **last such edge** in input order, we scan `edges` in reverse and return the first edge connecting two remaining cycle nodes.

```cpp
class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        vector<int> indegree(n + 1, 0);
        vector<vector<int>> adj(n + 1);
        for (auto& edge : edges) {
            int u = edge[0], v = edge[1];
            adj[u].push_back(v);
            adj[v].push_back(u);
            indegree[u]++;
            indegree[v]++;
        }

        queue<int> q;
        for (int i = 1; i <= n; i++) {
            if (indegree[i] == 1) q.push(i);
        }

        while (!q.empty()) {
            int node = q.front(); q.pop();
            indegree[node]--;
            for (int nei : adj[node]) {
                indegree[nei]--;
                if (indegree[nei] == 1) q.push(nei);
            }
        }

        for (int i = edges.size() - 1; i >= 0; i--) {
            int u = edges[i][0], v = edges[i][1];
            if (indegree[u] == 2 && indegree[v])
                return {u, v};
        }
        return {};
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph.

## 4. Disjoint Set Union ▶ video

Use **Disjoint Set Union (Union-Find)** to track connected components while adding edges one by one.

- Initially, every node is its own component.
- When we add an edge `(u, v)`:
    - If `u` and `v` are already in the **same component**, adding this edge creates a **cycle**.
    - That edge is exactly the **redundant connection**.
- If they are in different components, we safely merge them.

Because edges are processed in order, the **first edge that fails to union** is the answer.

```cpp
class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        vector<int> par(n + 1), rank(n + 1, 1);
        for (int i = 0; i <= n; ++i)
            par[i] = i;

        for (const auto& edge : edges) {
            if (!Union(par, rank, edge[0], edge[1]))
                return vector<int>{ edge[0], edge[1] };
        }
        return {};
    }

private:
    int Find(vector<int>& par, int n) {
        int p = par[n];
        while (p != par[p]) {
            par[p] = par[par[p]];
            p = par[p];
        }
        return p;
    }

    bool Union(vector<int>& par, vector<int>& rank, int n1, int n2) {
        int p1 = Find(par, n1);
        int p2 = Find(par, n2);

        if (p1 == p2)
            return false;
        if (rank[p1] > rank[p2]) {
            par[p2] = p1;
            rank[p1] += rank[p2];
        } else {
            par[p1] = p2;
            rank[p2] += rank[p1];
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + (E * α(V)))$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges in the graph. $α()$ is used for amortized complexity.

## Standalone solution file (`cpp/0684-redundant-connection.cpp` in the NeetCode repo)

```cpp
/*
    Given undirected graph, return an edge that can be removed to make a tree
    Ex. edges = [[1,2],[1,3],[2,3]] -> [2,3]

    If n nodes & n edges, guaranteed a cycle
    How to know creating cycle? When connecting a node already connected
    Union Find: can find this redundant edge, track parents & ranks

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        
        vector<int> parents;
        vector<int> ranks;
        for (int i = 0; i < n + 1; i++) {
            parents.push_back(i);
            ranks.push_back(1);
            
        }
        
        vector<int> result;
        for (int i = 0; i < n; i++) {
            int n1 = edges[i][0];
            int n2 = edges[i][1];
            if (!doUnion(parents, ranks, n1, n2)) {
                result = {n1, n2};
                break;
            }
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
    
    bool doUnion(vector<int>& parents, vector<int>& ranks, int n1, int n2) {
        int p1 = doFind(parents, n1);
        int p2 = doFind(parents, n2);
        if (p1 == p2) {
            return false;
        }
        
        if (ranks[p1] > ranks[p2]) {
            parents[p2] = p1;
            ranks[p1] += ranks[p2];
        } else {
            parents[p1] = p2;
            ranks[p2] += ranks[p1];
        }
        
        return true;
    }
};
```
