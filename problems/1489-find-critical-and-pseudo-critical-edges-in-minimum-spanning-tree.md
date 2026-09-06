# 1489. Find Critical and Pseudo Critical Edges in Minimum Spanning Tree

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/>  
- **NeetCode:** <https://neetcode.io/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree>  
- **Video:** <https://www.youtube.com/watch?v=83JnUxrLKJU>  
- **Video approach:** 1. Kruskal's Algorithm - I  

[← Back to index](../INDEX.md)

## 1. Kruskal's Algorithm - I ▶ video

An edge is critical if removing it increases the MST weight or disconnects the graph. An edge is pseudo-critical if it can appear in some MST but is not mandatory. We test each edge by building the MST without it (to check criticality) and by forcing it into the MST first (to check if it can be part of a valid MST without increasing weight).

```cpp
class UnionFind {
public:
    vector<int> par, rank;

    UnionFind(int n) : par(n), rank(n, 1) {
        iota(par.begin(), par.end(), 0);
    }

    int find(int v) {
        if (v != par[v]) {
            par[v] = find(par[v]);
        }
        return par[v];
    }

    bool unionSets(int v1, int v2) {
        int p1 = find(v1), p2 = find(v2);
        if (p1 == p2) return false;
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

class Solution {
public:
    vector<vector<int>> findCriticalAndPseudoCriticalEdges(int n, vector<vector<int>>& edges) {
        vector<array<int, 4>> edgeList;
        for (int i = 0; i < edges.size(); ++i) {
            edgeList.push_back({ edges[i][0], edges[i][1], edges[i][2], i });
        }

        sort(edgeList.begin(), edgeList.end(), [](auto& a, auto& b) {
            return a[2] < b[2];
        });

        int mstWeight = 0;
        UnionFind uf(n);
        for (auto& edge : edgeList) {
            if (uf.unionSets(edge[0], edge[1])) {
                mstWeight += edge[2];
            }
        }

        vector<int> critical, pseudo;
        for (auto& edge : edgeList) {
            // Try without current edge
            UnionFind ufWithout(n);
            int weight = 0;
            for (auto& other : edgeList) {
                if (other[3] != edge[3] && ufWithout.unionSets(other[0], other[1])) {
                    weight += other[2];
                }
            }
            if (*max_element(ufWithout.rank.begin(), ufWithout.rank.end()) != n || weight > mstWeight) {
                critical.push_back(edge[3]);
                continue;
            }

            // Try with current edge
            UnionFind ufWith(n);
            ufWith.unionSets(edge[0], edge[1]);
            weight = edge[2];
            for (auto& other : edgeList) {
                if (ufWith.unionSets(other[0], other[1])) {
                    weight += other[2];
                }
            }
            if (weight == mstWeight) {
                pseudo.push_back(edge[3]);
            }
        }

        return { critical, pseudo };
    }
};
```

**Complexity**

- Time complexity: $O(E ^ 2)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Kruskal's Algorithm - II

This is a cleaner implementation of the same approach. We use a helper function `findMST` that optionally skips one edge or forces one edge to be included first. By comparing results against the baseline MST weight, we classify each edge as critical or pseudo-critical.

```cpp
class UnionFind {
private:
    int n;
    vector<int> Parent, Size;

public:
    UnionFind(int n) : n(n), Parent(n + 1), Size(n + 1, 1) {
        for (int i = 0; i <= n; ++i) {
            Parent[i] = i;
        }
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
        n--;
        if (Size[pu] < Size[pv]) {
            swap(pu, pv);
        }
        Size[pu] += Size[pv];
        Parent[pv] = pu;
        return true;
    }

    bool isConnected() {
        return n == 1;
    }
};

class Solution {
public:
    vector<vector<int>> findCriticalAndPseudoCriticalEdges(int n, vector<vector<int>>& edges) {
        for (int i = 0; i < edges.size(); ++i) {
            edges[i].push_back(i);
        }

        sort(edges.begin(), edges.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[2] < b[2];
        });

        auto findMST = [&](int index, bool include) -> int {
            UnionFind uf(n);
            int wgt = 0;
            if (include) {
                wgt += edges[index][2];
                uf.unionSets(edges[index][0], edges[index][1]);
            }
            for (int i = 0; i < edges.size(); ++i) {
                if (i == index) continue;
                if (uf.unionSets(edges[i][0], edges[i][1])) {
                    wgt += edges[i][2];
                }
            }
            return uf.isConnected() ? wgt : INT_MAX;
        };

        int mst_wgt = findMST(-1, false);
        vector<int> critical, pseudo;

        for (int i = 0; i < edges.size(); ++i) {
            if (mst_wgt < findMST(i, false)) {
                critical.push_back(edges[i][3]);
            } else if (mst_wgt == findMST(i, true)) {
                pseudo.push_back(edges[i][3]);
            }
        }

        return { critical, pseudo };
    }
};
```

