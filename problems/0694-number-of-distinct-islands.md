# 694. Number of Distinct Islands

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-distinct-islands/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-distinct-islands>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Two islands are considered the same if one can be translated (shifted) to match the other. To identify distinct islands, we need a way to represent each island's shape independent of its position. We do this by normalizing each island: recording each cell's position relative to the island's origin (the first cell we encounter). Then we compare each new island against all previously found unique islands.

```cpp
// NeetCode has no C++ version of this approach yet.
```

**Complexity**

- Time complexity: $O(M^2 \cdot N^2)$
- Space complexity: $O(N \cdot M)$

> Where $M$ is the number of rows, and $N$ is the number of columns

## 2. Hash By Local Coordinates

Instead of comparing islands one by one, we can use a hash set for O(1) lookup. Each island is represented as a set of relative coordinates (offsets from the origin cell). Since sets of tuples are hashable (using frozenset in Python), we can directly add each island's shape to a set of unique islands. Duplicate shapes will naturally be filtered out.

```cpp
// NeetCode has no C++ version of this approach yet.
```

**Complexity**

- Time complexity: $O(M \cdot N)$
- Space complexity: $O(M \cdot N)$

> Where $M$ is the number of rows, and $N$ is the number of columns

## 3. Hash By Path Signature

Another way to uniquely identify an island's shape is through its `dfs` traversal path. If we always explore directions in the same order (e.g., Down, Up, Right, Left), two identical shapes will produce the same sequence of moves. We record each direction taken during `dfs`, and importantly, we also record when we backtrack. This backtrack marker is crucial because without it, different shapes could produce the same direction sequence.

```cpp
class Solution {
private:
    vector<vector<int>>* grid;
    vector<vector<bool>> visited;
    string currentIsland;

    void dfs(int row, int col, char dir) {
        if (row < 0 || col < 0 || row >= grid->size() || col >= (*grid)[0].size()) {
            return;
        }
        if (visited[row][col] || (*grid)[row][col] == 0) {
            return;
        }
        visited[row][col] = true;
        currentIsland += dir;
        dfs(row + 1, col, 'D');
        dfs(row - 1, col, 'U');
        dfs(row, col + 1, 'R');
        dfs(row, col - 1, 'L');
        currentIsland += '0';
    }

public:
    int numDistinctIslands(vector<vector<int>>& grid) {
        this->grid = &grid;
        visited = vector<vector<bool>>(grid.size(), vector<bool>(grid[0].size(), false));
        unordered_set<string> islands;

        for (int row = 0; row < grid.size(); row++) {
            for (int col = 0; col < grid[0].size(); col++) {
                currentIsland = "";
                dfs(row, col, '0');
                if (currentIsland.empty()) {
                    continue;
                }
                islands.insert(currentIsland);
            }
        }
        return islands.size();
    }
};
```

**Complexity**

- Time complexity: $O(M \cdot N)$
- Space complexity: $O(M \cdot N)$

> Where $M$ is the number of rows, and $N$ is the number of columns
