# 1579. Remove Max Number of Edges to Keep Graph Fully Traversable

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/>  
- **NeetCode:** <https://neetcode.io/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable>  
- **Video:** <https://www.youtube.com/watch?v=booGwg5wYm4>  

[← Back to index](../INDEX.md)

## 1. Disjoint Set Union

We need to keep both Alice and Bob connected across all nodes while removing as many edges as possible.
Type 3 edges (usable by both) are most valuable since they count toward connectivity for both users simultaneously.
We use two separate Union-Find structures to track connectivity for Alice and Bob independently.
By processing type 3 edges first, we maximize their usage, then fill in gaps with type 1 (Alice-only) and type 2 (Bob-only) edges.

```cpp
class DSU {
private:
    vector<int> parent, size;
    int n;

public:
    DSU(int n) : n(n), parent(n + 1), size(n + 1, 1) {
        for (int i = 0; i <= n; i++) {
            parent[i] = i;
        }
    }

    int find(int node) {
        if (parent[node] != node) {
            parent[node] = find(parent[node]);
        }
        return parent[node];
    }

    int unionSets(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) {
            return 0;
        }
        if (size[pu] < size[pv]) {
            swap(pu, pv);
        }
        size[pu] += size[pv];
        parent[pv] = pu;
        n--;
        return 1;
    }

    bool isConnected() {
        return n == 1;
    }
};

class Solution {
public:
    int maxNumEdgesToRemove(int n, vector<vector<int>>& edges) {
        DSU alice(n), bob(n);
        int cnt = 0;

        for (auto& edge : edges) {
            if (edge[0] == 3) {
                cnt += (alice.unionSets(edge[1], edge[2]) | bob.unionSets(edge[1], edge[2]));
            }
        }

        for (auto& edge : edges) {
            if (edge[0] == 1) {
                cnt += alice.unionSets(edge[1], edge[2]);
            } else if (edge[0] == 2) {
                cnt += bob.unionSets(edge[1], edge[2]);
            }
        }

        if (alice.isConnected() && bob.isConnected()) {
            return edges.size() - cnt;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(E * α(V))$
- Space complexity: $O(V)$

> Where $V$ is the number of verticies and $E$ is the number of edges.