**Complexity**

- Time complexity: $O(E ^ 2)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 3. Dijkstra's Algorithm

For each edge connecting nodes `u` and `v` with weight `w`, we ask: is there an alternate path from `u` to `v` using only edges with weight at most `w`? We use a modified Dijkstra that finds the minimax path (minimizing the maximum edge weight along the path). If the edge's weight is strictly less than the minimax without it, the edge is critical. If equal to the minimax, it is pseudo-critical.

```cpp
class Solution {
public:
    vector<vector<int>> findCriticalAndPseudoCriticalEdges(int n, vector<vector<int>>& edges) {
        for (int i = 0; i < edges.size(); ++i) {
            edges[i].push_back(i);
        }

        vector<vector<vector<int>>> adj(n);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back({edge[1], edge[2], edge[3]});
            adj[edge[1]].push_back({edge[0], edge[2], edge[3]});
        }

        auto minimax = [&](int src, int dst, int excludeIdx) -> int {
            vector<int> dist(n, INT_MAX);
            dist[src] = 0;

            priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
            pq.push({0, src});

            while (!pq.empty()) {
                auto [maxW, u] = pq.top();
                pq.pop();
                if (u == dst) return maxW;

                for (const auto& neighbor : adj[u]) {
                    int v = neighbor[0], weight = neighbor[1], edgeIdx = neighbor[2];
                    if (edgeIdx == excludeIdx) continue;
                    int newW = max(maxW, weight);
                    if (newW < dist[v]) {
                        dist[v] = newW;
                        pq.push({newW, v});
                    }
                }
            }
            return INT_MAX;
        };

        vector<int> critical, pseudo;
        for (const auto& edge : edges) {
            int u = edge[0], v = edge[1], w = edge[2], idx = edge[3];
            if (w < minimax(u, v, idx)) {
                critical.push_back(idx);
            } else if (w == minimax(u, v, -1)) {
                pseudo.push_back(idx);
            }
        }

        return {critical, pseudo};
    }
};
```

**Complexity**

- Time complexity: $O(E ^ 2 \log V)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 4. Kruskal's Algorithm + DFS

After building one MST, edges not in the MST create cycles when added. We use `DFS` to find the path in the MST between the endpoints of each non-MST edge. If any edge on this path has the same weight as the non-MST edge, both edges are pseudo-critical (they can be swapped). MST edges not identified as pseudo-critical are critical.

```cpp
class UnionFind {
    vector<int> parent, size;

public:
    UnionFind(int n) {
        parent.resize(n);
        size.resize(n, 1);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    int find(int node) {
        if (parent[node] != node) {
            parent[node] = find(parent[node]);
        }
        return parent[node];
    }

    bool unionSets(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (size[pu] < size[pv]) swap(pu, pv);
        size[pu] += size[pv];
        parent[pv] = pu;
        return true;
    }
};

class Solution {
    vector<vector<int>> mst;
    set<int> mstEdges, pseudoCriticalEdges;
    vector<int> path;
    int destination;

public:
    vector<vector<int>> findCriticalAndPseudoCriticalEdges(int n, vector<vector<int>>& edges) {
        mst.resize(n);
        vector<array<int, 4>> edgeList;
        for (int i = 0; i < edges.size(); ++i) {
            edgeList.push_back({edges[i][2], edges[i][0], edges[i][1], i});
        }
        sort(edgeList.begin(), edgeList.end());

        UnionFind uf(n);
        for (auto& [w, u, v, idx] : edgeList) {
            if (uf.unionSets(u, v)) {
                mst[u].push_back(idx);
                mst[v].push_back(idx);
                mstEdges.insert(idx);
            }
        }

        for (int i = 0; i < edges.size(); ++i) {
            if (mstEdges.count(i)) continue;
            path.clear();
            destination = edges[i][1];
            if (dfs(edges[i][0], -1, edges)) {
                for (int p : path) {
                    if (edges[p][2] == edges[i][2]) {
                        pseudoCriticalEdges.insert(p);
                        pseudoCriticalEdges.insert(i);
                    }
                }
            }
        }

        vector<int> critical;
        for (int e : mstEdges) {
            if (!pseudoCriticalEdges.count(e)) critical.push_back(e);
        }

        return {critical, vector<int>(pseudoCriticalEdges.begin(), pseudoCriticalEdges.end())};
    }

    bool dfs(int node, int parent, vector<vector<int>>& edges) {
        if (node == destination) return true;
        for (int& edgeIdx : mst[node]) {
            if (edgeIdx == parent) continue;
            path.push_back(edgeIdx);
            int next = edges[edgeIdx][0] == node ? edges[edgeIdx][1] : edges[edgeIdx][0];
            if (dfs(next, edgeIdx, edges)) return true;
            path.pop_back();
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(E ^ 2)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of vertices and $E$ is the number of edges.
