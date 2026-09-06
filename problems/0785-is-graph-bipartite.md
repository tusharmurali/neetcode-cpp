# 785. Is Graph Bipartite?

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/is-graph-bipartite/>  
- **NeetCode:** <https://neetcode.io/problems/is-graph-bipartite>  
- **Video:** <https://www.youtube.com/watch?v=mev55LTubBY>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A graph is bipartite if we can split its nodes into two groups such that every edge connects nodes from different groups. This is equivalent to checking if the graph is 2-colorable. Using DFS, we assign a color to the starting node and then assign the opposite color to all its neighbors. If we ever find a neighbor that already has the same color as the current node, the graph is not bipartite. Since the graph may be disconnected, we run `dfs` from every unvisited node.

```cpp
class Solution {
private:
    vector<int> color;

    bool dfs(vector<vector<int>>& graph, int i, int c) {
        color[i] = c;
        for (int nei : graph[i]) {
            if (color[nei] == c) {
                return false;
            }
            if (color[nei] == 0 && !dfs(graph, nei, -c)) {
                return false;
            }
        }
        return true;
    }

public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        color.assign(n, 0); // Map node i -> odd=1, even=-1

        for (int i = 0; i < n; i++) {
            if (color[i] == 0 && !dfs(graph, i, 1)) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Breadth First Search

BFS provides another way to check 2-colorability. Starting from an uncolored node, we assign it a color and add it to a queue. For each node we process, we check all neighbors: if a neighbor has the same color, the graph is not bipartite; if uncolored, we assign it the opposite color and enqueue it. BFS naturally explores the graph level by level, alternating colors between levels.

```cpp
class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n, 0); // Map node i -> odd=1, even=-1

        for (int i = 0; i < n; i++) {
            if (color[i] != 0) continue;
            queue<int> q;
            q.push(i);
            color[i] = -1;

            while (!q.empty()) {
                int node = q.front();
                q.pop();
                for (int nei : graph[node]) {
                    if (color[nei] == color[node]) {
                        return false;
                    } else if (color[nei] == 0) {
                        q.push(nei);
                        color[nei] = -color[node];
                    }
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 3. Iterative DFS

Iterative DFS uses an explicit stack instead of recursion to traverse the graph. The coloring logic remains the same: assign a color to a node, then process all neighbors by checking for conflicts and pushing uncolored neighbors onto the stack with the opposite color. This avoids potential stack overflow issues with very deep graphs while achieving the same result as recursive DFS.

```cpp
class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n); // Map node i -> odd=1, even=-1
        stack<int> stack;

        for (int i = 0; i < n; i++) {
            if (color[i] != 0) continue;
            color[i] = -1;
            stack.push(i);
            while (!stack.empty()) {
                int node = stack.top();
                stack.pop();
                for (int nei : graph[node]) {
                    if (color[node] == color[nei]) return false;
                    if (color[nei] == 0) {
                        stack.push(nei);
                        color[nei] = -color[node];
                    }
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 4. Disjoint Set Union

DSU (Union-Find) offers an alternative perspective. For a bipartite graph, a node must be in a different set than all of its neighbors, but all neighbors should belong to the same set. For each node, we union all its neighbors together. If a node ever ends up in the same set as one of its neighbors, the graph is not bipartite. This works because being in the same connected component in the neighbor graph implies they must share a color in a valid 2-coloring.

```cpp
class DSU {
private:
    vector<int> Parent, Size;

public:
    DSU(int n) {
        Parent.resize(n);
        Size.resize(n, 0);
        for (int i = 0; i < n; i++) {
            Parent[i] = i;
        }
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionSet(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (Size[pu] > Size[pv]) {
            Parent[pv] = pu;
        } else if (Size[pu] < Size[pv]) {
            Parent[pu] = pv;
        } else {
            Parent[pv] = pu;
            Size[pu]++;
        }
        return true;
    }
};

class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        DSU dsu(n);

        for (int node = 0; node < n; node++) {
            for (int& nei : graph[node]) {
                if (dsu.find(node) == dsu.find(nei)) {
                    return false;
                }
                dsu.unionSet(graph[node][0], nei);
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + (E * α(V)))$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges. $α()$ is used for amortized complexity.
