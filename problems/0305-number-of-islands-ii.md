# 305. Number of Islands II

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-islands-ii/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-islands-ii>  

[← Back to index](../INDEX.md)

## 1. Union Find

We need to track islands dynamically as land cells are added one at a time. Union-Find is ideal for this because it efficiently merges sets and counts distinct groups. Each time we add a land cell, we check its four neighbors. If a neighbor is already land, we union the new cell with that neighbor. The island count increases by `1` for each new land cell added, then decreases by `1` for each successful union with an adjacent island.

```cpp
class UnionFind {
private:
    vector<int> parent, rank;
    int count;

public:
    UnionFind(int size) {
        parent.resize(size, -1);
        rank.resize(size, 0);
        count = 0;
    }

    void addLand(int x) {
        if (parent[x] >= 0) return;
        parent[x] = x;
        count++;
    }

    bool isLand(int x) {
        if (parent[x] >= 0) {
            return true;
        } else {
            return false;
        }
    }

    int numberOfIslands() { return count; }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void union_set(int x, int y) {
        int xset = find(x), yset = find(y);
        if (xset == yset) {
            return;
        } else if (rank[xset] < rank[yset]) {
            parent[xset] = yset;
        } else if (rank[xset] > rank[yset]) {
            parent[yset] = xset;
        } else {
            parent[yset] = xset;
            rank[xset]++;
        }
        count--;
    }
};

class Solution {
public:
    vector<int> numIslands2(int m, int n, vector<vector<int>>& positions) {
        int x[] = {-1, 1, 0, 0};
        int y[] = {0, 0, -1, 1};
        UnionFind dsu(m * n);
        vector<int> answer;

        for (auto& position : positions) {
            int landPosition = position[0] * n + position[1];
            dsu.addLand(landPosition);

            for (int i = 0; i < 4; i++) {
                int neighborX = position[0] + x[i];
                int neighborY = position[1] + y[i];
                int neighborPosition = neighborX * n + neighborY;
                // If neighborX and neighborY correspond to a point in the grid and there is a land
                // at that point, then merge it with the current land.
                if (neighborX >= 0 && neighborX < m && neighborY >= 0 && neighborY < n &&
                    dsu.isLand(neighborPosition)) {
                    dsu.union_set(landPosition, neighborPosition);
                }
            }
            answer.push_back(dsu.numberOfIslands());
        }
        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n + l)$
- Space complexity: $O(m \cdot n)$

> Where $m$ and $n$ are the number of rows and columns in the given grid, and $l$ is the size of `positions`.
